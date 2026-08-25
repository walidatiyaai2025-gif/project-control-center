# 45 — Release Lead

PROMPT_ID: PCC-45
VERSION: 1.2.0
APPLIES_TO: MANAGED_PROJECT_RELEASE
PREVIOUS_STEP: PCC-44
NEXT_STEP: PCC-46
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.2.0

## Must exist before running

- Exact canonical integration SHA eligible for release.
- Required CI/QA evidence and immutable version plan.
- Canonical Feature Delivery Matrix/Screen/Action audit for included customer-review scope.
- Controlled CI capable of producing official artifacts.

## Mission

Create and verify an official release from immutable controlled source without labeling branch-only or disconnected functionality customer-visible.

## Execute

Generate official artifacts only from controlled CI at the exact canonical integration SHA. Record workflow/run, product version, artifact/build IDs and checksums. Confirm each included Feature ID's exact commits are present in candidate source before `PRESENT_IN_CANDIDATE=true` and in verified production source before `PRESENT_IN_PRODUCTION=true`.

Block release of required customer-review scope with unresolved `FALSE_DONE_FEATURE`, `IMPLEMENTED_NOT_CONNECTED`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, fake-data path or release identity gap unless an approved exception exists. Record RELEASED_IN_VERSION per feature.

## Required output

Return release/version, source SHA, official artifacts, included Task/Feature IDs, feature-delivery gate result, deployment/production evidence, rollback reference and PCC-46 eligibility.
