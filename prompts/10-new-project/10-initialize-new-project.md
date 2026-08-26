# 10 — Initialize New Project

PROMPT_ID: PCC-10
VERSION: 1.2.0
APPLIES_TO: NEW_PROJECT
PREVIOUS_STEP: START_HERE
NEXT_STEP: PCC-11
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- A new project repository or approved repository creation target.
- Confirmed project purpose, owner, repository identity, and initial delivery constraints.
- No existing live development history that would require the Existing Project sequence.
- Read access to PCC and write access to the new repository.

## Mission

Create the minimum governed delivery skeleton and automatically classify the repository before product coding begins.

## Execute

Read PCC root `AGENTS.md` and the constitutional onboarding policy first.

Perform project classification automatically: determine `STANDALONE` or `PRODUCT_FAMILY`. If product/client variants are known or owner-declared, enumerate stable variant identities and aliases before implementation starts.

For a product family, create/reconcile root `AGENTS.md` and `.pcc/project-family.json` using the canonical template. Record implementation-location/routing states truthfully; do not invent a directory, permanent client branch, or shared-core boundary.

The owner's request to add/onboard the project authorizes governance-only onboarding files, not product feature code or deployment.

Create PROJECT_ID and managed control marker, canonical requirement/task/status locations, project profile, CODEOWNERS/PR traceability, CI skeleton, ADR/release evidence locations, and governance reference.

For customer/user-visible products designate one canonical version source; default to root `VERSION` and `0.1.0` only when justified for a genuinely new product.

Create no product feature code unless represented by a separate canonical Task ID after onboarding.

## Gate

Confirm project classification is recorded, variant uncertainty is explicit, zero untracked implementation requests exist, and no coding occurred outside Task IDs.

## Required output

Return PROJECT_ID, repository, project model, variant summary/routing blockers, control-plane version/SHA, governance paths, profile/version source, branch model, and exact next prompt PCC-11.
