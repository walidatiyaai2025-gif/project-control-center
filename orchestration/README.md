# PCC Fleet Orchestration

PCC v1.3.0 extends the existing desired-vs-observed controller into a live cross-repository fleet control loop while preserving v1.2.0 Feature/Screen/Action governance.

## Canonical loop

`ENROLL -> COLLECT -> DISCOVER -> BASELINE -> RECONCILE -> DRIFT -> PLAN -> OBSERVE/WARN/CANARY/ENFORCE -> AGGREGATE -> AUDIT`

The default is read-only. Existing repositories are not modified until all write gates in `policies/CENTRAL_ORCHESTRATION_POLICY.md` and `policies/FLEET_CONTROL_POLICY.md` pass.

## Runtime entry points

- `scripts/enrollment_controller.py` — idempotent PCC-local repository enrollment; never writes the target repository.
- `scripts/github_fleet_client.py` — authenticated GitHub REST abstraction with pagination, bounded retries and rate-limit handling.
- `scripts/fleet_control.py` — live discovery, baseline lock, reconciliation, drift, rollout, stale/orphan recovery, policy sync and portfolio aggregation.
- `scripts/self_protection.py` — audits/configures PCC main protection when admin credentials are available.
- `.github/workflows/fleet-control.yml` — scheduled/manual live collection.
- `.github/workflows/portfolio-dashboard.yml` — live collection + static dashboard deployment to GitHub Pages.

## State

- Desired fleet membership: `portfolio/projects.yml` and `orchestration/desired-state.json`.
- Seed/last committed observations: `orchestration/observed-state.json`.
- Read-only baseline anchors: `orchestration/baselines/`.
- Reconciliation evidence: `orchestration/reconciliation/`.
- Canonical seed ledger: `orchestration/audit-ledger.json`.
- Per-run runtime ledger/report: uploaded GitHub Actions artifacts.

AIMWWeb is enrolled as OBSERVE/CANARY-capable but `WRITE_AUTHORIZED=false`; this v1.3.0 closure does not mutate AIMWWeb.
