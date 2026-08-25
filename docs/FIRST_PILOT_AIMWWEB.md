# First Pilot — AIMWWeb

Target: `walidatiyaai2025-gif/AIMWWeb`

Bootstrap constraint: this control-center bootstrap does **not** modify AIMWWeb.

First exact step after Project Control Center self-audit: run `prompts/20-existing-project/20-discover-existing-project.md` against AIMWWeb.

The discovery must remain read-only and determine, from live GitHub evidence, remote branches, open/recently merged PRs, active Issues, releases/tags, unique commits, CI, QA evidence, and any existing governance files. It must not assume `main`, `master`, `develop`, or a named integration branch is current.

Only after a verified lineage report exists may Prompt 21 lock a baseline.
