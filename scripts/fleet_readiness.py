#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {p["PROJECT_ID"]: p for p in doc.get("PROJECTS", []) if p.get("PROJECT_ID")}


def add_check(checks: dict[str, bool], name: str, ok: bool, blockers: list[str], reason: str) -> None:
    checks[name] = bool(ok)
    if not ok:
        blockers.append(reason)


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

    template_ok = True
    for rel in ("templates/PROJECT_PROFILE.yml", "templates/MANAGED_REPOSITORY_CONTROL.yml"):
        path = root / rel
        if not path.exists():
            blockers.append(f"MISSING_TEMPLATE:{rel}")
            template_ok = False
            continue
        text = path.read_text(encoding="utf-8")
        if version not in text:
            blockers.append(f"STALE_TEMPLATE_VERSION:{rel}")
            template_ok = False
    checks["ONBOARDING_TEMPLATES_CURRENT"] = template_ok

    automation_requirements = {
        "scripts/enrollment_controller.py": ["PCC-local idempotent fleet enrollment", "TARGET_MUTATED"],
        "scripts/fleet_control.py": ["OBSERVE", "CANARY", "ENFORCE", "apply_policy_sync"],
        ".github/workflows/fleet-control.yml": ["workflow_dispatch", "apply_policy_sync", "fleet_readiness.py"],
        ".github/workflows/control-plane-validation.yml": ["fleet_readiness.py", "test_fleet_readiness.py"],
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

    # The PCC can be 100% ready to enroll more repositories while enrolled
    # repositories remain in OBSERVE with expected policy drift. Enforcement is
    # a separate, per-project promotion decision.
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
