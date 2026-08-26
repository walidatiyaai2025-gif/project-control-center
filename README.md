# Project Control Center

Central GitHub Portfolio & Software Delivery Control Plane for current, legacy, and future repositories.

**CONTROL_PLANE_VERSION: v1.5.0**

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
- Fleet onboarding readiness is machine-verifiable and independent from per-project promotion to enforcement.
- Every implementation worker must be routed to the correct repository/product/client boundary before writing code.

## Central project/client worker routing

`policies/PROJECT_FAMILY_ROUTING_POLICY.md` and `portfolio/project-routing.json` make PCC the authoritative dispatcher for standalone projects and product families with client variants.

The owner may provide a project name, client name, variant name, or registered alias. `scripts/route_work.py` resolves it to the canonical repository plus `PROJECT`, `CORE`, or `VARIANT` scope and emits a worker routing packet.

New projects must declare a repository constitution (normally `AGENTS.md`) and, for product families, a machine-readable `.pcc/project-family.json`. A new project with `CONSTITUTION_STATE=PENDING` cannot pass fleet onboarding readiness. Legacy projects may remain visible as `LEGACY_PENDING`, but they are not worker-routable until migrated.

This prevents a worker from accidentally applying one client's customization to another client edition of the same product.

## v1.5 fleet onboarding closure
PCC v1.5.0 adds a fleet-generic onboarding readiness gate in [`scripts/fleet_readiness.py`](scripts/fleet_readiness.py). It validates registry identity, desired-state parity, current templates, onboarding automation, allow-listed safety contracts, project/client routing governance and—when supplied a live fleet report—discovery/baseline/reconciliation for every registered project.

A `READINESS_PERCENT` of `100` with `ONBOARDING_READY=true` means the control plane is ready to register additional projects. It does **not** mean every registered project is ready for CANARY/ENFORCE; project-level drift, lineage and write authorization remain separate promotion gates.

## Execution output discipline
PCC v1.4.0 added [`policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md`](policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md) without replacing fleet, feature-delivery, version, QA, task, audit or portfolio governance. It adds silent execution, exact-head evidence, artifact provenance, Visual QA provenance, contradiction/stale-evidence gates, structured handoff schemas and `scripts/output_discipline.py`.

## Autonomous fleet control
PCC v1.3.0 fleet behavior remains in [`policies/FLEET_CONTROL_POLICY.md`](policies/FLEET_CONTROL_POLICY.md): live GitHub collection, central enrollment, discovery/baseline/reconciliation, safe migration and policy sync, drift planning, OBSERVE/WARN/CANARY/ENFORCE rollout, stale/orphan recovery, audit ledger, break-glass/exception handling and live portfolio aggregation.

## Feature delivery governance
The accepted v1.2.0 layer remains in [`policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`](policies/END_TO_END_FEATURE_DELIVERY_POLICY.md).

## Enrolled repositories
`AIMWWeb` remains centrally enrolled but its repository constitution is legacy-pending for central worker routing. `NotOnlyBook` is enrolled as a product family and routes the `NOTONLYBOOK` and `ARABIASWONDERS` variants through its repository constitution and family manifest.
