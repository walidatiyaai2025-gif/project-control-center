import json
from pathlib import Path
import sys

TEMPORARY_STATES = {
    "SERVICE_RESTORED_TEMPORARY",
    "TRACKED_FOR_PERMANENT_FIX",
    "PERMANENT_FIX_IN_PROGRESS",
    "READY_FOR_QA",
    "RESOLVED_PERMANENT",
    "CLOSED",
}
TRACKED_STATES = {
    "TRACKED_FOR_PERMANENT_FIX",
    "PERMANENT_FIX_IN_PROGRESS",
    "READY_FOR_QA",
    "RESOLVED_PERMANENT",
    "CLOSED",
}


def validate_incident(doc):
    errors = []
    required = [
        "INCIDENT_ID", "PROJECT_ID", "REPOSITORY", "TARGET_SCOPE", "SEVERITY",
        "STATE", "PRODUCTION_BASE_SHA", "DISCOVERED_AT", "TEMPORARY_MITIGATION",
        "ROOT_CAUSE_STATUS", "PERMANENT_FIX_REQUIRED", "REGRESSION_TEST_REQUIRED",
        "CARRY_FORWARD_TO_FUTURE_RELEASES", "RELEASE_GATE_STATE"
    ]
    for key in required:
        if key not in doc:
            errors.append(f"MISSING_REQUIRED:{key}")

    if errors:
        return {"PASS": False, "ERRORS": errors}

    if doc.get("TARGET_SCOPE") == "VARIANT" and not doc.get("TARGET_VARIANT"):
        errors.append("VARIANT_SCOPE_REQUIRES_TARGET_VARIANT")

    mitigation = doc.get("TEMPORARY_MITIGATION") or {}
    temporary = bool(mitigation.get("APPLIED"))
    state = doc.get("STATE")

    if state in TEMPORARY_STATES and temporary:
        for key in ("TASK_ID", "BRANCH", "SHA"):
            if not mitigation.get(key):
                errors.append(f"TEMPORARY_MITIGATION_REQUIRES:{key}")
        if not mitigation.get("DEPLOYMENT_EVIDENCE"):
            errors.append("TEMPORARY_MITIGATION_REQUIRES:DEPLOYMENT_EVIDENCE")
        if not doc.get("REGRESSION_TEST_REQUIRED"):
            errors.append("TEMPORARY_MITIGATION_REQUIRES_REGRESSION_PROTECTION")
        if not doc.get("CARRY_FORWARD_TO_FUTURE_RELEASES") and state not in {"RESOLVED_PERMANENT", "CLOSED"}:
            errors.append("TEMPORARY_MITIGATION_MUST_CARRY_FORWARD_UNTIL_PERMANENT_RESOLUTION")

    if doc.get("PERMANENT_FIX_REQUIRED") and state in TRACKED_STATES:
        if not doc.get("PERMANENT_FIX_TASK_ID"):
            errors.append("PERMANENT_FIX_TASK_REQUIRED")
        if not doc.get("PERMANENT_FIX_TARGET_VERSION"):
            errors.append("PERMANENT_FIX_TARGET_VERSION_REQUIRED")

    if state == "SERVICE_RESTORED_TEMPORARY" and not temporary:
        errors.append("SERVICE_RESTORED_TEMPORARY_REQUIRES_TEMPORARY_MITIGATION")

    if state == "CLOSED":
        if temporary and doc.get("PERMANENT_FIX_REQUIRED"):
            if doc.get("ROOT_CAUSE_STATUS") != "CONFIRMED":
                errors.append("CLOSED_REQUIRES_CONFIRMED_ROOT_CAUSE")
            if not doc.get("PERMANENT_FIX_TASK_ID"):
                errors.append("CLOSED_REQUIRES_PERMANENT_FIX_TASK")
            if not doc.get("PERMANENT_FIX_SHA"):
                errors.append("CLOSED_REQUIRES_PERMANENT_FIX_SHA")
            if doc.get("REGRESSION_TEST_REQUIRED") and not doc.get("REGRESSION_TEST_EVIDENCE"):
                errors.append("CLOSED_REQUIRES_REGRESSION_EVIDENCE")
            if doc.get("RELEASE_GATE_STATE") != "CLEARED":
                errors.append("CLOSED_REQUIRES_CLEARED_RELEASE_GATE")
            if doc.get("CARRY_FORWARD_TO_FUTURE_RELEASES"):
                errors.append("CLOSED_CANNOT_RETAIN_CARRY_FORWARD_OBLIGATION")

    return {"PASS": not errors, "ERRORS": errors}


def validate_path(path):
    p = Path(path)
    doc = json.loads(p.read_text(encoding="utf-8"))
    return validate_incident(doc)


def main(argv):
    if len(argv) != 2:
        print("usage: incident_governance.py <incident.json>")
        return 2
    result = validate_path(argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
