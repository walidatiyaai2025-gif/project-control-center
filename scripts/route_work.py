#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def names_for_project(row: dict[str, Any]) -> set[str]:
    values = [row.get("PROJECT_ID"), row.get("DISPLAY_NAME"), row.get("REPOSITORY")]
    repo = row.get("REPOSITORY") or ""
    if "/" in repo:
        values.append(repo.split("/", 1)[1])
    values.extend(row.get("ALIASES") or [])
    return {norm(v) for v in values if v}


def names_for_variant(row: dict[str, Any]) -> set[str]:
    values = [row.get("VARIANT_ID"), row.get("DISPLAY_NAME")]
    values.extend(row.get("ALIASES") or [])
    return {norm(v) for v in values if v}


def git_sha(root: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def resolve_project(identifier: str, routing: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    needle = norm(identifier)
    matches: list[tuple[dict[str, Any], dict[str, Any] | None, str]] = []
    for project in routing.get("PROJECTS", []):
        if needle in names_for_project(project):
            matches.append((project, None, "PROJECT"))
        for variant in project.get("VARIANTS") or []:
            if needle in names_for_variant(variant):
                matches.append((project, variant, "VARIANT"))
    unique = {(m[0].get("PROJECT_ID"), (m[1] or {}).get("VARIANT_ID"), m[2]) for m in matches}
    if not matches:
        return None, None, "PROJECT_OR_VARIANT_NOT_REGISTERED"
    if len(unique) > 1:
        project_only = [m for m in matches if m[2] == "PROJECT"]
        distinct_projects = {m[0].get("PROJECT_ID") for m in matches}
        if len(project_only) == 1 and len(distinct_projects) == 1:
            return project_only[0][0], None, None
        return None, None, "ROUTING_ALIAS_COLLISION"
    p, v, _ = matches[0]
    return p, v, None


def resolve_variant(identifier: str, project: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    needle = norm(identifier)
    matches = [v for v in project.get("VARIANTS") or [] if needle in names_for_variant(v)]
    if not matches:
        return None, "VARIANT_NOT_REGISTERED_FOR_PROJECT"
    ids = {v.get("VARIANT_ID") for v in matches}
    if len(ids) != 1:
        return None, "VARIANT_ALIAS_COLLISION"
    return matches[0], None


def blocked(reason: str, **extra: Any) -> dict[str, Any]:
    return {"ROUTING_STATUS": "BLOCKED", "REASON": reason, **extra}


def route(root: Path, identifier: str, variant_name: str | None = None, scope: str | None = None, task: str | None = None) -> dict[str, Any]:
    routing_path = root / "portfolio/project-routing.json"
    registry_path = root / "portfolio/projects.yml"
    if not routing_path.exists():
        return blocked("PROJECT_ROUTING_REGISTRY_MISSING")
    routing = load(routing_path)
    registry = load(registry_path)
    project, inferred_variant, error = resolve_project(identifier, routing)
    if error:
        return blocked(error, INPUT=identifier)
    assert project is not None

    registry_ids = {p.get("PROJECT_ID"): p for p in registry.get("PROJECTS", [])}
    registered = registry_ids.get(project.get("PROJECT_ID"))
    if not registered or registered.get("REPOSITORY") != project.get("REPOSITORY"):
        return blocked("ROUTING_RECORD_NOT_ALIGNED_TO_FLEET_REGISTRY", PROJECT_ID=project.get("PROJECT_ID"))

    constitution_state = project.get("CONSTITUTION_STATE")
    if constitution_state != "READY":
        return blocked("REPOSITORY_CONSTITUTION_NOT_READY", PROJECT_ID=project.get("PROJECT_ID"), REPOSITORY=project.get("REPOSITORY"), CONSTITUTION_STATE=constitution_state, CONSTITUTION_PATH=project.get("CONSTITUTION_PATH"))

    normalization_state = project.get("ONBOARDING_NORMALIZATION_STATE")
    if normalization_state != "READY":
        return blocked("PROJECT_ONBOARDING_NORMALIZATION_NOT_READY", PROJECT_ID=project.get("PROJECT_ID"), ONBOARDING_NORMALIZATION_STATE=normalization_state)

    model = project.get("PROJECT_MODEL")
    target_scope = (scope or "").upper() or None
    target_variant = inferred_variant

    if variant_name:
        target_variant, error = resolve_variant(variant_name, project)
        if error:
            return blocked(error, PROJECT_ID=project.get("PROJECT_ID"), VARIANT_INPUT=variant_name)
        if inferred_variant and target_variant.get("VARIANT_ID") != inferred_variant.get("VARIANT_ID"):
            return blocked("PROJECT_INPUT_AND_VARIANT_INPUT_CONFLICT")

    target_location = None
    target_location_state = None

    if model == "STANDALONE":
        if target_variant or variant_name:
            return blocked("STANDALONE_PROJECT_DOES_NOT_ACCEPT_VARIANT")
        target_scope = target_scope or "PROJECT"
        if target_scope != "PROJECT":
            return blocked("INVALID_SCOPE_FOR_STANDALONE_PROJECT", TARGET_SCOPE=target_scope)
        impacted_variants: list[str] = []
        cross_variant = False
        change_boundary = "PROJECT"
    elif model == "PRODUCT_FAMILY":
        if target_variant and not target_scope:
            target_scope = "VARIANT"
        if not target_scope:
            return blocked("TARGET_SCOPE_REQUIRED_FOR_PRODUCT_FAMILY", PROJECT_ID=project.get("PROJECT_ID"), ALLOWED_SCOPES=["CORE", "VARIANT"])
        if target_scope == "CORE":
            if target_variant:
                return blocked("CORE_SCOPE_CANNOT_TARGET_SINGLE_VARIANT")
            core_state = project.get("CORE_ROUTING_STATE")
            if core_state != "READY":
                return blocked("SHARED_CORE_BOUNDARY_NOT_READY", PROJECT_ID=project.get("PROJECT_ID"), CORE_ROUTING_STATE=core_state)
            impacted_variants = [v.get("VARIANT_ID") for v in project.get("VARIANTS", []) if v.get("STATUS") == "ACTIVE"]
            cross_variant = True
            change_boundary = "SHARED_CORE"
        elif target_scope == "VARIANT":
            if not target_variant:
                return blocked("TARGET_VARIANT_REQUIRED", PROJECT_ID=project.get("PROJECT_ID"))
            if target_variant.get("STATUS") != "ACTIVE":
                return blocked("TARGET_VARIANT_NOT_ACTIVE", TARGET_VARIANT=target_variant.get("VARIANT_ID"))
            if target_variant.get("ROUTING_STATE") != "READY":
                return blocked(
                    "TARGET_VARIANT_BOUNDARY_NOT_READY",
                    PROJECT_ID=project.get("PROJECT_ID"),
                    TARGET_VARIANT=target_variant.get("VARIANT_ID"),
                    ROUTING_STATE=target_variant.get("ROUTING_STATE"),
                    IMPLEMENTATION_LOCATION_STATE=target_variant.get("IMPLEMENTATION_LOCATION_STATE"),
                )
            target_location = target_variant.get("IMPLEMENTATION_LOCATION")
            target_location_state = target_variant.get("IMPLEMENTATION_LOCATION_STATE")
            impacted_variants = [target_variant.get("VARIANT_ID")]
            cross_variant = False
            change_boundary = f"{target_variant.get('VARIANT_ID')}_ONLY"
        else:
            return blocked("INVALID_SCOPE_FOR_PRODUCT_FAMILY", TARGET_SCOPE=target_scope)
    else:
        return blocked("INVALID_PROJECT_MODEL", PROJECT_MODEL=model)

    read_first = [project.get("CONSTITUTION_PATH")]
    if project.get("FAMILY_MANIFEST_PATH"):
        read_first.append(project.get("FAMILY_MANIFEST_PATH"))
    read_first = [x for x in read_first if x]

    return {
        "ROUTING_STATUS": "ROUTED",
        "ROUTING_CONTRACT_VERSION": routing.get("ROUTING_CONTRACT_VERSION"),
        "CONTROL_PLANE_VERSION": routing.get("CONTROL_PLANE_VERSION"),
        "PCC_SOURCE_SHA": git_sha(root),
        "PROJECT_ID": project.get("PROJECT_ID"),
        "REPOSITORY": project.get("REPOSITORY"),
        "PROJECT_MODEL": model,
        "ONBOARDING_NORMALIZATION_STATE": normalization_state,
        "VARIANT_GOVERNANCE_STATE": project.get("VARIANT_GOVERNANCE_STATE"),
        "CORE_ROUTING_STATE": project.get("CORE_ROUTING_STATE"),
        "TARGET_SCOPE": target_scope,
        "TARGET_VARIANT": target_variant.get("VARIANT_ID") if target_variant else None,
        "TARGET_VARIANT_DISPLAY_NAME": target_variant.get("DISPLAY_NAME") if target_variant else None,
        "TARGET_IMPLEMENTATION_LOCATION": target_location,
        "TARGET_IMPLEMENTATION_LOCATION_STATE": target_location_state,
        "IMPACTED_VARIANTS": impacted_variants,
        "REQUIRES_CROSS_VARIANT_VALIDATION": cross_variant,
        "CHANGE_BOUNDARY": change_boundary,
        "CONSTITUTION_PATH": project.get("CONSTITUTION_PATH"),
        "CONSTITUTION_SOURCE_SHA": project.get("CONSTITUTION_SOURCE_SHA"),
        "FAMILY_MANIFEST_PATH": project.get("FAMILY_MANIFEST_PATH"),
        "READ_FIRST": read_first,
        "TASK": task,
        "WORKER_INSTRUCTION": "Read the repository constitution and family manifest first. Modify only the routed boundary and implementation location. If repository evidence contradicts this route, stop and return ROUTING_CONFLICT instead of guessing.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve a project/client label into an authoritative PCC worker routing packet")
    ap.add_argument("--project", required=True, help="Project, repository, client, variant, or registered alias")
    ap.add_argument("--variant")
    ap.add_argument("--scope", choices=["PROJECT", "CORE", "VARIANT", "project", "core", "variant"])
    ap.add_argument("--task")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()
    result = route(Path(args.root).resolve(), args.project, args.variant, args.scope, args.task)
    print(json.dumps(result, indent=2) + "\n", end="")
    return 0 if result.get("ROUTING_STATUS") == "ROUTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
