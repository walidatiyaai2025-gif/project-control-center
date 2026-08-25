# 43 — QA Worker

PROMPT_ID: PCC-43
VERSION: 1.1.0
APPLIES_TO: TASK_OR_RELEASE_CANDIDATE_QA
PREVIOUS_STEP: PCC-41_OR_PCC-42_OR_PCC-44
NEXT_STEP: PCC-44_OR_RETURN_TO_TASK
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- TASK_ID or release-candidate scope.
- Exact immutable SHA/build identity under test.
- Acceptance criteria/regression scope and environment prerequisites.
- For review/release candidates: product version/build ID and version-display/package expectations.

## Mission

Produce reproducible QA evidence bound to the exact candidate SHA/build/version.

## Execute

Validate acceptance criteria, affected regression paths, error/loading/empty states, localization/responsiveness/accessibility, data integrity and permitted production-like integration behavior.

For customer/review candidates, verify the presented version matches the candidate's canonical version source/package metadata where the project profile requires it; report mismatch as `VERSION_DRIFT`. Verify the artifact/build under QA has the expected version/build identity, not an anonymous `latest/final` identity.

Classify failure as product defect, test-harness, environment, version-drift or unresolved. Never weaken assertions. A pass from another SHA/build/version is not reusable without justified equivalence.

Update only QA/task evidence.

## Required output

Return exact SHA, PRODUCT_VERSION/BUILD_ID when applicable, checks, PASS/FAIL per criterion, version identity result, defects with Task IDs, regression result and QA_PASS only if required gates pass.
