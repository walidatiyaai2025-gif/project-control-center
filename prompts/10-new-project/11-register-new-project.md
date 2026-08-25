# 11 — Register New Project

PROMPT_ID: PCC-11
VERSION: 1.1.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-10
NEXT_STEP: PCC-12
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- PCC-10 completed successfully.
- Stable PROJECT_ID and repository URL.
- Managed repository records the control-plane repository/version/SHA.
- Canonical project status and project profile exist.

## Mission

Register/enroll the new project without inventing delivery or version progress.

## Execute

Add exactly one project entry to `portfolio/projects.yml` with all required portfolio fields and version fields: production/integration branches+SHAs, latest release, current production version, current/target development version, next candidate, latest user-review candidate, version policy/source/baseline confidence, enforcement mode, control-plane version, health/progress/P0/P1/blocked/QA/stale/waiting/last sync.

Unknown SHAs/releases/versions remain null. Progress must be evidence-derived; if no approved denominator exists keep it null.

Create/update the PCC desired-state enrollment from the verified project profile in `OBSERVE` mode unless a stronger mode is explicitly justified by evidence. Regenerate/validate dashboard projection.

## Required output

Return registered project record, desired-state enrollment state, exact registry commit SHA, unknown fields, dashboard projection status, and next prompt PCC-12.
