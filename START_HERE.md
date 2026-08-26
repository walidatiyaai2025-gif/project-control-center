# START HERE — Project Control Center v1.6.0

This is the operator entry point. Existing Feature/Screen/Action governance, fleet governance, execution-output discipline, fleet onboarding, Manager/Lead routing, constitutional decision persistence, and emergency production incident governance remain authoritative.

## Before any scenario
1. **Read root `AGENTS.md` first.** It is the PCC constitution for every Manager/Lead/Worker role.
2. Confirm this PCC repository at a known immutable SHA and read `VERSION`.
3. Read `policies/GOVERNANCE_LAWS.md`.
4. Read `policies/CONSTITUTIONAL_DECISION_AND_VARIANT_ONBOARDING_POLICY.md` for durable decisions and automatic project-family normalization.
5. If the request is a production emergency or the owner says `مشكلة طارئة`, read `policies/EMERGENCY_PRODUCTION_INCIDENT_POLICY.md` and use the production-incident schema/template.
6. Read mandatory `policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md`; operational roles use silent execution by default and report reconciled final state only.
7. For product delivery, read `policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md` and `policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`.
8. For fleet operations, read `policies/FLEET_CONTROL_POLICY.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`, and `orchestration/README.md`.
9. For worker dispatch, read `policies/PROJECT_FAMILY_ROUTING_POLICY.md` and resolve the project/client through `portfolio/project-routing.json`.
10. Never invent branches, SHAs, task state, incident state, QA, release, lineage, version, connectivity, client identity, variant identity, implementation locations, or completion.
11. Existing-project discovery/baseline/reconciliation are read-only until an explicit write gate is satisfied.
12. Cross-repository product writes require the normal authorization gates. A direct owner instruction to add/onboard a project authorizes only governance-only onboarding changes defined in the constitution/policy.
13. Before bulk enrollment, run `python scripts/fleet_readiness.py`; require `READINESS_PERCENT=100` and `ONBOARDING_READY=true`.

## Constitutional decision rule

A durable decision made during a conversation is not complete merely because the Manager/Lead stated it. It must be persisted to the appropriate PCC constitution/policy and machine-readable state, validated by CI, and merged before a replacement Lead can be expected to enforce it.

`CONVERSATION -> DECISION -> CONSTITUTION/POLICY -> MACHINE STATE (when applicable) -> CI -> MAIN`

## Manager / Lead mandatory entrypoint

When the owner names a project, client, or variant and asks for work, a Manager/Lead must resolve and package the work before implementation starts. The Manager/Lead owns routing ambiguity and cannot delegate it to the implementation Worker.

Required sequence:

`OWNER REQUEST -> FETCH LIVE PCC -> RESOLVE PROJECT/CLIENT -> FETCH LIVE TARGET -> CLASSIFY SCOPE -> RECONCILE TASK/BRANCH -> ISSUE ROUTING PACKET -> IMPLEMENT -> QA -> INTEGRATE/RELEASE WHEN REQUIRED -> RECONCILE FINAL EVIDENCE`

A replacement Manager/Lead continues the same canonical task and branch where they exist.

## Emergency production incident path

The owner marker `مشكلة طارئة` (or equivalent explicit production-emergency wording) activates the emergency path.

The Manager/Lead still resolves the exact project/variant and live production lineage first, then may prioritize the narrowest safe service-restoration action.

Canonical sequence:

`EMERGENCY -> LIVE PRODUCTION BASE -> ROUTED INCIDENT -> TEMPORARY MITIGATION WHEN NEEDED -> SERVICE_RESTORED_TEMPORARY -> INCIDENT RECORD -> PERMANENT FIX TASK -> TARGET VERSION/RELEASE -> REGRESSION EVIDENCE -> RELEASE GATE -> CLOSED`

Rules:
- `SERVICE_RESTORED_TEMPORARY != DONE`.
- One incident keeps one `INCIDENT_ID`; Workers/Managers may change but identity does not.
- Persist the project record at `.pcc/incidents/<INCIDENT_ID>.json` using `templates/PRODUCTION_INCIDENT.json` and validate with `scripts/incident_governance.py`.
- If `PERMANENT_FIX_REQUIRED=true`, register a permanent-fix Task and target version or `NEXT_RELEASE` before claiming the incident is fully tracked.
- Every later Release Lead must enumerate open incidents and carry-forward decisions in `OPEN_PRODUCTION_INCIDENTS` and `INCIDENT_CARRY_FORWARD`.
- A deferral moves the target; it does not close the incident.
- Permanent closure requires root-cause confirmation, permanent-fix SHA, required regression evidence, and cleared release gate.

## Worker routing — mandatory entrypoint

The owner may name only the project/client/variant. Resolve it before assigning implementation work:

`python scripts/route_work.py --project <project-or-client> [--scope PROJECT|CORE|VARIANT] [--variant <variant>] [--task <task>]`

A worker must receive `ROUTING_STATUS=ROUTED` before implementation writes. It must read the routed repository constitution first. If routing is blocked or repository evidence conflicts with the packet, the worker stops rather than guessing.

For a `PRODUCT_FAMILY`:
- `CORE` requires `CORE_ROUTING_STATE=READY` and cross-variant validation.
- `VARIANT` requires the selected variant `ROUTING_STATE=READY`.
- unresolved variants remain registered/visible but cannot receive implementation writes.
- branch names do not define long-lived client identity.

## Fleet onboarding — canonical path
1. Fetch the live repository and perform classification/variant discovery before deciding the routing model.
2. Decide `STANDALONE` vs `PRODUCT_FAMILY` from evidence and owner-declared identities.
3. For a family, map each known variant/client, aliases, implementation-location state, routing state, and shared-core state. Never invent missing locations.
4. Copy `templates/PROJECT_PROFILE.yml` and replace placeholders with repository-specific facts.
5. Add one matching entry to `portfolio/project-routing.json` using `templates/PROJECT_ROUTING.json`.
6. Install/reconcile a repository-root constitution, normally `AGENTS.md`. For product families also install `.pcc/project-family.json` using `templates/PROJECT_FAMILY.json`.
7. Set `ONBOARDING_NORMALIZATION_STATE=READY` only after classification is evidence-backed. A family may be `VARIANT_GOVERNANCE_STATE=PARTIAL` when some declared variants are intentionally blocked/unresolved; those boundaries must not route.
8. Keep `CONSTITUTION_STATE=PENDING` until target-repository governance files are verified.
9. Keep a newly added existing project in `OBSERVE`, `WRITE_AUTHORIZED=false`, and `CANONICAL_DEVELOPMENT_LINEAGE=UNRESOLVED` unless verified evidence says otherwise.
10. Run `python scripts/enrollment_controller.py --profile <profile> --apply` to update the PCC registry and desired state only.
11. Run `scripts/fleet_control.py` or `.github/workflows/fleet-control.yml` for live discovery/baseline/reconciliation.
12. Run `python scripts/self_audit.py` and `python scripts/fleet_readiness.py --live-report <fleet-report>` for acceptance.
13. Promote a project separately through `OBSERVE -> WARN -> CANARY -> ENFORCE`; never infer product-write readiness from onboarding readiness.

## Output discipline invariant
Normal operational flow is `READ -> INVESTIGATE -> EXECUTE -> VALIDATE -> RECONCILE EVIDENCE -> REPORT`. Do not stream tool narration or intermediate hypotheses. Exact-head and artifact provenance must be established before authoritative QA/CI/integration/release conclusions. Use the structured handoff schemas under `schemas/` and `scripts/output_discipline.py` where applicable.

## Existing project sequence
`prompts/20-existing-project/20-discover-existing-project.md` → `21-baseline-lock.md` → `22-reconcile-existing-work.md` → `23-install-control-plane.md` → `24-enable-enforcement.md` → `25-existing-project-acceptance.md`

The central fleet collector may perform read-only discovery/baseline/reconciliation evidence gathering. It must preserve unique unmerged work and may not infer canonical development lineage or client identity from branch names.

## Fleet operating loop
1. Enroll in `portfolio/projects.yml` and `portfolio/project-routing.json` after classification/normalization.
2. Run `.github/workflows/fleet-control.yml` or `scripts/fleet_control.py`.
3. Review live collection, baseline, reconciliation, variant-routing blockers, stale recovery, orphan candidates and drift.
4. Stay in OBSERVE/WARN until write prerequisites are satisfied.
5. Advance explicit canaries before ENFORCE.
6. Every repair remains allow-listed and audited.

## Recovery
Prompts `50`–`53` remain the operator workflow for stale/orphan/overlap/full reconciliation. Expired work is reclaimed with the same Task ID, branch and latest pushed SHA. Production incidents similarly continue with the same `INCIDENT_ID` and evidence chain.

## Dashboard
`dashboard/` is built from canonical portfolio/observed state and live fleet state. The dashboard workflow also publishes `portfolio/status/readiness.json`. GitHub Pages enablement is an external repository-administration concern and is not allowed to falsify fleet onboarding readiness.

## Feature delivery invariant
The accepted invariant remains: `FALSE_DONE_FEATURES = 0`. Use `scripts/feature_delivery_audit.py` and the existing Feature Delivery Matrix / Screen Inventory / Screen Action Matrix; do not recreate them.
