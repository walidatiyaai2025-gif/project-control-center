# 41 — Task Worker

PROMPT_ID: PCC-41
VERSION: 1.2.0
APPLIES_TO: CANONICAL_TASK_IMPLEMENTATION
PREVIOUS_STEP: PCC-40
NEXT_STEP: PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.2.0

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

## Required output

Return TASK, FEATURE, SCREENS AFFECTED, BACKEND STATUS, API STATUS, UI STATUS, NAVIGATION STATUS, UI/API BINDING STATUS, PERSISTENCE STATUS, QA STATUS, CUSTOMER VISIBLE, TARGET VERSION, CURRENT HEAD, NEXT GAP, and the derived feature state. `DONE` alone is forbidden.
