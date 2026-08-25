# Control Plane Architecture

## Purpose

The repository is a governance and delivery control plane, not a product implementation repository.

## Data/control layers

1. **Prompt library** — deterministic operator/worker procedures.
2. **Policies** — non-negotiable delivery laws and quality controls.
3. **Templates + schemas** — canonical machine/human-readable records.
4. **Project status** — one authoritative state per managed project.
5. **Portfolio registry/priorities** — cross-project visibility and priority control.
6. **Dashboard** — read-only projection of canonical portfolio state.
7. **Validation workflows** — guard metadata, structures, registries, and dashboard generation.

## Traceability graph

PORTFOLIO → PROJECT → REQUIREMENT → TASK → BRANCH → COMMIT → PR → CI → QA → RELEASE → USER ACCEPTANCE.

## Authority boundaries

Workers own temporary leases and report Task-local evidence. QA owns acceptance evidence. Integration/Release leads own their gates. The Delivery / Control Lead alone publishes authoritative overall project status.

## Existing repository safety

No governance installation occurs until live discovery and baseline lock identify the actual development lineage. Unique unmerged work is preserved and reconciled; branch simplification is never a reason to discard it.
