# 10 — Initialize New Project

PROMPT_ID: PCC-10
VERSION: 1.0.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: START_HERE
NEXT_STEP: PCC-11
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- A new project repository or approved repository creation target.
- Confirmed project purpose, owner, repository identity, and initial delivery constraints.
- No existing live development history that would require the Existing Project sequence.
- Read access to this control plane and write access to the new repository.

## Mission

Create the minimum governed delivery skeleton before product coding begins.

## Execute

Create a PROJECT_ID and install the managed-repository control marker with control-plane repository/version/SHA. Create canonical requirement/task/status locations, initial CODEOWNERS and PR traceability template, CI skeleton appropriate to the technology, ADR location, release evidence location, and governance reference.

Define the intended production branch and canonical integration strategy explicitly because the project is new; do not copy arbitrary branch conventions from another project. Create the initial project status with unknown/not-yet-created SHAs represented truthfully.

Create no product feature code unless represented by a separate canonical Task ID after this onboarding sequence.

## Gate

Before completing, confirm there are zero untracked implementation requests and no coding has occurred outside a Task ID.

## Required output

Return PROJECT_ID, repository, control-plane version/SHA recorded, created governance paths, initial branch model, canonical status path, and exact next prompt PCC-11.
