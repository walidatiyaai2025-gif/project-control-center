# 53 — Full Project Reconciliation

PROMPT_ID: PCC-53
VERSION: 1.0.0
APPLIES_TO: PROJECT_STATE_DRIFT_OR_DISAGREEMENT
PREVIOUS_STEP: PCC-40_OR_PCC-52_OR_STATUS_CONFLICT
NEXT_STEP: PCC-40_OR_PCC-44_OR_PCC-46
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Managed/partially managed project with conflicting or stale status.
- Read access to all relevant branches, PRs, Issues, CI, QA, releases/tags, canonical task/status records.
- Control-center write access.

## Mission

Reconstruct the current project truth from live evidence and restore one canonical status.

## Execute

Fetch current production/development heads, open/recent PRs, active issues/tasks, branch unique commits, CI at exact heads, QA evidence, releases, stale leases, orphan work, and suspected duplicate work. Compare all of it with the existing canonical status.

Repair traceability/status records without discarding unique implementation. Use PCC-50/51/52 logic where needed. Recompute progress only from canonical scope and evidence. Record discrepancies and their cause.

## Required output

Return reconciled production SHA, canonical integration SHA, latest release, task-state corrections, stale/orphan/duplicate findings, blockers/QA/waiting-for-user, authoritative last-sync timestamp, and the next operational gate.
