# 61 — Portfolio Audit

PROMPT_ID: PCC-61
VERSION: 1.1.0
APPLIES_TO: PORTFOLIO_AUDIT
PREVIOUS_STEP: PCC-60_OR_SCHEDULED_AUDIT
NEXT_STEP: PCC-62_OR_PCC-63
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Portfolio registry/priorities, desired/observed orchestration state and canonical project status sources.
- Read access to live repositories where synchronization is verified.

## Mission

Measure portfolio control, version and policy health and identify drift.

## Audit

Verify unique project/repo mapping, maturity/lifecycle, last-sync freshness, production/development SHA evidence, current production/development versions, next/user-review candidates, release identity, health, priorities, blockers, QA, stale/reclaimable, waiting, orphan/duplicate and untracked requests.

Compare desired vs observed control-plane/policy/version state. Flag VERSION_DRIFT, missing version baseline, stale observed state, enforcement ahead of readiness, or versions/tags whose SHA identity conflicts. Identify projects in UNMANAGED/DISCOVERY/MIGRATING and next onboarding prompt.

## Required output

Return portfolio totals, VERSION_DRIFT_PROJECTS, maturity/enforcement distribution, per-project production/development version@SHA, next candidate, control-plane version, drift/blockers and next control action. Make no writes.
