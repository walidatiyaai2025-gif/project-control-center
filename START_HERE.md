# START HERE — Project Control Center v1.1.0

This is the operator entry point. You do not need previous chat history. Choose exactly one scenario, open the numbered prompt, satisfy its prerequisites, execute it against the named repository, then follow `NEXT_STEP`.

## Before any scenario

1. Confirm you are operating from `walidatiyaai2025-gif/project-control-center` at a known immutable SHA.
2. Read `policies/GOVERNANCE_LAWS.md`.
3. For customer/user-visible software, read `policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md`.
4. For central enrollment/rollout, read `policies/CENTRAL_ORCHESTRATION_POLICY.md` and `orchestration/README.md`.
5. Never invent a project branch, SHA, task, QA state, release, version, or percentage.
6. For existing/legacy repositories, discovery is read-only until a prompt explicitly permits writes.
7. Any repository managed by this plane must record this repository and a control-plane version/tag/SHA.

`CONTROL_PLANE_VERSION` in a prompt records the control-plane version in which that prompt was last materially defined. Unchanged compatible prompts may retain an older prompt compatibility marker; managed repositories always record the exact PCC version/SHA actually installed.

## Choose your scenario

### NEW PROJECT
Run in order:

`prompts/10-new-project/10-initialize-new-project.md`
→ `11-register-new-project.md`
→ `12-new-project-readiness-audit.md`

Use when the product repository is new and there is no live development history to preserve. Product projects establish one canonical version source during initialization, normally beginning at `0.1.0` unless another starting version is justified.

### ACTIVE EXISTING PROJECT
Run in order:

`prompts/20-existing-project/20-discover-existing-project.md`
→ `21-baseline-lock.md`
→ `22-reconcile-existing-work.md`
→ `23-install-control-plane.md`
→ `24-enable-enforcement.md`
→ `25-existing-project-acceptance.md`

**Safety rule:** Prompt 20 must inspect remote branches, open/recent PRs, issues, releases/tags, unique commits, CI, QA, governance files, and perform **VERSION BASELINE DISCOVERY**. Never assume `main`, `master`, `develop`, or any integration branch is the current development lineage. Never invent a historical product version. Enforcement advances through OBSERVE → WARN → CANARY → ENFORCE after baseline evidence exists.

### LEGACY / DORMANT PROJECT
Run:

`prompts/30-legacy-project/30-legacy-inventory.md`
→ `31-archive-or-maintenance.md`

### REACTIVATE LEGACY
Run:

`prompts/30-legacy-project/32-reactivate-project.md`
→ then ACTIVE EXISTING PROJECT sequence `20` through `25`, including version-baseline discovery.

## Daily operation after onboarding

- Dispatch work: `40-dispatcher.md`
- Execute a canonical task: `41-task-worker.md`
- Continue/take over abandoned work: `42-continuation-worker.md`
- QA: `43-qa-worker.md`
- Integration: `44-integration-lead.md`
- Release: `45-release-lead.md`
- Final user delivery: `46-user-delivery-lead.md`

Customer-impacting tasks carry `TARGET_VERSION`. Official/reviewable releases must pass the immutable product version gate and produce a version manifest.

## Recovery

- Stale task: `50-stale-task-recovery.md`
- Orphan branch/commit/PR: `51-orphan-recovery.md`
- Suspected duplicated work: `52-overlap-audit.md`
- Project state disagreement/drift: `53-full-reconciliation.md`

## Portfolio control

- Register project: `60-register-project.md`
- Audit portfolio: `61-portfolio-audit.md`
- Set cross-project priority: `62-priority-controller.md`
- Publish executive status: `63-executive-status.md`

## Central orchestration

After project discovery/onboarding has produced a verified project profile, central orchestration may enroll desired state and compare it to observed state. Default mode is `OBSERVE`. `WARN` is non-mutating. `CANARY` and `ENFORCE` require explicit readiness and baseline gates. Use `scripts/enrollment_controller.py` for PCC-local enrollment planning and `.github/workflows/central-orchestrator.yml` for controlled desired-vs-observed runs. Neither authorizes arbitrary product-repository writes.

## Write-access interpretation

Every prompt declares `REQUIRES_WRITE_ACCESS`. `false` means discovery/audit only and forbids repository mutation. `true` means writes are allowed only within the prompt's explicit scope and after prerequisites are satisfied.

## Canonical status and delivery rule

Workers report Task-local state only. The **DELIVERY / CONTROL LEAD** is the only role allowed to publish authoritative overall project state. Project-wide progress comes from canonical status evidence, never Worker estimates.

Official customer/reviewable delivery must identify project, product version, build ID, source SHA, CI/QA status, what changed, and what the user should verify. Anonymous authoritative builds such as `latest.apk`, `final.zip`, or `new.exe` are forbidden by `IMMUTABLE_PRODUCT_VERSION_POLICY`.

## First pilot

For `walidatiyaai2025-gif/AIMWWeb`, after this control center passes self-audit, the exact first prompt is:

`prompts/20-existing-project/20-discover-existing-project.md`

That prompt is read-only and now includes VERSION BASELINE DISCOVERY. Do not run Prompt 21 until Prompt 20 has identified the verified live development lineage and the real existing version state with confidence/unknowns documented.
