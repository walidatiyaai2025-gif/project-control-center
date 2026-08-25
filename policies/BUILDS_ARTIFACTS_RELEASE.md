# Official Builds, Artifact Identity and Release Candidates

Official builds are generated only by controlled CI from immutable SHAs. Each official/reviewable artifact must identify project, `PRODUCT_VERSION`, source SHA, workflow/run, build ID, environment/target, creation time, control-plane version and checksum/digest where feasible.

All customer/reviewable product versions are additionally governed by `IMMUTABLE_PRODUCT_VERSION_POLICY.md`: one canonical product version source, immutable version→SHA mapping, non-ambiguous versioned artifact names, user-visible/package reconciliation where required, and an immutable version manifest.

A release candidate must reference the canonical integration SHA, unique candidate version, build ID and all required QA evidence. A release must record immutable source SHA, artifact identity, immutable tag/version, deployment target, release notes, previous known-good version/SHA, rollback reference, and production verification state.

Local untracked builds, Worker-branch builds and anonymous artifacts such as `latest.*` or `final.*` are never authoritative customer/release evidence.
