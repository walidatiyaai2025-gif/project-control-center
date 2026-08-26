#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

MODES = {"OBSERVE", "WARN", "CANARY", "ENFORCE"}
WRITE_MODES = {"CANARY", "ENFORCE"}
ALLOWLISTED_MANAGED_FILES = {
    ".github/workflows/reusable-version-governance.yml",
    ".github/workflows/reusable-feature-delivery-governance.yml",
    ".pcc/managed-repository-control.json",
}
REGISTRY_REQUIRED = {
    "PROJECT_ID",
    "DISPLAY_NAME",
    "REPOSITORY",
    "ENROLLMENT_STATE",
    "DISCOVERY_STATE",
    "POLICY_ENFORCEMENT_MODE",
    "ROLLOUT_WAVE",
    "CONTROL_PLANE_VERSION",
    "DESIRED_POLICY_VERSION",
    "MANAGED_FILES",
    "WRITE_AUTHORIZED",
    "CANONICAL_DEVELOPMENT_LINEAGE",
}
DESIRED_PARITY_KEYS = {
    "PROJECT_ID",
    "REPOSITORY",
    "CONTROL_PLANE_VERSION",
    "DESIRED_POLICY_VERSION",
    "POLICY_ENFORCEMENT_MODE",
    "ROLLOUT_WAVE",
    "CANARY",
    "WRITE_AUTHORIZED",
    "CANONICAL_DEVELOPMENT_LINEAGE",
    "MANAGED_FILES",
}
ROUTING_MODELS = {"STANDALONE", "PRODUCT_FAMILY"}
ROUTING_ACCEPTED_CONSTITUTION_STATES = {"READY", "LEGACY_PENDING"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {p["PROJECT_ID"]: p for p in doc.get("PROJECTS", []) if p.get("PROJECT_ID")}


def norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def add_check(checks: dict[str, bool], name: str, ok: bool, blockers: list[str], reason: str) -> None:
    checks[name] = bool(ok)
    if not ok:
        blockers.append(reason)


def validate_routing(root: Path, registry: dict[str, Any], version: str, blockers: list[str], warnings: list[str]) -> tuple[bool, int]:
    path = root / "portfolio/project-routing.json"
    if not path.exists():
        blockers.append("PROJECT_ROUTING_REGISTRY_MISSING")
        return False, 0
    try:
        routing = load(path)
    except Exception as exc:
        blockers.append(f"PROJECT_ROUTING_REGISTRY_PARSE_FAILED:{exc}")
        return False, 0
    if routing.get("CONTROL_PLANE_VERSION") != version:
        blockers.append("PROJECT_ROUTING_CONTROL_PLANE_VERSION_MISMATCH")
        return False, 0

    projects = registry.get("PROJECTS", [])
    registered = by_id(registry)
    rows = by_id(routing)
    ok = set(rows) == set(registered)
    if not ok:
        blockers.append("PROJECT_ROUTING_REGISTRY_PROJECT_SET_MISMATCH")

    global_alias_owner: dict[str, str] = {}
    routable = 0
    for pid, project in registered.items():
        row = rows.get(pid)
        if not row:
            continue
        if row.get("REPOSITORY") != project.get("REPOSITORY"):
            blockers.append(f"{pid}:PROJECT_ROUTING_REPOSITORY_MISMATCH")
            ok = False
        if row.get("PROJECT_MODEL") not in ROUTING_MODELS:
            blockers.append(f"{pid}:INVALID_PROJECT_MODEL")
            ok = False
        if row.get("ROUTING_REQUIRED") is not True:
            blockers.append(f"{pid}:ROUTING_MUST_BE_REQUIRED")
            ok = False
        if not row.get("CONSTITUTION_PATH"):
            blockers.append(f"{pid}:CONSTITUTION_PATH_REQUIRED")
            ok = False
        state = row.get("CONSTITUTION_STATE")
        if state not in ROUTING_ACCEPTED_CONSTITUTION_STATES:
            blockers.append(f"{pid}:CONSTITUTION_NOT_READY_FOR_ONBOARDING:{state}")
            ok = False
        elif state == "LEGACY_PENDING":
            warnings.append(f"{pid}:LEGACY_CONSTITUTION_PENDING_WORKER_ROUTING")
        elif state == "READY":
            routable += 1

        alias_values = [pid, row.get("DISPLAY_NAME"), row.get("REPOSITORY")]
        alias_values.extend(row.get("ALIASES") or [])
        repo = row.get("REPOSITORY") or ""
        if "/" in repo:
            alias_values.append(repo.split("/", 1)[1])

        variants = row.get("VARIANTS") or []
        if row.get("PROJECT_MODEL") == "STANDALONE":
            if variants:
                blockers.append(f"{pid}:STANDALONE_PROJECT_MUST_NOT_DECLARE_VARIANTS")
                ok = False
            if row.get("FAMILY_MANIFEST_PATH") is not None:
                blockers.append(f"{pid}:STANDALONE_PROJECT_FAMILY_MANIFEST_MUST_BE_NULL")
                ok = False
        elif row.get("PROJECT_MODEL") == "PRODUCT_FAMILY":
            if not row.get("FAMILY_MANIFEST_PATH"):
                blockers.append(f"{pid}:PRODUCT_FAMILY_MANIFEST_REQUIRED")
                ok = False
            active = [v for v in variants if v.get("STATUS") == "ACTIVE"]
            ids = [v.get("VARIANT_ID") for v in variants]
            if len(active) < 2 or len(ids) != len(set(ids)) or any(not x for x in ids):
                blockers.append(f"{pid}:PRODUCT_FAMILY_VARIANTS_INVALID")
                ok = False
            for v in variants:
                alias_values.extend([v.get("VARIANT_ID"), v.get("DISPLAY_NAME")])
                alias_values.extend(v.get("ALIASES") or [])

        for value in alias_values:
            key = norm(value)
            if not key:
                continue
            owner = global_alias_owner.get(key)
            if owner and owner != pid:
                blockers.append(f"ROUTING_ALIAS_COLLISION:{value}:{owner}:{pid}")
                ok = False
            else:
                global_alias_owner[key] = pid

    return ok, routable


def validate_static(root: Path) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    checks: dict[str, bool] = {}

    version_path = root / "VERSION"
    registry_path = root / "portfolio/projects.yml"
    desired_path = root / "orchestration/desired-state.json"
    version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else ""

    try:
        registry = load(registry_path)
        desired = load(desired_path)
    except Exception as exc:
        return {
            "CONTROL_PLANE_VERSION": version or None,
            "READINESS_PROFILE": "FLEET_ONBOARDING",
            "CHECKS": {"CONFIG_PARSE": False},
            "BLOCKERS": [f"CONFIG_PARSE_FAILED:{exc}"],
            "WARNINGS": [],
            "READINESS_PERCENT": 0,
            "ONBOARDING_READY": False,
        }

    add_check(
        checks,
        "VERSION_ALIGNMENT",
        bool(version)
        and registry.get("CONTROL_PLANE_VERSION") == version
        and desired.get("CONTROL_PLANE_VERSION") == version,
        blockers,
        "CONTROL_PLANE_VERSION_MISMATCH",
    )

    projects = registry.get("PROJECTS", [])
    ids = [p.get("PROJECT_ID") for p in projects]
    repos = [p.get("REPOSITORY") for p in projects]
    identity_ok = (
        all(isinstance(x, str) and x.strip() for x in ids + repos)
        and len(ids) == len(set(ids))
        and len(repos) == len(set(repos))
    )
    add_check(checks, "REGISTRY_IDENTITY", identity_ok, blockers, "REGISTRY_IDENTITY_INVALID_OR_DUPLICATE")

    profile_ok = True
    desired_map = by_id(desired)
    for p in projects:
        pid = p.get("PROJECT_ID", "<missing>")
        missing = sorted(REGISTRY_REQUIRED - set(p))
        if missing:
            blockers.append(f"{pid}:MISSING_REQUIRED_FIELDS:{','.join(missing)}")
            profile_ok = False
            continue
        if p.get("CONTROL_PLANE_VERSION") != version:
            blockers.append(f"{pid}:STALE_CONTROL_PLANE_VERSION")
            profile_ok = False
        if p.get("POLICY_ENFORCEMENT_MODE") not in MODES:
            blockers.append(f"{pid}:INVALID_MODE")
            profile_ok = False
        managed = p.get("MANAGED_FILES") or []
        bad_paths = sorted(set(managed) - ALLOWLISTED_MANAGED_FILES)
        if bad_paths:
            blockers.append(f"{pid}:NON_ALLOWLISTED_MANAGED_FILES:{','.join(bad_paths)}")
            profile_ok = False
        if p.get("POLICY_ENFORCEMENT_MODE") == "CANARY" and not p.get("CANARY"):
            blockers.append(f"{pid}:CANARY_MODE_WITHOUT_CANARY_FLAG")
            profile_ok = False
        if p.get("POLICY_ENFORCEMENT_MODE") in WRITE_MODES:
            if not p.get("WRITE_AUTHORIZED"):
                blockers.append(f"{pid}:WRITE_MODE_WITHOUT_AUTHORIZATION")
                profile_ok = False
            if p.get("CANONICAL_DEVELOPMENT_LINEAGE", "UNRESOLVED") == "UNRESOLVED":
                blockers.append(f"{pid}:WRITE_MODE_WITH_UNRESOLVED_LINEAGE")
                profile_ok = False
        d = desired_map.get(pid)
        if not d:
            blockers.append(f"{pid}:MISSING_DESIRED_STATE")
            profile_ok = False
        else:
            for key in DESIRED_PARITY_KEYS:
                if p.get(key) != d.get(key):
                    blockers.append(f"{pid}:DESIRED_STATE_MISMATCH:{key}")
                    profile_ok = False
    extra_desired = sorted(set(desired_map) - set(ids))
    if extra_desired:
        blockers.append(f"DESIRED_STATE_HAS_UNREGISTERED_PROJECTS:{','.join(extra_desired)}")
        profile_ok = False
    checks["REGISTRY_AND_DESIRED_STATE_PARITY"] = profile_ok

    routing_ok, routable_projects = validate_routing(root, registry, version, blockers, warnings)
    checks["PROJECT_AND_VARIANT_ROUTING"] = routing_ok

    template_ok = True
    for rel in ("templates/PROJECT_PROFILE.yml", "templates/MANAGED_REPOSITORY_CONTROL.yml", "templates/PROJECT_ROUTING.json"):
        path = root / rel
        if not path.exists():
            blockers.append(f"MISSING_TEMPLATE:{rel}")
            template_ok = False
            continue
        text = path.read_text(encoding="utf-8")
        if rel != "templates/PROJECT_ROUTING.json" and version not in text:
            blockers.append(f"STALE_TEMPLATE_VERSION:{rel}")
            template_ok = False
        if rel == "templates/PROJECT_ROUTING.json" and "CONSTITUTION_STATE" not in text:
            blockers.append(f"ROUTING_TEMPLATE_INCOMPLETE:{rel}")
            template_ok = False
    checks["ONBOARDING_TEMPLATES_CURRENT"] = template_ok

    automation_requirements = {
        "scripts/enrollment_controller.py": ["PCC-local idempotent fleet enrollment", "TARGET_MUTATED"],
        "scripts/fleet_control.py": ["OBSERVE", "CANARY", "ENFORCE", "apply_policy_sync"],
        "scripts/route_work.py": ["PCC worker routing packet", "REPOSITORY_CONSTITUTION_NOT_READY", "TARGET_SCOPE_REQUIRED_FOR_PRODUCT_FAMILY"],
        ".github/workflows/fleet-control.yml": ["workflow_dispatch", "apply_policy_sync", "fleet_readiness.py"],
        ".github/workflows/control-plane-validation.yml": ["fleet_readiness.py", "test_fleet_readiness.py", "test_route_work.py"],
    }
    automation_ok = True
    for rel, needles in automation_requirements.items():
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if not all(n in text for n in needles):
            blockers.append(f"ONBOARDING_AUTOMATION_INCOMPLETE:{rel}")
            automation_ok = False
    checks["ONBOARDING_AUTOMATION"] = automation_ok

    safety_requirements = {
        "policies/FLEET_CONTROL_POLICY.md": ["read before write", "OBSERVE -> WARN -> CANARY -> ENFORCE", "Automatic deletion is forbidden"],
        "policies/PROJECT_FAMILY_ROUTING_POLICY.md": ["Every implementation worker MUST receive", "CONSTITUTION_STATE=PENDING", "Alias collisions are governance blockers"],
        "scripts/fleet_control.py": ["PATH_NOT_ALLOWLISTED", "BREAK_GLASS_ACTIVE", "WRITE_AUTH_PROVIDER_REQUIRED"],
        "scripts/self_protection.py": ["MAIN_PROTECTION_NOT_CONFIGURED", "REPOSITORY_ADMIN_WRITE_CREDENTIAL_REQUIRED"],
    }
    safety_ok = True
    for rel, needles in safety_requirements.items():
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if not all(n in text for n in needles):
            blockers.append(f"SAFETY_CONTRACT_INCOMPLETE:{rel}")
            safety_ok = False
    checks["SAFETY_GATES"] = safety_ok

    if any(p.get("POLICY_ENFORCEMENT_MODE") in {"OBSERVE", "WARN"} for p in projects):
        warnings.append("OBSERVE_OR_WARN_PROJECTS_MAY_HAVE_EXPECTED_POLICY_DRIFT_BEFORE_PROMOTION")

    evaluated = len(checks)
    passed = sum(checks.values())
    percent = round((passed / evaluated) * 100) if evaluated else 0
    return {
        "CONTROL_PLANE_VERSION": version or None,
        "READINESS_PROFILE": "FLEET_ONBOARDING",
        "CHECKS": checks,
        "BLOCKERS": blockers,
        "WARNINGS": warnings,
        "READINESS_PERCENT": percent,
        "ONBOARDING_READY": percent == 100 and not blockers,
        "REGISTERED_PROJECTS": len(projects),
        "ROUTABLE_PROJECTS": routable_projects,
    }


def validate_live(root: Path, live_report: Path, result: dict[str, Any]) -> dict[str, Any]:
    try:
        report = load(live_report)
        registry = load(root / "portfolio/projects.yml")
    except Exception as exc:
        result["CHECKS"]["LIVE_FLEET_COLLECTION"] = False
        result["BLOCKERS"].append(f"LIVE_REPORT_PARSE_FAILED:{exc}")
        return result

    expected = {p["PROJECT_ID"] for p in registry.get("PROJECTS", [])}
    rows = {p.get("PROJECT_ID"): p for p in report.get("PROJECTS", [])}
    live_ok = report.get("CONTROL_PLANE_VERSION") == result.get("CONTROL_PLANE_VERSION") and set(rows) == expected
    for pid in sorted(expected):
        row = rows.get(pid, {})
        live_ok = live_ok and row.get("RESULT") == "PASS"
        live_ok = live_ok and row.get("SNAPSHOT", {}).get("DISCOVERY_COMPLETE") is True
        live_ok = live_ok and row.get("BASELINE", {}).get("RESULT") == "LOCKED"
        live_ok = live_ok and row.get("RECONCILIATION", {}).get("RESULT") == "RECONCILED_READ_ONLY"
    result["CHECKS"]["LIVE_FLEET_COLLECTION"] = bool(live_ok)
    if not live_ok:
        result["BLOCKERS"].append("LIVE_FLEET_COLLECTION_NOT_ACCEPTED")

    evaluated = len(result["CHECKS"])
    passed = sum(bool(v) for v in result["CHECKS"].values())
    result["READINESS_PERCENT"] = round((passed / evaluated) * 100) if evaluated else 0
    result["ONBOARDING_READY"] = result["READINESS_PERCENT"] == 100 and not result["BLOCKERS"]
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PCC fleet-onboarding readiness without mutating target repositories")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--live-report")
    ap.add_argument("--out")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    result = validate_static(root)
    if args.live_report:
        result = validate_live(root, Path(args.live_report), result)
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.get("ONBOARDING_READY") else 2


if __name__ == "__main__":
    raise SystemExit(main())
