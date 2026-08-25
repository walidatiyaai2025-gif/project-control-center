# 60 — Register Project

PROMPT_ID: PCC-60
VERSION: 1.0.0
APPLIES_TO: PORTFOLIO_REGISTRATION
PREVIOUS_STEP: PCC-11_OR_PCC-25_OR_PCC-31
NEXT_STEP: PCC-61
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Stable PROJECT_ID and repository URL.
- Lifecycle/control-plane maturity determined by onboarding evidence.
- Canonical project status source defined or explicitly pending discovery.

## Mission

Create/update exactly one portfolio record for the project.

## Execute

Populate all required fields: PROJECT_ID, DISPLAY_NAME, REPOSITORY, CRITICALITY, LIFECYCLE_STATE, CONTROL_PLANE_MATURITY, PRODUCTION_BRANCH, PRODUCTION_SHA, CANONICAL_INTEGRATION_BRANCH, CANONICAL_INTEGRATION_SHA, LATEST_RELEASE, HEALTH, PROGRESS, P0, P1, BLOCKED, QA, STALE, WAITING_FOR_USER, LAST_SYNC.

Do not guess unknown branch/SHA/release values. Do not register Worker estimates as PROGRESS. Reject duplicate PROJECT_ID or repository records unless the action is an explicit update.

Regenerate/validate dashboard projection.

## Required output

Return final registry entry, exact control-center SHA, unknown fields, and dashboard visibility status.
