# 24 — Enable Enforcement

PROMPT_ID: PCC-24
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-23
NEXT_STEP: PCC-25
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- PCC-23 installation on verified development lineage.
- Canonical task mapping for active work.
- CI/QA/release requirements identified.
- Product version baseline/profile installed where applicable.

## Mission

Turn governance into staged enforceable delivery gates without breaking valid existing work.

## Execute

Enable Task-ID PR traceability, canonical status/task validation, exact-SHA CI evidence, official build identity, and QA/integration/release evidence before DONE.

For central/version policy, progress deliberately through `OBSERVE → WARN → CANARY → ENFORCE`. Existing repositories begin OBSERVE unless stronger readiness is proven. Before CANARY/ENFORCE confirm discovery complete, baseline locked, version baseline established, canonical version source valid, display/package reconciliation supported, immutable tag/version guard wired, version manifest generation available, and rollback identity represented.

Use dry-run/compatibility/drift reports before changing mode. Never force policy ENFORCE to hide unresolved version/history conflicts. Where repository settings/branch protection remain external, record exact manual settings.

Ensure stale work remains recoverable by same task/branch/SHA and Worker-local reports cannot publish overall project state.

## Required output

Return enforcement changes, exact SHA/PR, orchestration mode/wave, compatibility/drift result, version guards enabled, external settings, exceptions with Task IDs, and PCC-25.
