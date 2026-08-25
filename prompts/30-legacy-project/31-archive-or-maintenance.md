# 31 — Archive or Maintenance Decision

PROMPT_ID: PCC-31
VERSION: 1.0.0
APPLIES_TO: LEGACY_DORMANT_PROJECT
PREVIOUS_STEP: PCC-30
NEXT_STEP: END_OR_PCC-32
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Completed PCC-30 inventory.
- Evidence of runtime/production/support obligations and unresolved unique work.
- Write access to the control-center portfolio; repository archive/settings access only if explicitly intended.

## Mission

Place the legacy project into `MAINTENANCE` or `ARCHIVED` control-plane state without losing evidence.

## Execute

Choose the lifecycle based on actual obligations. Register/update the project, preserve production/release references, document unresolved security/dependency/data/operational risks, and record unique unmerged work. If archived, define reactivation entry through PCC-32. If maintenance, define the narrow classes of Tasks that may be opened.

Do not delete branches, releases, artifacts, or history merely to make archival cleaner. Repository-level archive toggles are optional platform actions and require explicit scope.

## Required output

Return selected lifecycle/maturity, portfolio/status updates, preserved obligations, allowed future work, and reactivation path.
