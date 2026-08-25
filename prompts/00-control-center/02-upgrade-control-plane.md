# 02 — Upgrade Control Plane

PROMPT_ID: PCC-02
VERSION: 1.0.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: PCC-01
NEXT_STEP: PCC-01
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- A previously self-audited control-plane version.
- Exact current control-plane version and immutable HEAD SHA.
- A defined upgrade requirement and compatibility impact.

## Mission

Upgrade the control plane without silently changing the rules applied to managed repositories.

## Execute

1. Diff the requested governance behavior against the current version.
2. Classify changes as backward-compatible, migration-required, or breaking.
3. Update prompts/policies/templates/schemas/workflows consistently.
4. Increment the semantic control-plane version.
5. Document managed-repository migration requirements and which maturity states are affected.
6. Never rewrite old status/evidence to pretend it was created under the new version.
7. Preserve historical tags/SHAs and require managed repositories to record the version/tag/SHA they actually use.
8. Run PCC-01 against the upgraded exact HEAD.

## Required output

Return old/new versions, exact upgrade SHA, compatibility notes, migration actions, affected managed projects if known, and self-audit result.
