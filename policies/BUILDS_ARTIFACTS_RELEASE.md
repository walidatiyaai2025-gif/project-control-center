# Official Builds, Artifact Identity and Release Candidates

Official builds are generated only by controlled CI from immutable SHAs. Each artifact must identify project, source SHA, workflow/run, build/version, environment/target, creation time, and checksum where feasible.

A release candidate must reference the canonical integration SHA and all required QA evidence. A release must record immutable source SHA, artifact identity, tag/version, deployment target, release notes, rollback reference, and production verification state.

Local untracked builds are never authoritative release evidence.
