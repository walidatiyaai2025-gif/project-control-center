# Official Builds, Artifact Identity and Release Candidates

Official builds are generated only by controlled CI from immutable SHAs. Each artifact identifies project, product version, source SHA, workflow/run, build identity, environment/target, creation time and checksum where feasible.

A release candidate references the canonical integration SHA, immutable product version, all required QA evidence, and the canonical Feature Delivery Matrix audit. A feature is `PRESENT_IN_CANDIDATE` only when its exact implementation is contained in the candidate source SHA; a feature is `PRESENT_IN_PRODUCTION` only when contained in the verified production SHA.

A release must record immutable source SHA, artifact identity, tag/version, deployment target, release notes, rollback reference, production verification, included Task/Feature IDs and released-version mapping. A release must not promote requested customer-review scope with unresolved required `IMPLEMENTED_NOT_CONNECTED`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, or `FALSE_DONE_FEATURE` findings unless an approved exception is recorded.

Local untracked builds and Worker branches are never authoritative customer-visible release evidence.
