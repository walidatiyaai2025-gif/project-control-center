# Project Control Center

Central GitHub Portfolio & Software Delivery Control Plane for current, legacy, and future repositories.

**CONTROL_PLANE_VERSION: v1.4.0**

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
- Operational roles execute silently by default and report only reconciled, evidence-backed final state through structured handoffs.

## Execution output discipline
PCC v1.4.0 adds [`policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md`](policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md) without replacing fleet, feature-delivery, version, QA, task, audit or portfolio governance. It adds silent execution, exact-head evidence, artifact provenance, Visual QA provenance, contradiction/stale-evidence gates, structured handoff schemas and `scripts/output_discipline.py`.

## Autonomous fleet control
PCC v1.3.0 fleet behavior remains in [`policies/FLEET_CONTROL_POLICY.md`](policies/FLEET_CONTROL_POLICY.md): live GitHub collection, central enrollment, discovery/baseline/reconciliation, safe migration and policy sync, drift planning, OBSERVE/WARN/CANARY/ENFORCE rollout, stale/orphan recovery, audit ledger, break-glass/exception handling and live portfolio aggregation.

## Feature delivery governance
The accepted v1.2.0 layer remains in [`policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`](policies/END_TO_END_FEATURE_DELIVERY_POLICY.md).

## First enrolled pilot
`walidatiyaai2025-gif/AIMWWeb` remains centrally enrolled as OBSERVE and CANARY-eligible with `WRITE_AUTHORIZED=false`. PCC v1.4.0 does not modify AIMWWeb.
