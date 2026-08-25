# 23 — Install Control Plane

PROMPT_ID: PCC-23
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-22
NEXT_STEP: PCC-24
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- PCC-20 discovery, PCC-21 baseline and PCC-22 reconciliation completed.
- Verified development lineage and preservation plan.
- Verified forward version baseline/source decision for product projects, or explicit unresolved status preventing enforcement.
- Write access to target repository and PCC.

## Mission

Install governance into the existing repository without disrupting verified development or historical version identity.

## Execute

Add managed-repository control marker with exact PCC repository/version/SHA; canonical status/task/requirement evidence locations; project profile; traceable PR template; CODEOWNERS where appropriate; ADR/docs/release evidence paths; and validation hooks compatible with the technology.

Integrate on verified live development lineage or a governance branch from its exact SHA. Do not reset to a conventional branch. Reconcile pre-existing governance explicitly.

For product versioning, designate `ONE_CANONICAL_PRODUCT_VERSION_SOURCE` using the baseline decision. Reuse a legitimate stack-native source when selected; create root `VERSION` only when it is the chosen forward source. Reconcile user display/package metadata to derive from or match it. Add version-manifest/reusable-governance integration initially in `OBSERVE`/non-breaking mode for migrated existing projects.

Populate initial status/profile from evidence; unknown stays null/UNKNOWN.

## Required output

Return target branch/base SHA, installation commit/PR, PCC version/SHA, canonical status/profile paths, version source/baseline confidence, initial enforcement mode, preserved-work/history confirmation, and PCC-24.
