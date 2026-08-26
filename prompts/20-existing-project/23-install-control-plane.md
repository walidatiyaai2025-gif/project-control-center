# 23 — Install Control Plane

PROMPT_ID: PCC-23
VERSION: 1.2.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-22
NEXT_STEP: PCC-24
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- PCC-20 discovery, PCC-21 baseline and PCC-22 reconciliation completed.
- Verified preservation plan and project-model/variant discovery result.
- Verified forward version baseline or explicit unresolved status preventing unsupported enforcement.
- Write access to target repository and PCC.

## Mission

Install governance without disrupting verified development and persist the automatic variant-routing model.

## Execute

Install/reconcile root `AGENTS.md`, managed-repository control marker, canonical status/task/requirement evidence, profile, traceable PR template/CODEOWNERS where appropriate, and validation hooks.

For `PRODUCT_FAMILY`, install/reconcile `.pcc/project-family.json` from the canonical schema/template. Record each known variant's implementation-location and routing states. Never create product directories, permanent client branches, or copied code merely to make a route look ready.

Mirror the target family model in `portfolio/project-routing.json`. Set `ONBOARDING_NORMALIZATION_STATE=READY` when classification is complete; use `VARIANT_GOVERNANCE_STATE=PARTIAL` if one or more known boundaries are explicitly blocked.

The owner's onboarding authorization is governance-only. Any product source change requires a separate routed Task ID.

Integrate governance on verified lineage or a dedicated governance branch from its exact SHA; reconcile existing governance explicitly.

## Required output

Return target branch/base SHA, governance installation commit/PR, project model, family/variant route states, PCC version/SHA, status/profile paths, preserved-work confirmation, and PCC-24.
