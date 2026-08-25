# 22 — Reconcile Existing Work

PROMPT_ID: PCC-22
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-21
NEXT_STEP: PCC-23
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Immutable PCC-21 lineage/version baseline.
- Inventory of active PRs, branches, Issues, unique commits and version-source conflicts.
- No unresolved ambiguity that would make reconciliation destructive.

## Mission

Map pre-control-plane work into canonical requirements/tasks and reconcile version conventions without losing live work/history.

## Execute

For every active request/Issue/PR/branch/unique commit cluster, classify existing logical task, duplicate implementation, orphan, stale, or unrelated history. Assign/plan canonical Task IDs and one canonical task branch per logical task. Prefer continuation of strongest valid lineage and preserve unique commits.

For versioning, classify existing version sources as canonical candidate, derived display/package source, historical-only, or conflicting. Preserve legitimate historical tags/releases. Select a forward canonical source only from PCC-21 evidence; if exact historical version is unknown, document a forward baseline and confidence rather than rewriting history. Map customer-impacting active tasks to `TARGET_VERSION` only when the target version is evidenced/approved; otherwise leave null/unknown.

Create a reconciliation plan; do not silently rewrite branch or tag history.

## Required output

Return canonical task map/branches, preserved unique work, duplicate/orphan/stale classifications, version-source reconciliation, historical tags/releases preserved, target-version mapping/unknowns, planned safe actions, and readiness for PCC-23.
