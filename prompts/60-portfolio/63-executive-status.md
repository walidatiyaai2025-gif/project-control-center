# 63 — Executive Portfolio Status

PROMPT_ID: PCC-63
VERSION: 1.1.0
APPLIES_TO: AUTHORITATIVE_PORTFOLIO_STATUS
PREVIOUS_STEP: PCC-61_OR_PCC-62
NEXT_STEP: PCC-40_OR_END
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Current portfolio registry/priorities.
- Canonical project status for every represented project.
- Freshness/drift findings from PCC-61 or equivalent reconciliation.

## Authority

Operate as portfolio-level DELIVERY / CONTROL LEAD. Worker-local summaries are not authoritative.

## Mission

Publish one canonical portfolio view and refresh dashboard status.

## Execute

For each project show Project, Health, Progress, Production Version@SHA, Development/Target Version@SHA, Next Release Candidate, Latest User Review Candidate, P0, Blocked, QA, Stale, Waiting for User, Version/Policy Drift, Last Sync, Control Plane Maturity and Control Plane Version.

Include totals for TOTAL PROJECTS, HEALTHY, NEEDS ATTENTION, CRITICAL, ACTIVE TASKS, WAITING FOR USER, UNTRACKED REQUESTS and VERSION DRIFT PROJECTS.

Reference immutable SHAs/releases; unknown explicit; progress only canonical evidence. Regenerate dashboard and record exact PCC SHA.

## Required output

Return authoritative portfolio summary, top cross-project/version/policy risks, projects needing reconciliation/onboarding, dashboard status and exact source SHA.
