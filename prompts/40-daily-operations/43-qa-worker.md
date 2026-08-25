# 43 — QA Worker

PROMPT_ID: PCC-43
VERSION: 1.2.0
APPLIES_TO: TASK_OR_RELEASE_CANDIDATE_QA
PREVIOUS_STEP: PCC-41_OR_PCC-42_OR_PCC-44
NEXT_STEP: PCC-44_OR_RETURN_TO_TASK
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.2.0

## Must exist before running

- TASK_ID or release-candidate scope.
- Exact immutable SHA/build identity under test.
- Acceptance criteria, Feature Delivery Matrix, applicable Screen Inventory/Action Matrix and regression scope.
- Environment/test prerequisites.

## Mission

Produce reproducible QA evidence bound to the exact candidate and verify actual connectivity, not isolated component existence.

## Execute

For customer-facing functions verify: reachable screen; visible/enabled action; correct permission; real production service/API path; authoritative data; mutation request; server business rule; persistence; authoritative reconciliation/reload; truthful failure handling; localization/responsiveness/accessibility where applicable; and official candidate presence when required. Verify loading/empty/error/retry states.

Classify failures as product defect, test-harness issue, environment issue or unresolved. Never weaken assertions. A pass from another SHA/build is not reusable without justified equivalence.

## Required output

Return exact SHA/build, checks, Feature/Screen/Action connectivity evidence, persistence/reload result, integration-gap findings, PASS/FAIL per criterion, and `QA_PASS` only if all applicable gates pass. Do not publish project-wide status.
