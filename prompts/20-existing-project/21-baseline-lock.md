# 21 — Baseline Lock

PROMPT_ID: PCC-21
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-20
NEXT_STEP: PCC-22
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Completed PCC-20 discovery from current live GitHub state.
- Evidence-backed candidate production and development lineages.
- Inventory of unique unmerged work and unresolved ambiguity.
- Write access to the Project Control Center; target-repository writes are not yet required.

## Mission

Lock an immutable discovery baseline before reconciling or installing governance.

## Execute

Record PROJECT_ID, discovery timestamp, repository, relevant branch heads, production candidate SHA, canonical development candidate SHA, open PR exact heads, unique unmerged branch SHAs, release/tag evidence, and CI/QA evidence. Any unresolved lineage choice must remain explicitly `UNRESOLVED`; do not select a branch because its name looks conventional.

The baseline is a reference snapshot, not a command to reset the repository. Never force-push, delete branches, close PRs, or discard unique commits in this step.

## Gate

If two or more plausible development lineages remain and evidence cannot distinguish them, stop with a baseline marked unresolved and request reconciliation evidence; do not proceed by guess.

## Required output

Return baseline ID/path, exact locked SHAs, unresolved items, preservation list for unique work, and whether PCC-22 is safe to run.
