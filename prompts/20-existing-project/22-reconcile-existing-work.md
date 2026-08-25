# 22 — Reconcile Existing Work

PROMPT_ID: PCC-22
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-21
NEXT_STEP: PCC-23
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Immutable PCC-21 baseline.
- Inventory of active PRs, branches, Issues, unique commits, and candidate lineages.
- No unresolved ambiguity that would make reconciliation destructive.

## Mission

Map pre-control-plane work into canonical requirements/tasks without losing live work.

## Execute

For every active request/Issue/PR/branch/unique commit cluster, determine whether it maps to an existing logical task, duplicate implementation, orphan work, stale work, or unrelated history. Assign/plan canonical Task IDs and one canonical task branch per logical task.

Prefer continuation of the branch containing the strongest valid implementation lineage. Preserve unique commits even if a branch is not selected as canonical. Do not create duplicate implementation branches to make the structure look cleaner.

Create a reconciliation plan showing merge/cherry-pick/close/archive decisions as future controlled actions; do not silently rewrite history. Identify untracked user requests and drive them toward zero by linking them to requirements/tasks.

## Required output

Return canonical task map, selected canonical branches, preserved unique work, duplicate/orphan/stale classifications, planned safe actions, and readiness for governance installation with PCC-23.
