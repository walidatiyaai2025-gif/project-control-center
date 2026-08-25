# 62 — Cross-Project Priority Controller

PROMPT_ID: PCC-62
VERSION: 1.0.0
APPLIES_TO: PORTFOLIO_PRIORITY_CONTROL
PREVIOUS_STEP: PCC-61_OR_PRIORITY_CHANGE_REQUEST
NEXT_STEP: PCC-63_OR_PCC-40
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Current portfolio audit/status with project health and critical work.
- Known business/operational priority inputs.
- `portfolio/priorities.yml` available for controlled update.

## Mission

Set a single evidence-backed cross-project work order without rewriting project-local truth.

## Execute

Rank projects/objectives using criticality, P0/production risk, security/data-loss risk, release blockers, waiting-for-user dependencies, stale work cost, and business deadlines where supplied. Production safety/P0 outranks ordinary feature throughput unless an explicit higher-level decision says otherwise.

Record priority order, rationale, timestamp, and any temporary overrides. Do not change task state merely to make priorities look aligned; dispatchers consume this order in PCC-40.

## Required output

Return exact prioritized project/objective order, rationale, blockers/user decisions, changes from prior order, priorities file SHA, and projects whose dispatcher should run next.
