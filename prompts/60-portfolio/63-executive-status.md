# 63 — Executive Portfolio Status

PROMPT_ID: PCC-63
VERSION: 1.0.0
APPLIES_TO: AUTHORITATIVE_PORTFOLIO_STATUS
PREVIOUS_STEP: PCC-61_OR_PCC-62
NEXT_STEP: PCC-40_OR_END
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Current portfolio registry/priorities.
- Canonical project status for every project being represented.
- Freshness/drift findings from PCC-61 or equivalent reconciliation.

## Authority

Operate as the portfolio-level DELIVERY / CONTROL LEAD. Worker-local summaries are not authoritative.

## Mission

Publish one canonical portfolio view and refresh dashboard status.

## Execute

For each project show Project, Health, Progress, Production, Development, P0, Blocked, QA, Stale, Waiting for User, Last Sync, and Control Plane Maturity. Include portfolio totals for TOTAL PROJECTS, HEALTHY, NEEDS ATTENTION, CRITICAL, ACTIVE TASKS, WAITING FOR USER, and UNTRACKED REQUESTS.

Reference immutable SHAs/releases where applicable. Keep unknown values explicit. Progress must come only from canonical scope/evidence.

Regenerate `portfolio/status/index.json`/dashboard projection and record the exact control-center SHA used.

## Required output

Return the authoritative portfolio summary, top cross-project risks/actions, projects needing reconciliation/onboarding, dashboard generation status, and exact source SHA.
