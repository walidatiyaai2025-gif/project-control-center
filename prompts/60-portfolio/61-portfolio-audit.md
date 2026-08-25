# 61 — Portfolio Audit

PROMPT_ID: PCC-61
VERSION: 1.0.0
APPLIES_TO: PORTFOLIO_AUDIT
PREVIOUS_STEP: PCC-60_OR_SCHEDULED_AUDIT
NEXT_STEP: PCC-62_OR_PCC-63
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Portfolio registry/priorities and project canonical status sources.
- Read access to live project repositories where synchronization must be verified.

## Mission

Measure portfolio control health and identify drift.

## Audit

Verify unique PROJECT_ID/repository mapping, maturity/lifecycle consistency, last-sync freshness, production/development SHA evidence, release identity, health, P0/P1 counts, blockers, QA queue, stale/reclaimable work, waiting-for-user, orphan/duplicate work, and untracked requests.

Flag project records whose authoritative status is older than material live GitHub changes. Identify projects still `UNMANAGED`, `DISCOVERY`, or `MIGRATING` and the next onboarding prompt required.

## Required output

Return total projects, HEALTHY, NEEDS_ATTENTION, CRITICAL, active tasks, waiting-for-user, untracked requests, stale projects, maturity distribution, and per-project next control action. Make no writes.
