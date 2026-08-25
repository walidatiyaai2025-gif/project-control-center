# 60 — Register Project

PROMPT_ID: PCC-60
VERSION: 1.1.0
APPLIES_TO: PORTFOLIO_REGISTRATION
PREVIOUS_STEP: PCC-11_OR_PCC-25_OR_PCC-31
NEXT_STEP: PCC-61
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Stable PROJECT_ID/repository URL.
- Lifecycle/control-plane maturity determined by evidence.
- Canonical project status/profile defined or explicitly pending discovery.

## Mission

Create/update exactly one portfolio record and central desired-state enrollment without inventing state.

## Execute

Populate required fields plus version/orchestration fields: PROJECT_ID, DISPLAY_NAME, REPOSITORY, CRITICALITY, LIFECYCLE_STATE, CONTROL_PLANE_MATURITY, CONTROL_PLANE_VERSION, production/integration branches+SHAs, LATEST_RELEASE, CURRENT_PRODUCTION_VERSION, CURRENT_DEVELOPMENT_VERSION, TARGET_DEVELOPMENT_VERSION, NEXT_RELEASE_CANDIDATE, LATEST_USER_REVIEW_CANDIDATE, VERSION_POLICY, VERSION_SOURCE, VERSION_BASELINE_CONFIDENCE, POLICY_ENFORCEMENT_MODE, desired/observed policy versions, DRIFT, HEALTH, PROGRESS, P0/P1/BLOCKED/QA/STALE/WAITING/LAST_SYNC.

Unknown values remain null/UNKNOWN. No Worker estimates as PROGRESS. Reject duplicate project/repo records unless explicit update.

Use verified project profile to plan/enroll desired state. Existing projects normally enter OBSERVE first. Regenerate dashboard projection.

## Required output

Return registry entry, desired-state enrollment/operation key, exact PCC SHA, unknown fields and dashboard visibility.
