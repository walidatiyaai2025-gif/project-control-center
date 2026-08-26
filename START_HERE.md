# START HERE — Project Control Center v1.5.0

This is the operator entry point. Existing v1.2 Feature/Screen/Action governance, v1.3 fleet governance and v1.4 execution-output discipline remain authoritative.

## Before any scenario
1. Confirm this PCC repository at a known immutable SHA and read `VERSION`.
2. Read `policies/GOVERNANCE_LAWS.md`.
3. Read mandatory `policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md`; operational roles use silent execution by default and report reconciled final state only.
4. For product delivery, read `policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md` and `policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`.
5. For fleet operations, read `policies/FLEET_CONTROL_POLICY.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`, and `orchestration/README.md`.
6. Never invent branches, SHAs, task state, QA, release, lineage, version, connectivity or completion.
7. Existing-project discovery/baseline/reconciliation are read-only until an explicit write gate is satisfied.
8. Cross-repository writes require CANARY/ENFORCE + explicit write authorization + write-capable runtime auth + resolved target lineage.
9. Before bulk enrollment, run `python scripts/fleet_readiness.py`; require `READINESS_PERCENT=100` and `ONBOARDING_READY=true`.

## Fleet onboarding — canonical path
1. Copy `templates/PROJECT_PROFILE.yml` and replace placeholders with repository-specific facts.
2. Keep a newly added existing project in `OBSERVE`, `WRITE_AUTHORIZED=false`, and `CANONICAL_DEVELOPMENT_LINEAGE=UNRESOLVED` unless verified evidence says otherwise.
3. Run `python scripts/enrollment_controller.py --profile <profile> --apply` to update the PCC registry and desired state only.
4. Run `scripts/fleet_control.py` or `.github/workflows/fleet-control.yml` for live discovery/baseline/reconciliation.
5. Run `python scripts/fleet_readiness.py --live-report <fleet-report>` for fleet-wide onboarding acceptance.
6. Promote a project separately through `OBSERVE -> WARN -> CANARY -> ENFORCE`; never infer write readiness from onboarding readiness.

## Output discipline invariant
Normal operational flow is `READ -> INVESTIGATE -> EXECUTE -> VALIDATE -> RECONCILE EVIDENCE -> REPORT`. Do not stream tool narration or intermediate hypotheses. Exact-head and artifact provenance must be established before authoritative QA/CI/integration/release conclusions. Use the structured handoff schemas under `schemas/` and `scripts/output_discipline.py` where applicable.

## Existing project sequence
`prompts/20-existing-project/20-discover-existing-project.md` → `21-baseline-lock.md` → `22-reconcile-existing-work.md` → `23-install-control-plane.md` → `24-enable-enforcement.md` → `25-existing-project-acceptance.md`

The central fleet collector may perform read-only discovery/baseline/reconciliation evidence gathering. It must preserve unique unmerged work and may not infer canonical development lineage from branch names.

## Fleet operating loop
1. Enroll in `portfolio/projects.yml` using the enrollment controller.
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
