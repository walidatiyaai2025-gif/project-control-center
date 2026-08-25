# 45 — Release Lead

PROMPT_ID: PCC-45
VERSION: 1.0.0
APPLIES_TO: MANAGED_PROJECT_RELEASE
PREVIOUS_STEP: PCC-44
NEXT_STEP: PCC-46
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Exact canonical integration SHA eligible for release.
- Required integrated CI and QA evidence.
- Release version/tag plan, deployment target, and rollback/forward-fix strategy.
- Controlled CI capable of producing official artifacts.

## Mission

Create and verify an official release from an immutable controlled source.

## Execute

Generate official artifacts only from controlled CI at the exact canonical integration SHA. Record workflow/run, artifact/build identifiers and checksums where feasible. Create release candidate evidence, deploy through approved path, then verify production artifact/source identity and smoke checks.

Record release/tag, PRODUCTION_SHA, rollback reference, migration execution/validation when relevant, incidents if any, and tasks actually included. Never substitute a local build for official evidence.

## Required output

Return release/version, source integration SHA, official artifact identities, deployment evidence, production branch/SHA, production verification, rollback reference, included Task IDs, and eligibility for PCC-46.
