# Autonomous Fleet Control Policy

CONTROL_PLANE_VERSION: v1.3.0
POLICY_VERSION: 1.1.0

## Scope
This policy extends the existing PCC control plane with live cross-repository collection, enrollment, discovery, immutable read-only baseline locking, reconciliation, controlled migration, policy sync, drift handling, fleet rollout, stale/orphan recovery, portfolio aggregation, dashboard publication, and PCC self-protection.

It does not replace the v1.2.0 End-to-End Feature Delivery Governance.

## Authentication abstraction
Credential material is runtime-only. Supported providers are `github_app`, `token_runtime`, `github_actions`, and `anonymous_public`. A provider must explicitly be write-capable before cross-repository mutation is possible.

## Live collection
The collector must paginate branches, pull requests, issues, releases and tags; capture default branch identity, protection state, recent Actions runs, and managed governance-file presence. HTTP 429, 5xx, and exhausted rate limits are retried with bounded exponential/reset-aware backoff. One repository failure is isolated from the rest of the fleet.

## Enrollment
Enrollment is centralized in PCC. `PROJECT_ID + REPOSITORY` identity is stable. Re-enrolling the same record is a NOOP. A conflicting repository for an existing PROJECT_ID is blocked.

## Existing-project discovery and baseline
Existing projects are read before write. Baseline locking captures immutable observation anchors: default branch/SHA, branch inventory fingerprint/count, open PR heads/bases, releases/tags and governance evidence. A baseline never selects or rewrites a development lineage by assumption.

## Reconciliation
Reconciliation preserves unique work. Open PR heads and task branches remain referenced. Branches not referenced by default branch, PRs or tasks are only ORPHAN_CANDIDATES until unique-commit review. Automatic deletion is forbidden.

## Safe migration and policy sync
Migration is dry-run in OBSERVE and WARN. CANARY and ENFORCE require:
- discovery complete;
- baseline locked;
- reconciliation complete;
- explicit write authorization;
- write-capable auth;
- resolved canonical target lineage;
- no active break-glass;
- allow-listed managed paths only.

Allowed automatic repair is limited to PCC governance/control files. Product source, database state, release tags, customer builds, and unrelated branches are never automatically rewritten.

## Rollout
Fleet rollout sequence is `OBSERVE -> WARN -> CANARY -> ENFORCE`, ordered by `ROLLOUT_WAVE`. CANARY applies only to projects with `CANARY=true`. A failure is project-local and higher-risk waves must not silently bypass unresolved blockers.

## Stale recovery
Expired worker leases become RECLAIMABLE using the same TASK_ID, same task branch and latest pushed SHA. Stale work is reclaimed, not recreated.

## Orphan audit
Orphan audit is evidence-only. It identifies branch candidates but never deletes them. Unique-unmerged work preservation has priority over branch simplification.

## Idempotency and concurrency
State-changing operations use deterministic operation keys. Ledger insertion is idempotent. Concurrency locks are per project + operation and GitHub Actions adds workflow-level concurrency.

## Audit ledger
Every enrollment, discovery, baseline, reconciliation, migration, repair, exception and break-glass event must contain project, operation key, actor/auth provider, result, target-mutation flag and timestamp.

## Break glass and policy exceptions
Break-glass must be explicit, attributable and optionally time-bounded; while active it blocks automatic migration/repair. Policy exceptions are typed, time-bounded where possible, remain visible as drift, and do not rewrite history.

## PCC self-protection
PCC `main` must be protected by repository administration rules requiring control-plane validation before merge. If the available automation credential cannot administer branch protection, the state is reported as an external blocker and must never be represented as PASS.
