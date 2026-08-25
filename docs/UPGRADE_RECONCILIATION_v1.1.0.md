# PCC Upgrade Reconciliation — v1.0.0 → v1.1.0

## Baseline inspected

- Version before: `v1.0.0`
- HEAD before: `43ee790af03eae6819d8fa15353c2ed331a28dc9`
- Existing prompt library: 30 mandatory prompts
- Existing controls preserved: governance laws, worker lease/task lifecycle, existing-project safety, QA/integration/release/delivery roles, recovery, portfolio registry, canonical status, schemas/templates, dashboard foundation and validation workflows.

## Capability classification

| Capability | Before | v1.1.0 action |
|---|---|---|
| Core task/branch/worker governance | IMPLEMENTED | Preserved |
| Existing-project live discovery | IMPLEMENTED | Upgraded with version-baseline discovery |
| Canonical project status | IMPLEMENTED | Extended with version identities |
| Portfolio dashboard | PARTIAL | Extended with production/development/candidate/control-plane version view |
| Repository Enrollment Controller | MISSING | Added declarative enrollment/profile foundation |
| Central Orchestrator | MISSING | Added desired-vs-observed orchestrator + workflow |
| Policy Version Manager | MISSING | Added policy catalog/current/previous model |
| Dry Run / Observe / Warn | MISSING | Added |
| Canary / Wave / Enforce | MISSING | Added guarded rollout model |
| Policy rollback | PARTIAL | Added policy previous-version metadata; product history remains immutable |
| Drift detection | PARTIAL | Extended to control-plane/policy/version state |
| Safe self-healing | MISSING | Added strict PCC-local allow-list |
| Concurrency locks | MISSING | Added workflow + per-operation lock |
| Idempotent operations | MISSING | Added stable operation keys + ledger de-duplication |
| Failure isolation | PARTIAL | Orchestrator reports per-project failures independently |
| Cross-repository authentication abstraction | MISSING | Added provider contract; no credentials stored |
| Audit ledger | MISSING | Added logical ledger model |
| Portfolio state aggregator | PARTIAL | Extended dashboard projection |
| Immutable customer version policy | MISSING | Added mandatory central policy |
| No same-version/different-code guard | MISSING | Added script, tests, reusable workflow |
| Version manifest | MISSING | Added schema/template/generator |
| User acceptance version identity | PARTIAL | Extended template and delivery prompts |

## Conflict classification

No existing valid governance law required destructive replacement. No branch history was reset. Existing files were extended where their responsibility already existed; new files were added only for capabilities absent in v1.0.0.

## Product repository impact

None. AIMWWeb remains untouched during this upgrade.
