#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

NORMALIZATION_STATES = {"READY", "LEGACY_PENDING"}
FAMILY_STATES = {"READY", "PARTIAL"}
LOCATION_STATES = {"MAPPED", "EXTERNAL_REPOSITORY", "UNRESOLVED", "UNMATERIALIZED"}
ROUTING_STATES = {"READY", "BLOCKED_UNRESOLVED", "BLOCKED_UNMATERIALIZED", "ARCHIVED"}


def validate_routing_normalization(doc: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    registered_variants = 0
    routable_variants = 0
    blocked_variants = 0
    families = 0

    for project in doc.get("PROJECTS", []):
        pid = project.get("PROJECT_ID") or "<missing>"
        model = project.get("PROJECT_MODEL")
        normalization = project.get("ONBOARDING_NORMALIZATION_STATE")
        if normalization not in NORMALIZATION_STATES:
            errors.append(f"{pid}:ONBOARDING_NORMALIZATION_STATE_INVALID_OR_MISSING")
            continue
        if normalization == "LEGACY_PENDING":
            warnings.append(f"{pid}:LEGACY_ONBOARDING_NORMALIZATION_PENDING")

        if model == "STANDALONE":
            if project.get("VARIANT_GOVERNANCE_STATE") != "NOT_APPLICABLE":
                errors.append(f"{pid}:STANDALONE_VARIANT_GOVERNANCE_STATE_MUST_BE_NOT_APPLICABLE")
            if project.get("CORE_ROUTING_STATE") != "NOT_APPLICABLE":
                errors.append(f"{pid}:STANDALONE_CORE_ROUTING_STATE_MUST_BE_NOT_APPLICABLE")
            if project.get("VARIANTS"):
                errors.append(f"{pid}:STANDALONE_MUST_NOT_HAVE_VARIANTS")
            continue

        if model != "PRODUCT_FAMILY":
            errors.append(f"{pid}:UNKNOWN_PROJECT_MODEL_FOR_NORMALIZATION")
            continue

        families += 1
        if normalization != "READY":
            errors.append(f"{pid}:PRODUCT_FAMILY_NORMALIZATION_NOT_READY")

        declared_family_state = project.get("VARIANT_GOVERNANCE_STATE")
        if declared_family_state not in FAMILY_STATES:
            errors.append(f"{pid}:VARIANT_GOVERNANCE_STATE_INVALID_OR_MISSING")

        core_state = project.get("CORE_ROUTING_STATE")
        if core_state not in {"READY", "BLOCKED_UNRESOLVED"}:
            errors.append(f"{pid}:CORE_ROUTING_STATE_INVALID_OR_MISSING")

        variants = project.get("VARIANTS") or []
        active = [v for v in variants if v.get("STATUS") == "ACTIVE"]
        if len(active) < 2:
            errors.append(f"{pid}:PRODUCT_FAMILY_REQUIRES_AT_LEAST_TWO_ACTIVE_VARIANTS")

        all_active_ready = True
        seen: set[str] = set()
        for variant in variants:
            vid = variant.get("VARIANT_ID") or "<missing>"
            registered_variants += 1
            if vid in seen:
                errors.append(f"{pid}:DUPLICATE_VARIANT_ID:{vid}")
            seen.add(vid)

            location_state = variant.get("IMPLEMENTATION_LOCATION_STATE")
            route_state = variant.get("ROUTING_STATE")
            if location_state not in LOCATION_STATES:
                errors.append(f"{pid}:{vid}:IMPLEMENTATION_LOCATION_STATE_INVALID_OR_MISSING")
            if route_state not in ROUTING_STATES:
                errors.append(f"{pid}:{vid}:ROUTING_STATE_INVALID_OR_MISSING")

            if variant.get("STATUS") != "ACTIVE":
                continue

            if route_state == "READY":
                routable_variants += 1
                if location_state not in {"MAPPED", "EXTERNAL_REPOSITORY"}:
                    errors.append(f"{pid}:{vid}:READY_ROUTE_REQUIRES_VERIFIED_LOCATION")
                if not variant.get("IMPLEMENTATION_LOCATION"):
                    errors.append(f"{pid}:{vid}:READY_ROUTE_REQUIRES_IMPLEMENTATION_LOCATION")
            else:
                blocked_variants += 1
                all_active_ready = False
                if location_state == "UNRESOLVED" and route_state != "BLOCKED_UNRESOLVED":
                    errors.append(f"{pid}:{vid}:UNRESOLVED_LOCATION_REQUIRES_BLOCKED_UNRESOLVED")
                if location_state == "UNMATERIALIZED" and route_state != "BLOCKED_UNMATERIALIZED":
                    errors.append(f"{pid}:{vid}:UNMATERIALIZED_LOCATION_REQUIRES_BLOCKED_UNMATERIALIZED")

        computed = "READY" if all_active_ready and core_state == "READY" else "PARTIAL"
        if declared_family_state in FAMILY_STATES and declared_family_state != computed:
            errors.append(f"{pid}:VARIANT_GOVERNANCE_STATE_MISMATCH:{declared_family_state}:{computed}")
        if computed == "PARTIAL":
            warnings.append(f"{pid}:PRODUCT_FAMILY_PARTIAL_ROUTING")

    return {
        "PASS": not errors,
        "ERRORS": errors,
        "WARNINGS": warnings,
        "REGISTERED_PROJECT_FAMILIES": families,
        "REGISTERED_VARIANTS": registered_variants,
        "ROUTABLE_VARIANTS": routable_variants,
        "BLOCKED_VARIANTS": blocked_variants,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PCC project-family onboarding normalization")
    ap.add_argument("--routing", default=str(Path(__file__).resolve().parents[1] / "portfolio/project-routing.json"))
    args = ap.parse_args()
    doc = json.loads(Path(args.routing).read_text(encoding="utf-8"))
    result = validate_routing_normalization(doc)
    print(json.dumps(result, indent=2))
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
