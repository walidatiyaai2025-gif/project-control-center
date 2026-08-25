# 40 — Dispatcher

PROMPT_ID: PCC-40
VERSION: 1.0.0
APPLIES_TO: MANAGED_PROJECT_DAILY_OPERATIONS
PREVIOUS_STEP: PCC-12_OR_PCC-25_OR_PRIOR_DAILY_CYCLE
NEXT_STEP: PCC-41_OR_PCC-42_OR_PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Managed project with canonical status and verified development lineage.
- Portfolio/project state synchronized recently enough to dispatch safely.
- Incoming requests/issues/bugs to evaluate.

## Mission

Convert work demand into canonical, non-duplicated Tasks and lease work safely.

## Execute

1. Sync live Issues, PRs, active task branches, stale/reclaimable work, blockers, QA queue, and integration queue.
2. Before creating any Task, perform duplicate/overlap search across requirements, Tasks, branches, PRs, and recent commits.
3. Prefer continuation/reclaim of an existing logical task over creating a new one.
4. For a genuinely new request, create one canonical Task ID, one canonical task branch plan, Ready criteria, acceptance criteria, risk, dependencies, and priority.
5. Assign only temporary Worker leases; do not transfer task identity.
6. Dispatch P0/safety blockers ahead of lower-priority throughput according to portfolio priority policy.

## Required output

Return dispatch table with Task IDs, states, canonical branches, latest SHA, lease owner, blockers, next role/prompt, plus untracked request count. Do not publish a project-wide percentage from Worker estimates.
