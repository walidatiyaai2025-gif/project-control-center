# 23 — Install Control Plane

PROMPT_ID: PCC-23
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: PCC-22
NEXT_STEP: PCC-24
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- PCC-20 discovery, PCC-21 baseline, and PCC-22 reconciliation completed.
- Verified development lineage and preservation plan for unique unmerged work.
- Write access to the target repository and Project Control Center.

## Mission

Install governance into the existing repository without disrupting its verified development lineage.

## Execute

Add the managed-repository control marker containing this control-plane repository plus exact version/tag/SHA. Add canonical status/task/requirement evidence locations, traceable PR template, CODEOWNERS coverage where appropriate, ADR/documentation/release evidence paths, and validation hooks compatible with the repository's technology.

Integrate governance on the verified live development lineage or a governance branch based from its exact SHA. Do not reset the repository to a conventional branch. Do not delete or overwrite pre-existing governance; reconcile it explicitly.

Populate initial status from discovered evidence, using null/unknown rather than guesses. Worker estimates must not become project-wide progress.

## Required output

Return exact target branch/base SHA, installation commit/PR, control-plane version/SHA recorded, canonical status path, preserved-work confirmation, and next step PCC-24.
