# 30 — Legacy Inventory

PROMPT_ID: PCC-30
VERSION: 1.0.0
APPLIES_TO: LEGACY_DORMANT_PROJECT
PREVIOUS_STEP: START_HERE
NEXT_STEP: PCC-31
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Legacy repository URL and read access.
- Evidence that the project is dormant/legacy rather than actively developed.
- Access to control-plane policies.

## Mission

Inventory a dormant repository without accidentally reactivating or rewriting it.

## Inspect

Collect branches, tags/releases, last meaningful commits, open/closed PRs, Issues, CI configuration/history, deployment/release clues, dependencies, known production references, documentation, database/migration assets, secrets/config indicators, and unique unmerged work.

Determine whether the repository is safely archivable, needs maintenance ownership, or contains unresolved production/support obligations. Never delete unique work or assume the default branch equals the production lineage.

## Required output

Return repository inventory, last verified activity, candidate production/release identity if evidence exists, unresolved branches/PRs, security/dependency concerns, data/operational obligations, recommended lifecycle state, and exact next prompt PCC-31.
