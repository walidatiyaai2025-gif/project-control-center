# 50 — Stale Task Recovery

PROMPT_ID: PCC-50
VERSION: 1.4.0
APPLIES_TO: STALE_OR_RECLAIMABLE_TASK
PREVIOUS_STEP: PCC-40_OR_STALE_DETECTION
NEXT_STEP: PCC-42
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Canonical TASK_ID currently suspected/marked STALE.
- Canonical task branch identity.
- Access to branch, commits, PR, CI, QA, lease history, and current project base lineage.

## Mission
Reclaim stale work instead of recreating it.

## Execute
Fetch the latest pushed task-branch SHA and compare it with project integration/base. Determine whether the branch contains unique work, is already integrated, conflicts with newer work, or has an active PR/CI state. Preserve every unique commit. Expire/release the old Worker lease according to evidence, mark the task RECLAIMABLE, and prepare same-task/same-branch takeover.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return a `WORKER_HANDOFF` with TASK, STATUS, exact HEAD, reconciliation/preserved work under CHANGED, validation/evidence, blocker if any and NEXT_ACTION to PCC-42.
