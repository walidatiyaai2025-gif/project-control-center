# PCC v1.3.0 — Autonomous Fleet Control Closure

This material upgrade continues from PCC v1.2.0 without reimplementing feature-delivery governance.

Capabilities added:
- live GitHub cross-repository collector with pagination, auth abstraction, retries and rate-limit handling;
- centralized enrollment and idempotent repository identity;
- read-only existing-project discovery and baseline locking;
- existing-work reconciliation that preserves unique branches and PR heads;
- safe migration/policy-sync engine with allow-listed writes only;
- OBSERVE/WARN/CANARY/ENFORCE rollout model;
- stale-task reclaim and orphan-candidate audit;
- portfolio live aggregation;
- GitHub Pages deployment workflow;
- audit ledger, break-glass and policy-exception contracts;
- PCC main-protection audit with explicit blocker semantics when repository-admin write is unavailable.

AIMWWeb is enrolled as OBSERVE + CANARY-eligible with WRITE_AUTHORIZED=false. No AIMWWeb target repository mutation is part of this closure.
