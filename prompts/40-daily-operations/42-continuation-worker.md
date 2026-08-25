# 42 — Continuation / Takeover Worker

PROMPT_ID: PCC-42
VERSION: 1.4.0
APPLIES_TO: TASK_CONTINUATION_OR_TAKEOVER
PREVIOUS_STEP: PCC-40_OR_PCC-50
NEXT_STEP: PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Existing canonical TASK_ID.
- Existing canonical task branch or documented reason it cannot be used.
- Latest remote branch/PR/commit evidence.
- Prior Worker lease is expired/released/transferred or takeover is explicitly authorized.

## Mission
Continue abandoned/interrupted work without duplicating implementation.

## Execute
Fetch the same TASK, same canonical branch, and latest pushed SHA. Read prior commits, PR discussion, CI, QA, and handoff notes. Transfer the temporary Worker lease and continue from the strongest valid existing state. Do not create a fresh implementation branch because the previous Worker disappeared. Revalidate the exact current head before claiming prior evidence still applies.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return a `WORKER_HANDOFF` with TASK, STATUS, exact current HEAD, preserved prior work/changed scope, evidence rerun, blocker if any and NEXT_ACTION.
