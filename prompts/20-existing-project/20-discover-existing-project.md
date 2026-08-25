# 20 — Discover Existing Project

PROMPT_ID: PCC-20
VERSION: 1.0.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: START_HERE_OR_PCC-32
NEXT_STEP: PCC-21
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Repository URL and read access to its live GitHub state.
- Access to this control plane and its governance laws.
- No assumption that any named branch is the true development base.

## Mission

Perform a read-only live baseline discovery that preserves existing development.

## Mandatory live inspection

Fetch and inspect:

- current remote branches and their heads;
- open PRs and their exact heads/bases;
- recently merged PRs and merge lineage;
- active Issues and delivery references;
- releases and tags;
- recent/unique commits and branch divergence;
- CI/workflow state at relevant exact SHAs;
- QA/release evidence if present;
- existing governance/status/task/agent/control files.

Never blindly assume `main`, `master`, `develop`, `integration/current`, or any similarly named branch is the actual current development lineage.

Identify candidate production lineage separately from candidate development/integration lineage. Preserve all unique unmerged work and flag orphan, stale, duplicate, and conflicting active branches without deleting or rewriting anything.

## Required output

Produce an evidence-backed discovery report containing: repository identity; candidate production branch/SHA; candidate canonical development branch/SHA; open work graph; unique commits; PR/CI/QA/release state; governance maturity; unknowns; risks; and the exact evidence needed to lock the baseline.

Do not modify the target repository. Next step is PCC-21 only after the lineage is sufficiently verified.
