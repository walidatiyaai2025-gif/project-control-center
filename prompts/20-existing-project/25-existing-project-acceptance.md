# 25 — Existing Project Acceptance

PROMPT_ID: PCC-25
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-24
NEXT_STEP: PCC-40
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Completed discovery, baseline, reconciliation, installation, and enforcement sequence PCC-20 through PCC-24.
- Exact current target-repository SHA and control-plane registry access.

## Mission

Accept the existing project into managed operation only if live development was preserved and governance is functional.

## Audit and update

Verify production/development lineage, unique-work preservation, canonical task mapping, task branch continuity, PR traceability, CI exact-head evidence, QA/release gates, canonical project status, Delivery / Control Lead authority, and control-plane marker/version.

Register or update the project in `portfolio/projects.yml` with truthful maturity. Use `MANAGED` or `FULLY_ENFORCED` only when evidence supports it. Project progress must be derived from canonical scoped work, never Worker estimates.

Run stale/orphan/duplicate checks against the acceptance head. If material unresolved work remains, record it visibly rather than hiding it to pass acceptance.

## Required output

Return ACCEPTED/NOT_ACCEPTED, exact target SHA, production SHA, canonical development SHA, latest release, maturity, health, unresolved risks, portfolio registry SHA, and, if accepted, direct the operator to PCC-40.
