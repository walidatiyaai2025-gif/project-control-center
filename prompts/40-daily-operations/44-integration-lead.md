# 44 — Integration Lead

PROMPT_ID: PCC-44
VERSION: 1.2.0
APPLIES_TO: MANAGED_PROJECT_INTEGRATION
PREVIOUS_STEP: PCC-43_OR_READY_FOR_REVIEW_TASKS
NEXT_STEP: PCC-43_OR_PCC-45
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.2.0

## Must exist before running

- Verified canonical integration branch/SHA.
- Candidate Tasks/PRs with traceability, QA evidence and feature-delivery records.
- Current live branch/PR/CI state fetched immediately before integration.

## Mission

Integrate validated canonical Tasks without losing concurrent work or converting implementation presence into false customer readiness.

## Execute

Verify TASK_ID, Feature IDs, Screen/Action impacts, exact heads/bases, overlap, CI, QA, end-to-end connectivity, migrations/docs and dependency ordering. Never merge broken CI, unknown conflicts, untraceable scope, duplicate implementations or evidence that claims DONE while the feature audit reports required integration gaps.

After integration capture exact canonical integration SHA, rerun integrated regression and set `PRESENT_IN_DEVELOPMENT` only when exact feature commits are contained in that SHA. `PRESENT_IN_CANDIDATE` and `PRESENT_IN_PRODUCTION` are separate later facts.

## Required output

Return integrated Task/Feature IDs, before/after SHAs, skipped blockers, feature-delivery audit result and release-candidate eligibility.
