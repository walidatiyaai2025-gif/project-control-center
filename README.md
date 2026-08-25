# Project Control Center

Central GitHub Portfolio & Software Delivery Control Plane for current, legacy, and future repositories.

**CONTROL_PLANE_VERSION: v1.2.0**

Start with [`START_HERE.md`](START_HERE.md). Do not begin repository work from chat history or memory; choose the project scenario there and run the numbered prompt sequence.

## Canonical principles

- Every request maps to a canonical Task ID before implementation.
- Existing projects are discovered before governance is imposed.
- Task identity and canonical task branch survive Worker changes.
- Project-wide status has one canonical source and is published only by the Delivery / Control Lead.
- Official builds are produced by controlled CI from immutable SHAs.
- Every customer/reviewable product version has one immutable version identity; the same version must never represent different source code.
- Central orchestration is desired-vs-observed, policy-versioned, idempotent, concurrency-guarded, failure-isolated, and rollout-aware.
- `CODE EXISTS != FEATURE COMPLETE`: customer-facing completion is derived from end-to-end Feature/Screen/Action connectivity, QA, persistence, official-build presence, release and user acceptance evidence.
- Portfolio state is derived from canonical evidence; never from Worker percentage estimates.

## End-to-end feature delivery governance

See [`policies/END_TO_END_FEATURE_DELIVERY_POLICY.md`](policies/END_TO_END_FEATURE_DELIVERY_POLICY.md). PCC v1.2.0 adds canonical Feature Delivery Matrix, Screen Inventory, Screen Action Matrix, derived feature states, false-DONE detection, persistence/false-success gates, official-build connectivity, separate visual/functional screen completion, and reusable CI enforcement.

## Central orchestration

See [`orchestration/README.md`](orchestration/README.md).

## Immutable product version governance

See [`policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md`](policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md) and `.github/workflows/reusable-version-governance.yml`.

## First pilot

The first intended existing-project pilot is `walidatiyaai2025-gif/AIMWWeb`. This PCC upgrade does **not** modify AIMWWeb. The pilot begins with read-only Prompt 20 before any governance installation.
