# 53 — Full Project Reconciliation

PROMPT_ID: PCC-53
VERSION: 1.4.0
APPLIES_TO: PROJECT_STATE_DRIFT_OR_DISAGREEMENT
PREVIOUS_STEP: PCC-40_OR_PCC-52_OR_STATUS_CONFLICT
NEXT_STEP: PCC-40_OR_PCC-44_OR_PCC-46
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Managed/partially managed project with conflicting or stale status.
- Read access to all relevant branches, PRs, Issues, CI, QA, releases/tags, canonical task/status records.
- Control-center write access.

## Mission
Reconstruct the current project truth from live evidence and restore one canonical status.

## Execute
Fetch current production/development heads, open/recent PRs, active issues/tasks, branch unique commits, CI at exact heads, QA evidence, releases, stale leases, orphan work, and suspected duplicate work. Compare all of it with the existing canonical status. Repair traceability/status records without discarding unique implementation. Resolve contradictory signals before publishing state.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return reconciled production/integration exact SHAs, latest release, task-state corrections, stale/orphan/duplicate findings, blockers/QA/waiting-for-user, authoritative last-sync timestamp, evidence and NEXT_ACTION. No investigation diary.
