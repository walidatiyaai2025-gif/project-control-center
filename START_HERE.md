# START HERE — Project Control Center v1.2.0

This is the operator entry point. You do not need previous chat history. Choose one scenario, open the numbered prompt, satisfy prerequisites, execute it against the named repository, then follow `NEXT_STEP`.

## Before any scenario

1. Confirm `walidatiyaai2025-gif/project-control-center` at a known immutable SHA.
2. Read `policies/GOVERNANCE_LAWS.md`.
3. For customer/user-visible software, read `policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md` and `policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`.
4. For central enrollment/rollout, read `policies/CENTRAL_ORCHESTRATION_POLICY.md` and `orchestration/README.md`.
5. Never invent branch, SHA, task, QA state, release, product version, feature connectivity or completion percentage.
6. Existing/legacy discovery is read-only until a prompt explicitly permits writes.
7. Managed repositories record this PCC repository and exact control-plane version/tag/SHA.

`CONTROL_PLANE_VERSION` in a prompt records the PCC version in which that prompt was last materially defined. Compatible unchanged prompts may retain an older marker.

## NEW PROJECT

`prompts/10-new-project/10-initialize-new-project.md` → `11-register-new-project.md` → `12-new-project-readiness-audit.md`

Product projects establish one canonical version source and, before product-function Tasks are considered DONE, canonical Feature Delivery Matrix, Screen Inventory and Screen Action Matrix locations.

## ACTIVE EXISTING PROJECT

`prompts/20-existing-project/20-discover-existing-project.md` → `21-baseline-lock.md` → `22-reconcile-existing-work.md` → `23-install-control-plane.md` → `24-enable-enforcement.md` → `25-existing-project-acceptance.md`

Prompt 20 must inspect live branches/PRs/issues/releases/tags/unique commits/CI/QA/governance and perform VERSION BASELINE DISCOVERY. Never invent historical versions or development lineage. End-to-end feature governance is installed in-place after reconciliation; it must not rewrite valid existing product history.

## LEGACY / DORMANT / REACTIVATION

Use prompts `30` → `31`; use `32` then the Existing Project sequence to reactivate.

## Daily operation after onboarding

- Dispatch: `40-dispatcher.md`
- Task Worker: `41-task-worker.md`
- Continuation: `42-continuation-worker.md`
- QA: `43-qa-worker.md`
- Integration: `44-integration-lead.md`
- Release: `45-release-lead.md`
- User Delivery: `46-user-delivery-lead.md`

For product functionality, Workers must update Feature/Screen/Action evidence. `DONE` is derived; code or screen presence alone is not completion. Customer-impacting tasks carry `TARGET_VERSION`; official releases pass immutable version and end-to-end feature gates.

## Feature delivery governance

Canonical customer-facing traceability is:

FEATURE / REQUIREMENT → SCREEN(S) → ACTION(S) → SERVICE/API → DATA/PERSISTENCE → TASK(S) → PR(S) → VERSION → CUSTOMER BUILD.

Use `scripts/feature_delivery_audit.py` or `.github/workflows/reusable-feature-delivery-governance.yml`. Required project records are based on `templates/FEATURE_DELIVERY_MATRIX.yml`, `templates/SCREEN_INVENTORY.yml`, and `templates/SCREEN_ACTION_MATRIX.yml`.

The target invariant is `FALSE_DONE_FEATURES = 0`. `IMPLEMENTED_NOT_CONNECTED`, `BACKEND_ONLY`, `UI_ONLY`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, fake-data paths, and official-build gaps do not count as customer-ready completion.

## Recovery

Use prompts `50`–`53` for stale/orphan/overlap/full reconciliation.

## Portfolio control

Use prompts `60`–`63`. Executive status separates CODE COMPLETION, CONNECTIVITY COMPLETION, QA COMPLETION, CUSTOMER READY COMPLETION and RELEASE COMPLETION and exposes false-DONE/integration-gap counts.

## Central orchestration

After verified project profile/onboarding, desired-vs-observed orchestration defaults to OBSERVE and advances only through evidence-backed WARN/CANARY/ENFORCE gates. It does not authorize arbitrary product-repository writes.

## Authority

Workers report Task/Feature-local state only. The DELIVERY / CONTROL LEAD alone publishes authoritative overall project/user status.

## First pilot

For `walidatiyaai2025-gif/AIMWWeb`, the first prompt remains read-only `prompts/20-existing-project/20-discover-existing-project.md`. This PCC add-on itself does not modify AIMWWeb.
