# 11 — Register New Project

PROMPT_ID: PCC-11
VERSION: 1.0.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-10
NEXT_STEP: PCC-12
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- PCC-10 completed successfully.
- Stable PROJECT_ID and repository URL.
- Managed repository records the control-plane repository/version/SHA.
- Canonical project status path exists.

## Mission

Register the new project in the portfolio without inventing delivery progress.

## Execute

Add exactly one project entry to `portfolio/projects.yml` with all required portfolio fields: PROJECT_ID, DISPLAY_NAME, REPOSITORY, CRITICALITY, LIFECYCLE_STATE, CONTROL_PLANE_MATURITY, production branch/SHA, canonical integration branch/SHA, latest release, HEALTH, PROGRESS, P0, P1, BLOCKED, QA, STALE, WAITING_FOR_USER, LAST_SYNC.

Unknown SHAs/releases remain null. Set maturity according to evidence, normally `MANAGED` only after the onboarding skeleton is actually present. Progress must be evidence-derived from canonical requirements/tasks; if no approved denominator exists, keep it null rather than guessing.

Add/refresh the canonical project status projection and portfolio dashboard data.

## Required output

Return the registered project record, exact registry commit SHA, any null/unknown fields, dashboard projection status, and next prompt PCC-12.
