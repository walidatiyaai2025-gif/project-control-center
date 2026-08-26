# 11 — Register New Project

PROMPT_ID: PCC-11
VERSION: 1.2.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-10
NEXT_STEP: PCC-12
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- PCC-10 completed successfully.
- Stable PROJECT_ID and repository URL.
- Project classification/variant normalization evidence exists.
- Managed repository records the control-plane repository/version/SHA.
- Canonical project status/profile and target repository constitution exist.

## Mission

Register/enroll the new project without inventing delivery, variant boundaries, or version progress.

## Execute

Add exactly one project entry to `portfolio/projects.yml` and one aligned routing entry to `portfolio/project-routing.json`.

The routing entry MUST include `PROJECT_MODEL`, `CONSTITUTION_STATE`, `ONBOARDING_NORMALIZATION_STATE`, `VARIANT_GOVERNANCE_STATE`, `CORE_ROUTING_STATE`, and variants where applicable.

For product families, each active variant must declare identity/aliases, implementation-location state and routing state. A `READY` route requires a verified location. Unresolved/unmaterialized variants remain visible and blocked; do not fabricate locations to pass registration.

Create/update desired-state enrollment in `OBSERVE` unless stronger mode is evidence-backed. Unknown SHAs/releases/versions remain null. Progress remains evidence-derived.

## Required output

Return registered project record, routing/variant normalization state, blocked/routable variants, desired-state enrollment, exact registry commit SHA, dashboard projection status, and next prompt PCC-12.
