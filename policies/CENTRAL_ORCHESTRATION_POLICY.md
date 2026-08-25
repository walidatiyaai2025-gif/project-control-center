# Central Orchestration Policy

CONTROL_PLANE_VERSION: v1.3.0
POLICY_VERSION: 1.1.0

## Controllers

PCC operates a Repository Enrollment Controller, authenticated GitHub Fleet Collector, Existing-Project Discovery Controller, Baseline Locker, Existing-Work Reconciler, Safe Migration Engine, Policy Version Manager, Drift Detector/Controlled Repair engine, stale-task recovery, orphan audit, Audit Ledger, Portfolio Aggregator, dashboard publisher, and PCC Self-Protection auditor.

## Rollout modes

`OBSERVE -> WARN -> CANARY -> ENFORCE`.

- **OBSERVE**: live read/compare only. Target repository writes are forbidden.
- **WARN**: live read/compare plus actionable warnings. Target repository writes are forbidden.
- **CANARY**: writes are possible only for an explicitly enrolled canary, after discovery + baseline + reconciliation, with `WRITE_AUTHORIZED=true`, a resolved canonical lineage, a write-capable runtime credential, no active break-glass, and only allow-listed managed paths.
- **ENFORCE**: the same write gates as CANARY plus project-level enforcement authorization. Product source, branches, tags, releases, databases, and customer artifacts are never rewritten by the fleet controller.

Rollout uses `ROLLOUT_WAVE`; one project failure is isolated and does not abort state collection for the rest of the fleet.

## Cross-repository authentication

Credentials are runtime-only. Supported providers are `github_app`, `token_runtime`, `github_actions`, and `anonymous_public`. Secret values are never committed. Read-only collection must work without write credentials for public repositories. State-changing operations require a provider explicitly marked write-capable.

## Read-before-write gates

Existing repositories must complete all of the following before any fleet-managed target mutation:

1. live GitHub discovery;
2. immutable read-only baseline lock;
3. existing-work reconciliation preserving unique work;
4. resolved canonical development/integration lineage when a write mode requires it;
5. explicit project write authorization;
6. rollout-mode eligibility;
7. allow-listed migration path;
8. no active break-glass freeze.

Unknown state is non-compliant, never silently inferred as compliant.

## Idempotency, concurrency, retries, failure isolation

Operations use deterministic idempotency keys. A completed identical operation is not duplicated. A per-project + operation lock prevents concurrent duplicate mutations. HTTP 429, exhausted-rate-limit 403, and transient 5xx responses use bounded retry/backoff. A repository failure becomes a per-project failure record and does not terminate collection for unrelated projects.

## Drift and controlled repair

Drift is the deterministic difference between desired and observed state. OBSERVE/WARN never repair target repositories. CANARY/ENFORCE may repair only allow-listed PCC-managed policy/control files and only after all write gates pass. Automatic branch deletion, force-push, tag movement, product-source rewrite, database mutation, and customer-build publishing are forbidden.

## Recovery and orphan law

Expired non-terminal Worker leases are `RECLAIMABLE` using the same `TASK_ID`, same canonical branch, latest pushed SHA, and a replacement Worker. Orphan branches are candidates for investigation only; no automatic deletion is allowed. Unique commits must be reconciled before disposition.

## Audit ledger

Every enrollment, collection, baseline, reconciliation, migration plan, policy sync, recovery, and exception/break-glass decision receives an operation key, project identity, mode/auth context, result, mutation flag, and timestamp. GitHub Actions runtime ledgers are uploaded as immutable run artifacts; canonical seed events remain in `orchestration/audit-ledger.json`.

## Break-glass and policy exceptions

Break-glass is a time-bounded automation freeze: while active, fleet-managed writes are blocked and human intervention is required. Policy exceptions are explicit, scoped, expiring records; expired/disabled exceptions have no effect and are always surfaced in audit output.

## PCC self-protection

PCC `main` is expected to require pull-request review, prevent force-push/deletion, and require `Control Plane Validation / self-audit`. `scripts/self_protection.py --apply` can configure this only with a repository-admin, write-capable runtime credential. If the execution environment cannot supply branch-protection admin permission, the final state is an explicit external blocker rather than a false PASS.
