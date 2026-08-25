# START HERE — Project Control Center v1.0.0

This is the operator entry point. You do not need previous chat history. Choose exactly one scenario, open the numbered prompt, satisfy its prerequisites, execute it against the named repository, then follow `NEXT_STEP`.

## Before any scenario

1. Confirm you are operating from `walidatiyaai2025-gif/project-control-center` at a known immutable SHA.
2. Read `policies/GOVERNANCE_LAWS.md`.
3. Never invent a project branch, SHA, task, QA state, release, or percentage.
4. For existing/legacy repositories, discovery is read-only until a prompt explicitly permits writes.
5. Any repository managed by this plane must record this repository and a control-plane version/tag/SHA.

## Choose your scenario

### NEW PROJECT
Run in order:

`prompts/10-new-project/10-initialize-new-project.md`
→ `11-register-new-project.md`
→ `12-new-project-readiness-audit.md`

Use when the product repository is new and there is no live development history to preserve.

### ACTIVE EXISTING PROJECT
Run in order:

`prompts/20-existing-project/20-discover-existing-project.md`
→ `21-baseline-lock.md`
→ `22-reconcile-existing-work.md`
→ `23-install-control-plane.md`
→ `24-enable-enforcement.md`
→ `25-existing-project-acceptance.md`

**Safety rule:** Prompt 20 must inspect remote branches, open/recent PRs, issues, releases/tags, unique commits, CI, QA, and governance files. Never assume `main`, `master`, `develop`, or any integration branch is the current development lineage.

### LEGACY / DORMANT PROJECT
Run:

`prompts/30-legacy-project/30-legacy-inventory.md`
→ `31-archive-or-maintenance.md`

### REACTIVATE LEGACY
Run:

`prompts/30-legacy-project/32-reactivate-project.md`
→ then ACTIVE EXISTING PROJECT sequence `20` through `25`.

## Daily operation after onboarding

- Dispatch work: `40-dispatcher.md`
- Execute a canonical task: `41-task-worker.md`
- Continue/take over abandoned work: `42-continuation-worker.md`
- QA: `43-qa-worker.md`
- Integration: `44-integration-lead.md`
- Release: `45-release-lead.md`
- Final user delivery: `46-user-delivery-lead.md`

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

## Write-access interpretation

Every prompt declares `REQUIRES_WRITE_ACCESS`. `false` means discovery/audit only and forbids repository mutation. `true` means writes are allowed only within the prompt's explicit scope and after prerequisites are satisfied.

## Canonical status rule

Workers report Task-local state only. The **DELIVERY / CONTROL LEAD** is the only role allowed to publish authoritative overall project state. Project-wide progress comes from canonical status evidence, never Worker estimates.

## First pilot

For `walidatiyaai2025-gif/AIMWWeb`, after this control center passes self-audit, the exact first prompt is:

`prompts/20-existing-project/20-discover-existing-project.md`

That prompt is read-only. Do not run Prompt 21 until Prompt 20 has identified the verified live development lineage and its evidence.
