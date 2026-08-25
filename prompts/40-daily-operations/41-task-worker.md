# 41 — Task Worker

PROMPT_ID: PCC-41
VERSION: 1.4.0
APPLIES_TO: CANONICAL_TASK_IMPLEMENTATION
PREVIOUS_STEP: PCC-40
NEXT_STEP: PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Canonical TASK_ID in READY/CLAIMED/IN_PROGRESS state.
- Duplicate check completed.
- Canonical task branch and verified base SHA identified.
- Acceptance criteria and required validation defined.
- Product-function tasks have FEATURE_ID(s), applicable Screen/Action IDs and Feature Delivery Matrix records.

## Mission
Implement only the assigned canonical Task and prove applicable end-to-end delivery dimensions without representing disconnected code as complete.

## Execute
Confirm branch/Task identity and fetch latest remote state. Claim/refresh the Worker lease. Work only within Task scope. Update canonical feature/screen/action evidence for backend, API, UI, navigation, UI/API/data binding, mutation, permissions, persistence/reload, QA, customer visibility and target version as applicable. Irrelevant dimensions are explicitly NOT_APPLICABLE.

Commit/push traceable changes and run required tests. Never weaken tests, fabricate evidence, use fake production data, or show local success as server-authoritative success. A Worker may not manually return DONE when `scripts/feature_delivery_audit.py` derives an integration-gap state.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return a `WORKER_HANDOFF` compatible with `schemas/worker-handoff.schema.json`: TASK, STATUS, exact HEAD, changed scope, validation, blocker if any, and NEXT_ACTION. Preserve Feature/Screen/connectivity evidence in structured fields. `DONE` alone is forbidden.
