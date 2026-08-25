# Project Control Center

Central GitHub Portfolio & Software Delivery Control Plane for current, legacy, and future repositories.

**CONTROL_PLANE_VERSION: v1.1.0**

Start with [`START_HERE.md`](START_HERE.md). Do not begin repository work from chat history or memory; choose the project scenario there and run the numbered prompt sequence.

## Canonical principles

- Every request maps to a canonical Task ID before implementation.
- Existing projects are discovered before governance is imposed.
- Task identity and canonical task branch survive Worker changes.
- Project-wide status has one canonical source and is published only by the Delivery / Control Lead.
- Official builds are produced by controlled CI from immutable SHAs.
- Every customer/reviewable product version has one immutable version identity; the same version must never represent different source code.
- Central orchestration is desired-vs-observed, policy-versioned, idempotent, concurrency-guarded, failure-isolated, and rollout-aware.
- Portfolio state is derived from project status, task evidence, GitHub state, CI, QA, release, version, and user acceptance evidence; never from Worker percentage estimates.

## Central orchestration

See [`orchestration/README.md`](orchestration/README.md). The control plane supports enrollment planning, compatibility scanning, dry run, OBSERVE/WARN/CANARY/ENFORCE rollout stages, desired-vs-observed drift, policy rollback metadata, safe self-healing boundaries, concurrency locks, idempotency, audit ledger records, cross-repository authentication abstraction, and portfolio aggregation.

## Immutable product version governance

See [`policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md`](policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md) and the reusable workflow `.github/workflows/reusable-version-governance.yml`.

## First pilot

The first intended existing-project pilot is `walidatiyaai2025-gif/AIMWWeb`. This PCC upgrade does **not** modify AIMWWeb. The pilot begins with read-only Prompt 20, including version baseline discovery, before any governance installation.
