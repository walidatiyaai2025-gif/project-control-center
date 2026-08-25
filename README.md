# Project Control Center

Central GitHub Portfolio & Software Delivery Control Plane for current, legacy, and future repositories.

**CONTROL_PLANE_VERSION: v1.3.0**

Start with [`START_HERE.md`](START_HERE.md).

## Canonical principles
- Every request maps to a canonical Task ID before implementation.
- Existing projects are discovered before governance is imposed.
- Task identity and canonical task branch survive Worker changes.
- Official builds are produced by controlled CI from immutable SHAs.
- `CODE EXISTS != FEATURE COMPLETE`; PCC v1.2 feature-delivery governance remains authoritative.
- Fleet control is live desired-vs-observed, centrally enrolled, idempotent, concurrency-guarded, failure-isolated and rollout-aware.
- Existing-project baseline locks are read-only evidence anchors; they never justify deleting unique work or guessing development lineage.
- Cross-repository mutation requires explicit write authorization, a write-capable runtime auth provider, resolved lineage, and CANARY/ENFORCE gates.

## Autonomous fleet control
PCC v1.3.0 adds the operational fleet layer documented in [`policies/FLEET_CONTROL_POLICY.md`](policies/FLEET_CONTROL_POLICY.md):
live GitHub collection, central enrollment, discovery/baseline/reconciliation, safe migration and policy sync, drift repair planning, OBSERVE/WARN/CANARY/ENFORCE rollout, stale/orphan recovery, audit ledger, break-glass/exception handling, live portfolio aggregation and GitHub Pages dashboard deployment.

## Feature delivery governance
The accepted v1.2.0 layer remains in [`policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`](policies/END_TO_END_FEATURE_DELIVERY_POLICY.md). It is not replaced by this fleet upgrade.

## First enrolled pilot
`walidatiyaai2025-gif/AIMWWeb` is enrolled centrally as OBSERVE and CANARY-eligible with `WRITE_AUTHORIZED=false`. This fleet closure does not modify AIMWWeb.
