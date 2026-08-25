# 12 — New Project Readiness Audit

PROMPT_ID: PCC-12
VERSION: 1.0.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-11
NEXT_STEP: PCC-40
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- PCC-10 and PCC-11 completed.
- Project appears exactly once in the portfolio registry.
- Managed control marker and canonical status path exist.

## Mission

Decide whether the new project may enter normal task delivery.

## Audit

Verify project identity, control-plane version/SHA, branch model, task/requirement traceability, duplicate-check mechanism, worker lease model, CI gate, QA expectations, release/build identity, secrets/config policy, ADR path, documentation policy, database migration safety where applicable, user acceptance, and Delivery / Control Lead authority.

Confirm there is no coding request without a Task ID and no initial branch/PR that cannot be traced to a canonical task.

If any gate fails, report the exact missing evidence and keep the project below `FULLY_ENFORCED` as appropriate.

## Required output

Return READY/NOT_READY, exact audited project SHA, blocking defects, control-plane maturity recommendation, and, if ready, direct the operator to PCC-40 for task dispatch.
