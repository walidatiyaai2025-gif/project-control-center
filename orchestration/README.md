# Central Orchestration

PCC v1.1.0 orchestration is declarative and non-destructive by default.

## Components

- `desired-state.json` — operator-approved target state.
- `observed-state.json` — latest collected repository state.
- `policy-catalog.json` — current/previous policy versions and rollout defaults.
- `audit-ledger.json` — append-only logical operation ledger snapshot.
- `scripts/enrollment_controller.py` — idempotent PCC-local repository enrollment planning/application; it never edits the product repository.
- `scripts/orchestrator.py` — compatibility scan, desired-vs-observed reconciliation, drift report, rollout selection, stable operation keys and per-project locks.
- `.github/workflows/central-orchestrator.yml` — controlled observe/warn/canary/enforce reconciliation.

## Authentication abstraction

Profiles name `AUTH_PROVIDER` only: `github_app`, `connector`, `token_runtime`, or `none/read_only`. Credentials are injected at runtime and never persisted.

## Safe self-healing boundary

The v1.1.0 orchestrator repairs only allow-listed PCC-derived local metadata when explicitly invoked with `--apply-safe`. It does not delete/force-push branches, move tags, edit product code, deploy, change databases, or publish builds. Cross-repository writes require an explicitly authorized project prompt/workflow.

## Enrollment lifecycle

DISCOVER → PROFILE → DESIRED_STATE → OBSERVE → WARN → CANARY → ENFORCE.

Existing repositories cannot skip lineage/version baseline discovery merely because they are centrally enrolled.
