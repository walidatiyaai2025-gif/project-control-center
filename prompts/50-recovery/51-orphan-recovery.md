# 51 — Orphan Recovery

PROMPT_ID: PCC-51
VERSION: 1.0.0
APPLIES_TO: ORPHAN_BRANCH_COMMIT_OR_PR
PREVIOUS_STEP: PCC-40_OR_PCC-53
NEXT_STEP: PCC-41_OR_PCC-42_OR_PCC-53
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Identified branch/commit/PR with missing or incomplete Task traceability.
- Live repository evidence and project requirement/task registry.

## Mission

Recover untraceable work without discarding unique implementation.

## Execute

Inspect origin, commits, authorship, PR/Issue links, changed scope, base lineage, CI/QA, and overlap with canonical tasks. Link the orphan to an existing Task if it is the same logical work; otherwise create a canonical Task only after duplicate check.

Select/preserve the strongest implementation lineage. Do not delete the orphan until its unique work is safely integrated or intentionally retained with evidence. Never retroactively fabricate QA/release evidence.

## Required output

Return orphan identity, mapped/new TASK_ID, canonical branch decision, unique commits, overlap risks, required continuation/reconciliation actions, and updated orphan count.
