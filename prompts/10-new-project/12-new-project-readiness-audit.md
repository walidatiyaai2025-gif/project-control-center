# 12 — New Project Readiness Audit

PROMPT_ID: PCC-12
VERSION: 1.1.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-11
NEXT_STEP: PCC-40
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- PCC-10 and PCC-11 completed.
- Project appears exactly once in portfolio registry/desired state.
- Managed control marker, canonical status and project profile exist.

## Mission

Decide whether the new project may enter normal task delivery.

## Audit

Verify identity, control-plane version/SHA, branch model, task/requirement traceability, duplicate-check, worker lease, CI/QA, release/build identity, secrets/config, ADR/docs, database migration safety where applicable, user acceptance, Delivery / Control Lead authority, and central orchestration enrollment.

For customer/user-visible products verify one canonical version source, valid starting version, display/endpoint policy, tag/artifact patterns, Task target-version fields, version manifest path/workflow and immutable version guard. Confirm no official/reviewable anonymous artifact path exists.

If any gate fails, report exact missing evidence and keep maturity/enforcement below the unsupported state.

## Required output

Return READY/NOT_READY, exact audited project SHA, version/orchestration readiness, blocking defects, maturity recommendation, and, if ready, direct operator to PCC-40.
