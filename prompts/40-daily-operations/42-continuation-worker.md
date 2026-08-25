# 42 — Continuation / Takeover Worker

PROMPT_ID: PCC-42
VERSION: 1.0.0
APPLIES_TO: TASK_CONTINUATION_OR_TAKEOVER
PREVIOUS_STEP: PCC-40_OR_PCC-50
NEXT_STEP: PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Existing canonical TASK_ID.
- Existing canonical task branch or documented reason it cannot be used.
- Latest remote branch/PR/commit evidence.
- Prior Worker lease is expired/released/transferred or takeover is explicitly authorized.

## Mission

Continue abandoned/interrupted work without duplicating implementation.

## Execute

Fetch the same TASK, same canonical branch, and latest pushed SHA. Read prior commits, PR discussion, CI, QA, and handoff notes. Transfer the temporary Worker lease and continue from the strongest valid existing state.

Do not create a fresh implementation branch because the previous Worker disappeared. A replacement branch is last resort and must preserve/port unique work with an explicit reconciliation record.

Revalidate the exact current head before claiming prior evidence still applies.

## Required output

Return TASK_ID, reused branch, takeover-from SHA, current SHA, preserved prior work, new lease owner, remaining acceptance criteria, evidence rerun, and next gate.
