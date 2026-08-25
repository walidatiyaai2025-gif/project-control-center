#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import tempfile
import sys

MODES = ("OBSERVE", "WARN", "CANARY", "ENFORCE")
SAFE_HEAL_KEYS = {"DERIVED_STATUS_STALE"}
COMPARE_KEYS = (
    "CONTROL_PLANE_VERSION",
    "DESIRED_POLICY_VERSION",
    "VERSION_POLICY",
    "VERSION_SOURCE",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def by_project(doc: dict) -> dict[str, dict]:
    return {p["PROJECT_ID"]: p for p in doc.get("PROJECTS", []) if p.get("PROJECT_ID")}


def operation_key(project: dict, mode: str) -> str:
    material = json.dumps({
        "PROJECT_ID": project.get("PROJECT_ID"),
        "CONTROL_PLANE_VERSION": project.get("CONTROL_PLANE_VERSION"),
        "DESIRED_POLICY_VERSION": project.get("DESIRED_POLICY_VERSION"),
        "MODE": mode,
        "ROLLOUT_WAVE": project.get("ROLLOUT_WAVE", 0),
    }, sort_keys=True)
    return hashlib.sha256(material.encode()).hexdigest()[:24]


def compatibility(desired: dict, observed: dict | None, mode: str) -> list[str]:
    blockers = []
    if observed is None:
        blockers.append("OBSERVED_STATE_MISSING")
        return blockers
    if mode in ("CANARY", "ENFORCE"):
        if not observed.get("DISCOVERY_COMPLETE"):
            blockers.append("DISCOVERY_NOT_COMPLETE")
        if not observed.get("BASELINE_LOCKED"):
            blockers.append("BASELINE_NOT_LOCKED")
        if desired.get("VERSION_POLICY") != "none-nonproduct" and not observed.get("VERSION_BASELINE_ESTABLISHED"):
            blockers.append("VERSION_BASELINE_NOT_ESTABLISHED")
    return blockers


def drift(desired: dict, observed: dict | None) -> list[str]:
    if observed is None:
        return ["OBSERVED_STATE_MISSING"]
    result = []
    for key in COMPARE_KEYS:
        wanted = desired.get(key)
        seen_key = "OBSERVED_POLICY_VERSION" if key == "DESIRED_POLICY_VERSION" else key
        seen = observed.get(seen_key)
        if wanted is not None and wanted != seen:
            result.append(f"{key}:{seen!r}->{wanted!r}")
    return result


def acquire_lock(project_id: str, op_key: str):
    lock_dir = Path(tempfile.gettempdir()) / "pcc-orchestrator-locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    path = lock_dir / f"{project_id}-{op_key}.lock"
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    return path


def release_lock(path: Path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def safe_heal(observed: dict) -> list[str]:
    healed = []
    if observed.get("DERIVED_STATUS_STALE") is True:
        observed["DERIVED_STATUS_STALE"] = False
        observed["LAST_RECONCILED_AT"] = dt.datetime.now(dt.timezone.utc).isoformat()
        healed.append("DERIVED_STATUS_STALE")
    return healed


def reconcile(desired_doc: dict, observed_doc: dict, mode_override: str | None = None,
              project_filter: str | None = None, apply_safe: bool = False) -> tuple[dict, dict]:
    observed_map = by_project(observed_doc)
    results = []
    for desired in desired_doc.get("PROJECTS", []):
        pid = desired.get("PROJECT_ID")
        if not pid or (project_filter and pid != project_filter):
            continue
        mode = mode_override or desired.get("POLICY_ENFORCEMENT_MODE", "OBSERVE")
        if mode not in MODES:
            results.append({"PROJECT_ID": pid, "RESULT": "FAILED", "ERROR": f"invalid mode {mode}"})
            continue
        op_key = operation_key(desired, mode)
        lock = None
        try:
            lock = acquire_lock(pid, op_key)
            observed = observed_map.get(pid)
            blockers = compatibility(desired, observed, mode)
            deltas = drift(desired, observed)
            healed = []
            if apply_safe and observed is not None:
                healed = safe_heal(observed)
            if blockers:
                result = "BLOCKED"
            elif healed:
                result = "SAFE_HEALED"
            elif deltas:
                result = "DRIFT" if mode in ("OBSERVE", "WARN") else "PLANNED"
            else:
                result = "NOOP"
            results.append({
                "PROJECT_ID": pid,
                "OPERATION_KEY": op_key,
                "MODE": mode,
                "ROLLOUT_WAVE": desired.get("ROLLOUT_WAVE", 0),
                "DESIRED_CONTROL_PLANE_VERSION": desired.get("CONTROL_PLANE_VERSION"),
                "DESIRED_POLICY_VERSION": desired.get("DESIRED_POLICY_VERSION"),
                "OBSERVED_CONTROL_PLANE_VERSION": observed.get("CONTROL_PLANE_VERSION") if observed else None,
                "OBSERVED_POLICY_VERSION": observed.get("OBSERVED_POLICY_VERSION") if observed else None,
                "DRIFT": deltas,
                "BLOCKERS": blockers,
                "SAFE_HEALED": healed,
                "RESULT": result,
            })
        except FileExistsError:
            results.append({"PROJECT_ID": pid, "OPERATION_KEY": op_key, "MODE": mode, "RESULT": "BLOCKED", "BLOCKERS": ["CONCURRENCY_LOCKED"]})
        except Exception as exc:
            results.append({"PROJECT_ID": pid, "OPERATION_KEY": op_key, "MODE": mode, "RESULT": "FAILED", "ERROR": str(exc)})
        finally:
            if lock:
                release_lock(lock)

    report = {
        "CONTROL_PLANE_VERSION": desired_doc.get("CONTROL_PLANE_VERSION"),
        "GENERATED_AT": dt.datetime.now(dt.timezone.utc).isoformat(),
        "DRY_RUN": not apply_safe,
        "PROJECTS": sorted(results, key=lambda r: (r.get("ROLLOUT_WAVE", 0), r.get("PROJECT_ID", ""))),
    }
    return report, observed_doc


def append_ledger(ledger: dict, report: dict) -> dict:
    events = ledger.setdefault("EVENTS", [])
    known = {e.get("OPERATION_KEY") for e in events if e.get("RESULT") in {"NOOP", "SAFE_HEALED"}}
    for item in report.get("PROJECTS", []):
        if item.get("OPERATION_KEY") in known:
            continue
        event = dict(item)
        event["TIMESTAMP"] = report.get("GENERATED_AT")
        events.append(event)
    return ledger


def main() -> int:
    ap = argparse.ArgumentParser(description="PCC central desired-vs-observed orchestrator")
    ap.add_argument("--desired", default="orchestration/desired-state.json")
    ap.add_argument("--observed", default="orchestration/observed-state.json")
    ap.add_argument("--ledger", default="orchestration/audit-ledger.json")
    ap.add_argument("--mode", choices=MODES)
    ap.add_argument("--project")
    ap.add_argument("--apply-safe", action="store_true", help="apply only allow-listed PCC-local derived-state repairs")
    ap.add_argument("--record-ledger", action="store_true")
    ap.add_argument("--report-out", default="orchestration-report.json")
    args = ap.parse_args()

    desired_path = Path(args.desired)
    observed_path = Path(args.observed)
    ledger_path = Path(args.ledger)
    desired_doc = load(desired_path)
    observed_doc = load(observed_path)
    report, updated_observed = reconcile(desired_doc, observed_doc, args.mode, args.project, args.apply_safe)

    Path(args.report_out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.apply_safe:
        observed_path.write_text(json.dumps(updated_observed, indent=2) + "\n", encoding="utf-8")
    if args.record_ledger:
        ledger = append_ledger(load(ledger_path), report)
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if any(p.get("RESULT") == "FAILED" for p in report["PROJECTS"]) else 0


if __name__ == "__main__":
    sys.exit(main())
