# 02 — Upgrade Control Plane

PROMPT_ID: PCC-02
VERSION: 1.1.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: PCC-01_OR_UPGRADE_REQUEST
NEXT_STEP: PCC-01
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- A previously bootstrapped/self-audited control plane.
- Exact current control-plane version and immutable HEAD SHA.
- A defined upgrade requirement and compatibility impact.

## Mission

**INSPECT → RECONCILE → UPGRADE IN PLACE.** Never rebuild a valid PCC from scratch merely for consistency.

## Execute

1. Inspect current version, HEAD, files, prompts, workflows, policies, dashboard, portfolio, schemas, templates and architecture decisions.
2. Classify required capabilities `IMPLEMENTED`, `PARTIAL`, `MISSING`, or `CONFLICTING`.
3. Preserve IMPLEMENTED capabilities; upgrade PARTIAL; add MISSING; migrate CONFLICTING safely with reasoning.
4. Do not reset history, delete unique work, or blindly replace valid files.
5. Classify compatibility as backward-compatible, migration-required, or breaking.
6. Update prompts/policies/templates/schemas/workflows consistently and increment semantic control-plane version.
7. Version central policies and record desired/observed compatibility/rollout implications.
8. Never rewrite old status/evidence to pretend it was created under the new version.
9. Preserve historical tags/SHAs and require managed repositories to record the version/tag/SHA they actually use.
10. Keep product repositories untouched unless the upgrade request explicitly authorizes a target-repository write.
11. Run PCC-01 against the upgraded exact HEAD.

## Required output

Return old/new versions, exact upgrade SHA, reconciliation classification, files reused/updated/created, compatibility notes, migration actions, affected managed projects if known, product-repository impact, and self-audit result.
