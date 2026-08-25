# Immutable Product Version Policy

CONTROL_PLANE_VERSION: v1.1.0
POLICY_ID: IMMUTABLE_CUSTOMER_VERSION_POLICY
POLICY_VERSION: 1.0.0

## Fundamental version law

Every build or deployment presented to a customer/user as an official or reviewable product version MUST have a unique immutable version identity. Once a version has been delivered externally, **that version number must never represent different source code again**.

If `2.7.3` was delivered from SHA `abc123`, another official/reviewable `2.7.3` from SHA `def456` MUST fail. Source change requires a new version identity.

## Default format

Use Semantic Versioning `MAJOR.MINOR.PATCH`, with pre-release identities such as `2.8.0-alpha.1`, `2.8.0-beta.1`, `2.8.0-rc.1`. Distributed pre-release identifiers are immutable too; use `rc.2`, never reuse `rc.1` for different code.

New projects normally start at `0.1.0` or another justified pre-1.0 version and move to a stable version when product readiness warrants it. Do not force `1.0.0` prematurely.

## One canonical product version source

Every managed product repository has exactly `ONE_CANONICAL_PRODUCT_VERSION_SOURCE`. Preferred default is root `VERSION`. An existing stack-native manifest/package/project file may be designated instead. All display/package/artifact versions derive from that one source; multiple independently editable version numbers are forbidden.

Project profile fields:

- `VERSION_POLICY`
- `VERSION_SOURCE`
- `VERSION_DISPLAY_REQUIRED`
- `VERSION_ENDPOINT_REQUIRED`
- `VERSION_TAG_PATTERN`
- `ARTIFACT_NAMING_PATTERN`
- `CURRENT_RELEASE_VERSION`
- `TARGET_DEVELOPMENT_VERSION`
- `VERSION_BASELINE_CONFIDENCE`

## Customer-visible version

Official customer/user-visible software exposes the current version in an appropriate location: web footer/About/System Information; mobile Settings/About; desktop About/System Information/installer metadata; API/service safe info/version/health contract. Do not expose secrets or sensitive infrastructure metadata.

Minimum normal string: `Version 2.7.3`. Build ID and short commit may be shown diagnostically.

## Build identity and manifest

Official/reviewable builds record, where technically appropriate:

`PRODUCT_VERSION`, `SOURCE_SHA`, `BUILD_ID`, `BUILD_TIME`, `CONTROL_PLANE_VERSION`, `CI_RUN_ID`, `ARTIFACT_DIGEST`.

The version manifest travels with the official artifact where practical.

## Release/tag law

Every official released product version maps to an immutable Git tag, default `v{PRODUCT_VERSION}`, at the exact source SHA. A tag/version already mapped to one SHA must never be moved or reused for another source state.

User-review candidates also have unique versions and must not be delivered anonymously as `latest.apk`, `final.zip`, `new.exe`, or equivalent authoritative names.

## Artifact naming

Official artifact names include product version, for example `AIMWWeb-2.7.3.zip`. Ambiguous authoritative names such as `final.zip`, `final2.apk`, `latest.exe` are forbidden.

## Development target and task traceability

PCC records `CURRENT_RELEASE_VERSION` and `TARGET_DEVELOPMENT_VERSION`. Customer-impacting tasks record `TARGET_VERSION` and later `RELEASED_IN_VERSION`.

Traceability: TASK → TARGET VERSION → BRANCH → COMMITS → PR → INTEGRATION → RELEASE CANDIDATE → RELEASE TAG → PRODUCTION.

Workers receive canonical development branch/SHA, current release version, target development version, and task target version before implementation; they must not guess.

## Official build/release gate

Before official build/release validate:

1. canonical version exists;
2. format is valid;
3. user-visible version matches canonical source when required;
4. package/manifest version matches when required;
5. tag/version pair is valid;
6. version has not already been used for a different released/distributed SHA;
7. official artifact naming includes version;
8. release notes identify version;
9. source SHA is immutable/explicit;
10. CI evidence belongs to that SHA.

Any inconsistency is `VERSION_DRIFT` and blocks official release.

## Existing-project migration

Existing repositories first discover current application/version sources, manifests, tags, releases and deployed/customer version if discoverable. Detect conflicting sources, select a verified baseline, establish one canonical source, reconcile display/package metadata, then enforce immutable versioning forward from the locked baseline. Preserve legitimate historical tags/releases. Never invent historical versions. If exact history is uncertain, record `VERSION_BASELINE_CONFIDENCE` and a documented forward baseline.

Enforcement rollout is `OBSERVE → WARN → CANARY → ENFORCE`; do not immediately break unmanaged existing repositories.

## Rollback

Every release records `PREVIOUS_KNOWN_GOOD_VERSION` and `PREVIOUS_KNOWN_GOOD_SHA`. Rollback references that immutable prior identity; it does not republish new source under an old version.
