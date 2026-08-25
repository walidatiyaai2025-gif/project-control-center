# First Pilot — AIMWWeb

Target: `walidatiyaai2025-gif/AIMWWeb`

PCC upgrade constraint: this v1.1.0 control-center upgrade does **not** modify AIMWWeb.

First exact step after PCC self-audit: run `prompts/20-existing-project/20-discover-existing-project.md` against AIMWWeb.

Discovery remains read-only and must determine from live GitHub evidence: remote branches, open/recent PRs, active Issues, releases/tags, unique commits, CI, QA/release evidence, governance files, and the actual existing product-version state.

## Required AIMWWeb version-baseline discovery

Inspect application/customer-visible version if discoverable, package/project manifests, Git tags/releases, build/artifact metadata, candidate version sources, conflicting versions, tag→SHA mappings, and any currently deployed/reviewed version evidence. Record `VERSION_BASELINE_CONFIDENCE`. Do not create a new version number or modify AIMWWeb during discovery.

Only after verified lineage/version evidence exists may Prompt 21 lock the baseline. Version enforcement then migrates forward through OBSERVE → WARN → CANARY → ENFORCE.
