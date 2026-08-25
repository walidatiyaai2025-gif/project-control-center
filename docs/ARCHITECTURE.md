# Control Plane Architecture

## Purpose

The repository is a governance and delivery control plane, not a product implementation repository.

## Data/control layers

1. **Prompt library** — deterministic operator/worker procedures.
2. **Policies** — non-negotiable delivery, orchestration, and immutable product-version laws.
3. **Templates + schemas** — canonical machine/human-readable records.
4. **Project status** — one authoritative state per managed project.
5. **Portfolio registry/priorities** — cross-project visibility and priority control.
6. **Central orchestration** — enrollment, desired-vs-observed state, compatibility, rollout modes, drift and safe remediation planning.
7. **Version governance** — one canonical product version source, immutable version→SHA identity, version manifests and release guards.
8. **Dashboard** — read-only projection of canonical portfolio/version state.
9. **Validation workflows** — guard metadata, structures, registries, orchestration contracts and dashboard generation.

## Traceability graph

PORTFOLIO → PROJECT → REQUIREMENT → TASK → TARGET VERSION → BRANCH → COMMIT → PR → CI → QA → RELEASE CANDIDATE → RELEASE TAG → PRODUCTION → USER ACCEPTANCE.

## Authority boundaries

Workers own temporary leases and report Task-local evidence. QA owns acceptance evidence. Integration/Release leads own their gates. The Delivery / Control Lead alone publishes authoritative overall project status.

## Existing repository safety

No governance installation occurs until live discovery and baseline lock identify the actual development lineage and version baseline. Unique unmerged work and legitimate historical releases/tags are preserved. If historical version identity is uncertain, record `VERSION_BASELINE_CONFIDENCE`; never invent history.

## Orchestration safety

The orchestrator is declarative. Desired state and observed state are separate. Default execution is dry-run/observe. WARN is non-mutating. CANARY and ENFORCE require explicit enrollment, compatibility, concurrency and policy gates. Safe self-healing is restricted to declared metadata/status repairs; branch deletion, history rewrite, release retagging and product-code mutation are never automatic safe-heal actions.

Cross-repository credentials are abstracted by provider name and supplied at runtime; secrets are never stored in repository state.

## Version immutability

External/reviewable version identity is a tuple anchored by `PRODUCT_VERSION` and `SOURCE_SHA`. Once distributed, a version string cannot later map to another SHA. Official artifact names, tags, manifests, CI evidence and user-visible/package versions must reconcile to the canonical version source.
