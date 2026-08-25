# 24 — Enable Enforcement

PROMPT_ID: PCC-24
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-23
NEXT_STEP: PCC-25
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Control-plane installation from PCC-23 on the verified development lineage.
- Canonical task mapping for existing active work.
- CI/QA/release requirements identified for the project.

## Mission

Turn governance from documentation into enforceable delivery gates without breaking valid existing work.

## Execute

Enable/adjust branch/PR/CI conventions available through repository files: require Task ID traceability in PR templates/checks, validate canonical status/task records, bind CI evidence to exact SHAs, protect official build identity, and require QA/integration/release evidence before DONE.

Where repository settings or external branch protection cannot be changed by this prompt, record the exact manual/platform setting still required. Do not weaken existing quality gates. Grandfather only explicitly documented pre-control-plane work and map it to canonical tasks.

Ensure stale work is recoverable by same task/branch/SHA, and worker-local reports cannot publish authoritative project state.

## Required output

Return enforcement changes, exact SHA/PR, checks enabled, settings still external/manual, exceptions with Task IDs, and next prompt PCC-25.
