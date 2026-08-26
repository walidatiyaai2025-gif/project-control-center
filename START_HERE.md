# START HERE — Project Control Center v1.5.0

This is the operator entry point. Existing v1.2 Feature/Screen/Action governance, v1.3 fleet governance, v1.4 execution-output discipline, v1.5 fleet onboarding, and current project/client routing governance remain authoritative.

## Before any scenario
1. **Read root `AGENTS.md` first.** It is the PCC constitution for every Manager/Lead/Worker role.
2. Confirm this PCC repository at a known immutable SHA and read `VERSION`.
3. Read `policies/GOVERNANCE_LAWS.md`.
4. Read mandatory `policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md`; operational roles use silent execution by default and report reconciled final state only.
5. For product delivery, read `policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md` and `policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`.
6. For fleet operations, read `policies/FLEET_CONTROL_POLICY.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`, and `orchestration/README.md`.
7. For worker dispatch, read `policies/PROJECT_FAMILY_ROUTING_POLICY.md` and resolve the project/client through `portfolio/project-routing.json`.
8. Never invent branches, SHAs, task state, QA, release, lineage, version, connectivity, client identity, variant identity, or completion.
9. Existing-project discovery/baseline/reconciliation are read-only until an explicit write gate is satisfied.
10. Cross-repository writes require CANARY/ENFORCE + explicit write authorization + write-capable runtime auth + resolved target lineage where those fleet-managed write gates apply.
11. Before bulk enrollment, run `python scripts/fleet_readiness.py`; require `READINESS_PERCENT=100` and `ONBOARDING_READY=true`.

## Manager / Lead mandatory entrypoint

When the owner names a project, client, or variant and asks for work, a Manager/Lead must resolve and package the work before implementation starts. The Manager/Lead owns routing ambiguity and cannot delegate it to the implementation Worker.

Required sequence:

`OWNER REQUEST -> FETCH LIVE PCC -> RESOLVE PROJECT/CLIENT -> FETCH LIVE TARGET -> CLASSIFY SCOPE -> RECONCILE TASK/BRANCH -> ISSUE ROUTING PACKET -> IMPLEMENT -> QA -> INTEGRATE/RELEASE WHEN REQUIRED -> RECONCILE FINAL EVIDENCE`

A replacement Manager/Lead continues the same canonical task and branch where they exist.

## Worker routing — mandatory entrypoint

The owner may name only the project/client/variant. Resolve it before assigning implementation work:

`python scripts/route_work.py --project <project-or-client> [--scope PROJECT|CORE|VARIANT] [--variant <variant>] [--task <task>]`

A worker must receive `ROUTING_STATUS=ROUTED` before implementation writes. It must read the routed repository constitution first. If routing is blocked or repository evidence conflicts with the packet, the worker stops rather than guessing.

For a `PRODUCT_FAMILY`:
- `CORE` means shared behavior and requires validation across all affected active variants.
- `VARIANT` means exactly one routed client/product variant.
- branch names do not define long-lived client identity.

## Fleet onboarding — canonical path
1. Copy `templates/PROJECT_PROFILE.yml` and replace placeholders with repository-specific facts.
2. Add one matching entry to `portfolio/project-routing.json` using `templates/PROJECT_ROUTING.json`.
3. Install a repository-root constitution, normally `AGENTS.md`. For product families also install `.pcc/project-family.json`.
4. Keep `CONSTITUTION_STATE=PENDING` until those target-repository governance files are verified; a new project cannot pass onboarding readiness while pending.
5. Keep a newly added existing project in `OBSERVE`, `WRITE_AUTHORIZED=false`, and `CANONICAL_DEVELOPMENT_LINEAGE=UNRESOLVED` unless verified evidence says otherwise.
6. Run `python scripts/enrollment_controller.py --profile <profile> --apply` to update the PCC registry and desired state only.
7. Run `scripts/fleet_control.py` or `.github/workflows/fleet-control.yml` for live discovery/baseline/reconciliation.
8. Run `python scripts/fleet_readiness.py --live-report <fleet-report>` for fleet-wide onboarding acceptance.
9. Promote a project separately through `OBSERVE -> WARN -> CANARY -> ENFORCE`; never infer write readiness from onboarding readiness.

## Output discipline invariant
Normal operational flow is `READ -> INVESTIGATE -> EXECUTE -> VALIDATE -> RECONCILE EVIDENCE -> REPORT`. Do not stream tool narration or intermediate hypotheses. Exact-head and artifact provenance must be established before authoritative QA/CI/integration/release conclusions. Use the structured handoff schemas under `schemas/` and `scripts/output_discipline.py` where applicable.

## Existing project sequence
`prompts/20-existing-project/20-discover-existing-project.md` → `21-baseline-lock.md` → `22-reconcile-existing-work.md` → `23-install-control-plane.md` → `24-enable-enforcement.md` → `25-existing-project-acceptance.md`

The central fleet collector may perform read-only discovery/baseline/reconciliation evidence gathering. It must preserve unique unmerged work and may not infer canonical development lineage from branch names.

## Fleet operating loop
1. Enroll in `portfolio/projects.yml` using the enrollment controller and add its routing declaration.
2. Run `.github/workflows/fleet-control.yml` or `scripts/fleet_control.py`.
3. Review live collection, baseline, reconciliation, stale recovery, orphan candidates and drift.
4. Stay in OBSERVE/WARN until write prerequisites are satisfied.
5. Advance explicit canaries before ENFORCE.
6. Every repair remains allow-listed and audited.

## Recovery
Prompts `50`–`53` remain the operator workflow for stale/orphan/overlap/full reconciliation. Expired work is reclaimed with the same Task ID, branch and latest pushed SHA.

## Dashboard
`dashboard/` is built from canonical portfolio/observed state and live fleet state. The dashboard workflow also publishes `portfolio/status/readiness.json`. GitHub Pages enablement is an external repository-administration concern and is not allowed to falsify fleet onboarding readiness.

## Feature delivery invariant
The accepted v1.2 invariant remains: `FALSE_DONE_FEATURES = 0`. Use `scripts/feature_delivery_audit.py` and the existing Feature Delivery Matrix / Screen Inventory / Screen Action Matrix; do not recreate them.
