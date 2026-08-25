# 21 — Baseline Lock

PROMPT_ID: PCC-21
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-20
NEXT_STEP: PCC-22
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Completed PCC-20 discovery from current live GitHub state.
- Evidence-backed production/development lineage candidates.
- VERSION BASELINE DISCOVERY for customer/user-visible products.
- Inventory of unique unmerged work and unresolved ambiguity.
- Write access to PCC; target-repository writes are not yet required.

## Mission

Lock immutable lineage and version discovery evidence before reconciliation/governance installation.

## Execute

Record PROJECT_ID, timestamp, repository, branch heads, production candidate SHA, canonical development candidate SHA, open PR heads, unique unmerged branch SHAs, release/tag evidence, CI/QA evidence.

For product versioning record discovered version sources, observed customer/package versions, current release candidate/version if evidenced, tag→SHA mappings, candidate canonical VERSION_SOURCE, CURRENT_RELEASE_VERSION, TARGET_DEVELOPMENT_VERSION if inferable, and VERSION_BASELINE_CONFIDENCE. Unknown or conflicting historical facts remain `UNRESOLVED`; never invent a version to make the baseline complete.

The baseline is a reference snapshot, not a command to reset code or normalize version history. Never force-push, delete branches, close PRs, move tags, or discard unique commits.

## Gate

If plausible development lineages or current customer version cannot be distinguished safely, lock them as unresolved and do not enforce assumptions. PCC-22 may reconcile known work while preserving unresolved evidence, but PCC-24 may not ENFORCE version policy until a forward baseline is explicitly established.

## Required output

Return baseline ID/path, locked SHAs, locked version evidence/confidence, unresolved items, preservation list, and PCC-22 readiness.
