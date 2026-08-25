# 51 — Orphan Recovery

PROMPT_ID: PCC-51
VERSION: 1.4.0
APPLIES_TO: ORPHAN_BRANCH_COMMIT_OR_PR
PREVIOUS_STEP: PCC-40_OR_PCC-53
NEXT_STEP: PCC-41_OR_PCC-42_OR_PCC-53
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Identified branch/commit/PR with missing or incomplete Task traceability.
- Live repository evidence and project requirement/task registry.

## Mission
Recover untraceable work without discarding unique implementation.

## Execute
Inspect origin, commits, authorship, PR/Issue links, changed scope, base lineage, CI/QA, and overlap with canonical tasks. Link the orphan to an existing Task if it is the same logical work; otherwise create a canonical Task only after duplicate check. Select/preserve the strongest implementation lineage. Never retroactively fabricate QA/release evidence.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return a `WORKER_HANDOFF` with mapped TASK, STATUS, exact HEAD, preserved unique work/changed scope, validation, blocker if any and NEXT_ACTION.
