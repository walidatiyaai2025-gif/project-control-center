# Central Orchestration Policy

CONTROL_PLANE_VERSION: v1.6.0
POLICY_VERSION: 1.3.0

## Controllers

PCC operates a Repository Enrollment Controller, authenticated GitHub Fleet Collector, Existing-Project Discovery Controller, Baseline Locker, Existing-Work Reconciler, Safe Migration Engine, Policy Version Manager, Drift Detector/Controlled Repair engine, stale-task recovery, orphan audit, Audit Ledger, Portfolio Aggregator, project/client routing controller, onboarding variant-normalization controller, dashboard publisher, and PCC Self-Protection auditor.

## Constitutional decision persistence

Durable operating decisions must be represented in committed PCC constitution/policy and machine-readable state where applicable. Conversation, temporary prompts, and Worker memory are non-canonical inputs.

A current explicit owner instruction may change governance, but the Manager/Lead must persist and validate the amendment before dependent work treats it as durable truth. If that cannot be completed safely, dependent writes stop with `CONSTITUTION_AMENDMENT_PENDING`.

## Manager / Lead controller contract

A Worker assigned the role of Manager, Technical Lead, Integration Lead, Release Lead, Dispatcher, Onboarding Lead, or equivalent coordinator acts as a PCC controller first.

Before implementation is delegated or performed, that role must:

1. fetch live PCC state and read root `AGENTS.md`;
2. resolve the owner-supplied project/client/variant label through the PCC routing registry;
3. verify the target repository constitution, onboarding-normalization state, and family manifest where applicable;
4. fetch live target repository state;
5. determine the exact target scope (`PROJECT`, `CORE`, or `VARIANT`) and change boundary;
6. reconcile/create the canonical Task ID and continuation branch;
7. emit the PCC routing packet to implementation Workers;
8. coordinate non-overlapping work, exact-SHA QA, integration, release/deployment evidence when required, and final reconciliation.

The Manager/Lead owns ambiguity resolution. It must not delegate unresolved project/client/variant identity to an implementation Worker. If routing cannot be established, writes are blocked with `ROUTING_REQUIRED` or `ROUTING_CONFLICT`.

Replacement Managers/Leads inherit the same contract and continue canonical tasks/branches; they do not create parallel management truth.

## Automatic onboarding classification and variant normalization

An owner request to add/register/onboard a repository triggers Manager-owned classification automatically.

The Manager/Lead performs live repository discovery and determines `STANDALONE` versus `PRODUCT_FAMILY`. For families it records each known client/product variant, aliases, relationship, implementation-location state, routing state, and shared-core routing state in both PCC routing state and the target repository family manifest.

Missing physical variant boundaries are preserved explicitly as unresolved/unmaterialized. They are never invented from branch names or convenience. The unresolved boundary is write-blocked while verified siblings may remain routable.

A direct owner onboarding request permits a dedicated governance-only onboarding branch/PR limited to target constitution/control files defined in root `AGENTS.md`. This is distinct from autonomous fleet repair and does not authorize product source, deployment, release publication, force-push, or branch deletion.

## Rollout modes

`OBSERVE -> WARN -> CANARY -> ENFORCE`.

- **OBSERVE**: autonomous fleet collection is live read/compare only. Fleet-managed target repair writes are forbidden.
- **WARN**: live read/compare plus actionable warnings. Fleet-managed target repair writes are forbidden.
- **CANARY**: autonomous fleet writes are possible only for an explicitly enrolled canary, after discovery + baseline + reconciliation, with `WRITE_AUTHORIZED=true`, a resolved canonical lineage, a write-capable runtime credential, no active break-glass, and only allow-listed managed paths.
- **ENFORCE**: the same write gates as CANARY plus project-level enforcement authorization. Product source, branches, tags, releases, databases, and customer artifacts are never rewritten by the fleet controller.

The explicit governance-only onboarding PR authority above does not convert OBSERVE/WARN into autonomous repair modes.

Rollout uses `ROLLOUT_WAVE`; one project failure is isolated and does not abort state collection for the rest of the fleet.

## Cross-repository authentication

Credentials are runtime-only. Supported providers are `github_app`, `token_runtime`, `github_actions`, and `anonymous_public`. Secret values are never committed. Read-only collection must work without write credentials for public repositories. State-changing operations require a provider explicitly marked write-capable.

## Read-before-write gates

Existing repositories must complete all applicable gates before fleet-managed target mutation: live discovery; immutable baseline lock; existing-work reconciliation preserving unique work; resolved canonical lineage where required; explicit write authorization; rollout-mode eligibility; allow-listed path; and no active break-glass freeze.

Unknown state is non-compliant, never silently inferred as compliant.

## Idempotency, concurrency, retries, failure isolation

Operations use deterministic idempotency keys. A completed identical operation is not duplicated. A per-project + operation lock prevents concurrent duplicate mutations. HTTP 429, exhausted-rate-limit 403, and transient 5xx responses use bounded retry/backoff. A repository failure becomes a per-project failure record and does not terminate collection for unrelated projects.

## Drift and controlled repair

Drift is the deterministic difference between desired and observed state. OBSERVE/WARN never repair target repositories autonomously. CANARY/ENFORCE may repair only allow-listed PCC-managed policy/control files and only after all write gates pass. Automatic branch deletion, force-push, tag movement, product-source rewrite, database mutation, and customer-build publishing are forbidden.

## Recovery and orphan law

Expired non-terminal Worker leases are `RECLAIMABLE` using the same `TASK_ID`, same canonical branch, latest pushed SHA, and a replacement Worker. Orphan branches are candidates for investigation only; no automatic deletion is allowed. Unique commits must be reconciled before disposition.

## Audit ledger

Every enrollment, classification/variant-normalization decision, collection, baseline, reconciliation, routing decision, migration plan, policy sync, recovery, constitutional amendment, and exception/break-glass decision receives an operation key, project identity, mode/auth context, result, mutation flag, and timestamp where the applicable controller supports it.

## Break-glass and policy exceptions

Break-glass is a time-bounded automation freeze: while active, fleet-managed writes are blocked and human intervention is required. Policy exceptions are explicit, scoped, expiring records; expired/disabled exceptions have no effect and are always surfaced in audit output.

## PCC self-protection

PCC `main` is expected to require pull-request review, prevent force-push/deletion, and require `Control Plane Validation / self-audit`. `scripts/self_protection.py --apply` can configure this only with a repository-admin, write-capable runtime credential. If the execution environment cannot supply branch-protection admin permission, the final state is an explicit external blocker rather than a false PASS.
