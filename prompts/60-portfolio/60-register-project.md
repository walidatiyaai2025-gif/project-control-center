# 60 — Register Project

PROMPT_ID: PCC-60
VERSION: 1.2.0
APPLIES_TO: PORTFOLIO_REGISTRATION
PREVIOUS_STEP: PCC-11_OR_PCC-25_OR_PCC-31
NEXT_STEP: PCC-61
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- Stable PROJECT_ID/repository URL.
- Lifecycle/control-plane maturity determined by evidence.
- Project classification and onboarding-normalization result.
- Canonical project status/profile defined or explicitly pending discovery.

## Mission

Create/update exactly one portfolio record, one aligned routing record, and central desired-state enrollment without inventing state.

## Execute

Populate portfolio/version/orchestration fields from evidence. Unknown values remain null/UNKNOWN and Worker estimates are not progress.

Create/update `portfolio/project-routing.json` in the same registration operation.

For `STANDALONE`, set family states to `NOT_APPLICABLE`.

For `PRODUCT_FAMILY`, persist active variants/aliases, implementation-location states, routing states, `VARIANT_GOVERNANCE_STATE`, and `CORE_ROUTING_STATE`. `READY` routes require verified locations. Explicit unresolved variants remain visible and blocked rather than fabricated.

Reject duplicate project/repo identities and alias collisions. Existing projects normally enter `OBSERVE` first. Regenerate dashboard projection.

## Required output

Return registry entry, routing/family summary, routable/blocked variants, desired-state operation key, exact PCC SHA, unknown fields, and dashboard visibility.
