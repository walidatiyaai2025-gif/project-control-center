# 45 — Release Lead

PROMPT_ID: PCC-45
VERSION: 1.1.0
APPLIES_TO: MANAGED_PROJECT_RELEASE
PREVIOUS_STEP: PCC-44
NEXT_STEP: PCC-46
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Exact canonical integration SHA eligible for release/review candidate.
- Required integrated CI and QA evidence.
- Verified project profile with canonical VERSION_SOURCE and version policy.
- Candidate PRODUCT_VERSION, tag plan, artifact naming plan, deployment target and rollback/forward-fix strategy.
- Controlled CI capable of official artifacts/version manifest.

## Mission

Create/verify an official or user-reviewable release from immutable controlled source with a unique version identity.

## Version change gate

Before delivery/build publication validate:

1. canonical version exists and format is valid;
2. customer-visible version matches canonical source where required;
3. package/manifest version matches where required;
4. intended tag equals VERSION_TAG_PATTERN;
5. version/tag/history is not already mapped to another distributed/released SHA;
6. official artifact name includes correct version and is not ambiguous;
7. release notes identify version;
8. SOURCE_SHA equals approved immutable integration/candidate SHA;
9. CI/QA evidence belongs to same SHA/build;
10. version manifest is generated with PRODUCT_VERSION, SOURCE_SHA, BUILD_ID, BUILD_TIME, CONTROL_PLANE_VERSION, CI_RUN_ID and digest where applicable.

Any mismatch is release-blocking `VERSION_DRIFT`/identity failure. Never move/reuse a distributed candidate or release tag. If `2.8.0-rc.1` changes, issue `rc.2`; if `2.8.0` changes after release, issue an appropriate new semantic version.

## Execute

Generate official artifacts only from controlled CI at exact approved SHA. Record version manifest, workflow/run, artifact identity/digest, release candidate evidence and immutable tag mapping. Deploy through approved path and verify production artifact/source/version identity and smoke checks.

Record PREVIOUS_KNOWN_GOOD_VERSION/SHA for rollback. After proven release, set included Tasks' `RELEASED_IN_VERSION` to actual PRODUCT_VERSION.

## Required output

Return PRODUCT_VERSION, release tag, SOURCE_SHA/integration SHA, BUILD_ID, manifest/artifact identities, CI/QA, deployment/production SHA, previous known-good version/SHA, included Task IDs, and PCC-46 eligibility.
