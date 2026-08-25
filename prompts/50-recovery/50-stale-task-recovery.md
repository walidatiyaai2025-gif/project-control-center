# 50 — Stale Task Recovery

PROMPT_ID: PCC-50
VERSION: 1.0.0
APPLIES_TO: STALE_OR_RECLAIMABLE_TASK
PREVIOUS_STEP: PCC-40_OR_STALE_DETECTION
NEXT_STEP: PCC-42
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Canonical TASK_ID currently suspected/marked STALE.
- Canonical task branch identity.
- Access to branch, commits, PR, CI, QA, lease history, and current project base lineage.

## Mission

Reclaim stale work instead of recreating it.

## Execute

Fetch the latest pushed task-branch SHA and compare it with project integration/base. Determine whether the branch contains unique work, is already integrated, conflicts with newer work, or has an active PR/CI state. Preserve every unique commit.

Expire/release the old Worker lease according to evidence, mark the task `RECLAIMABLE`, and prepare same-task/same-branch takeover. If the branch is unusable, document why and define a preservation/port strategy before any replacement branch.

## Required output

Return TASK_ID, canonical branch, latest SHA, unique-work status, lease disposition, required reconciliation, and exact PCC-42 continuation instructions.
