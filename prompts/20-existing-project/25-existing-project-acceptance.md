# 25 — Existing Project Acceptance

PROMPT_ID: PCC-25
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-24
NEXT_STEP: PCC-40
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- PCC-20 through PCC-24 completed.
- Exact current target-repository SHA and PCC registry access.

## Mission

Accept the existing project into managed operation only if live development/history was preserved and governance/version controls reflect real evidence.

## Audit and update

Verify production/development lineage, unique-work preservation, canonical tasks/branches, PR traceability, exact-head CI, QA/release gates, canonical project status, Delivery / Control Lead authority, PCC marker/version, project profile, desired-state enrollment and staged enforcement mode.

For customer/user-visible products verify version-baseline evidence/confidence, one designated canonical source, preserved legitimate historical tags/releases, current/target version fields truthfully populated or null, immutable version guard/manifest capability, artifact/tag patterns and user-visible/package version contract. Do not require invented history to pass.

Register/update `portfolio/projects.yml` with truthful maturity/version fields. Run stale/orphan/duplicate and drift checks. Material unresolved work/version drift remains visible.

## Required output

Return ACCEPTED/NOT_ACCEPTED, exact target SHA, production/development SHAs, current production/development versions, latest release, version confidence, orchestration mode, maturity, health, unresolved risks, registry SHA, and if accepted PCC-40.
