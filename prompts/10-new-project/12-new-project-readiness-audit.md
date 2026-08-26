# 12 — New Project Readiness Audit

PROMPT_ID: PCC-12
VERSION: 1.2.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: PCC-11
NEXT_STEP: PCC-40
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- PCC-10 and PCC-11 completed.
- Project appears exactly once in portfolio registry, desired state, and routing registry.
- Managed control marker, canonical status/profile, and repository constitution exist.

## Mission

Decide whether the new project may enter normal task delivery without allowing false variant routing.

## Audit

Verify identity, control-plane version/SHA, task/requirement traceability, CI/QA, release/build identity, secrets/config, ADR/docs, user acceptance authority, and orchestration enrollment.

Verify `ONBOARDING_NORMALIZATION_STATE=READY`.

For `STANDALONE`, variant/core routing states must be `NOT_APPLICABLE`.

For `PRODUCT_FAMILY`, verify family manifest/PCC routing parity, stable active variant identities and aliases, implementation-location/routing states, and shared-core routing state. `PARTIAL` is acceptable only when blocked boundaries are explicitly represented; no Worker may route to them.

Run `python scripts/variant_governance.py`, `python scripts/self_audit.py`, and fleet readiness.

If any gate fails, report exact missing evidence and keep the affected route blocked.

## Required output

Return READY/NOT_READY, exact audited SHA, project/family model, routable/blocked variants, core route state, version/orchestration readiness, blockers, and if ready direct operator to PCC-40.
