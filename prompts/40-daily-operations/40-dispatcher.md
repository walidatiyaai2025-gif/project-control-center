# 40 — Dispatcher

PROMPT_ID: PCC-40
VERSION: 1.1.0
APPLIES_TO: MANAGED_PROJECT_DAILY_OPERATIONS
PREVIOUS_STEP: PCC-12_OR_PCC-25_OR_PRIOR_DAILY_CYCLE
NEXT_STEP: PCC-41_OR_PCC-42_OR_PCC-43_OR_PCC-44
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Managed project with canonical status, project profile and verified development lineage.
- Portfolio/project state synchronized recently enough to dispatch safely.
- Incoming requests/issues/bugs to evaluate.

## Mission

Convert work demand into canonical, non-duplicated Tasks and lease work safely with explicit release-target context.

## Execute

1. Sync live Issues, PRs, active task branches, stale/reclaimable work, blockers, QA/integration queues and current version status.
2. Before creating any Task, search duplicates/overlap across requirements, Tasks, branches, PRs and recent commits.
3. Prefer continuation/reclaim over a new logical task.
4. For a genuinely new request create one canonical Task ID, branch plan, Ready/acceptance criteria, risk, dependencies and priority.
5. For customer-impacting work set `TARGET_VERSION` only from the approved `TARGET_DEVELOPMENT_VERSION`/release plan; if not decided leave null and flag the decision. Never guess.
6. Dispatch Worker context with CANONICAL DEVELOPMENT BRANCH/SHA, CURRENT RELEASE VERSION, TARGET DEVELOPMENT VERSION and TASK TARGET VERSION where applicable.
7. Assign only temporary Worker leases.
8. Prioritize P0/safety blockers and critical version/release drift according to portfolio policy.

## Required output

Return dispatch table with Task IDs, states, canonical branches, latest SHA, lease owner, TARGET_VERSION, blockers, next role/prompt, and untracked request count. No Worker-derived project percentage.
