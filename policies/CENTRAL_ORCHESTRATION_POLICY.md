# Central Orchestration Policy

CONTROL_PLANE_VERSION: v1.1.0
POLICY_VERSION: 1.0.0

## Mandatory controllers

PCC provides a Repository Enrollment Controller, Central Orchestrator, Policy Version Manager, Desired-vs-Observed State model, Compatibility Scanner, Drift Detector, Audit Ledger and Portfolio State Aggregator.

## Rollout modes

`OBSERVE → WARN → CANARY → ENFORCE`.

- OBSERVE: read/compare only; no target repository mutation.
- WARN: read/compare plus actionable warnings; no target repository mutation.
- CANARY: only explicitly enrolled canary projects and explicitly authorized policy changes may be applied.
- ENFORCE: policy gates may block noncompliant delivery after compatibility and baseline evidence exist.

Wave rollout uses `ROLLOUT_WAVE`; lower waves complete before higher waves unless an explicit exception is recorded.

## Safety laws

1. Dry run is the default for central orchestration.
2. Existing repositories require live discovery before policy mutation.
3. Operations use stable idempotency keys; repeating an already-completed operation must not create duplicate work.
4. One project failure must not prevent reconciliation reports for other projects.
5. Concurrency is locked per project + policy operation.
6. Policy rollback points to a known policy version; rollback never rewrites product history.
7. Safe self-healing is allow-listed. Allowed examples: regenerate PCC projections, repair missing derived status metadata, re-evaluate observed state. Forbidden automatic actions include deleting branches, force-pushing, moving release tags, changing product source, changing database state, or publishing customer builds.
8. Cross-repository authentication uses an abstraction (`github_app`, `connector`, `token_runtime`, or approved equivalent). Credential material is runtime-only and never committed.
9. Every state-changing orchestration attempt must append an audit event with project, operation key, actor/provider, desired/observed versions, result and timestamp.
10. Product repositories are modified only by an explicitly authorized workflow/prompt whose write scope is declared.

## Desired vs observed

Desired state contains target control-plane version, policy version, enforcement mode, rollout wave, project profile/version policy, and expected managed files/checks. Observed state is collected from the repository and CI. Drift is the deterministic difference; unknown observations are not treated as compliant.
