# 10 — Initialize New Project

PROMPT_ID: PCC-10
VERSION: 1.1.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: START_HERE
NEXT_STEP: PCC-11
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- A new project repository or approved repository creation target.
- Confirmed project purpose, owner, repository identity, and initial delivery constraints.
- No existing live development history that would require the Existing Project sequence.
- Read access to this control plane and write access to the new repository.

## Mission

Create the minimum governed delivery skeleton before product coding begins, including product-version identity where the project produces customer/user-visible software.

## Execute

Create a PROJECT_ID and install the managed-repository control marker with control-plane repository/version/SHA. Create canonical requirement/task/status locations, project profile, initial CODEOWNERS and PR traceability template, CI skeleton appropriate to the technology, ADR location, release evidence location, and governance reference.

Define the intended production branch and canonical integration strategy explicitly because the project is new; do not copy arbitrary branch conventions from another project. Create initial status with unknown/not-yet-created SHAs represented truthfully.

For a customer/user-visible product, designate exactly one canonical version source. Default to root `VERSION` and initialize `0.1.0` unless another justified starting version is documented. Configure VERSION_POLICY, VERSION_SOURCE, VERSION_DISPLAY_REQUIRED, VERSION_ENDPOINT_REQUIRED, VERSION_TAG_PATTERN and ARTIFACT_NAMING_PATTERN. Wire version-governance CI in OBSERVE/non-release mode before product delivery. Do not force `1.0.0` before readiness.

Create no product feature code unless represented by a separate canonical Task ID after this onboarding sequence.

## Gate

Confirm zero untracked implementation requests, no coding outside Task IDs, and no independently editable duplicate version sources.

## Required output

Return PROJECT_ID, repository, control-plane version/SHA, created governance paths, project profile/version source and starting version if applicable, initial branch model, canonical status path, and exact next prompt PCC-11.
