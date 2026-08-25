# 20 — Discover Existing Project

PROMPT_ID: PCC-20
VERSION: 1.1.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: START_HERE_OR_PCC-32
NEXT_STEP: PCC-21
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Repository URL and read access to its live GitHub state.
- Access to this control plane and its governance/version laws.
- No assumption that any named branch or version file is authoritative.

## Mission

Perform a read-only live baseline discovery that preserves existing development and establishes the evidence needed for a safe version baseline.

## Mandatory live inspection

Fetch and inspect:

- current remote branches and their heads;
- open PRs and exact heads/bases;
- recently merged PRs and merge lineage;
- active Issues and delivery references;
- releases and tags;
- recent/unique commits and branch divergence;
- CI/workflow state at relevant exact SHAs;
- QA/release/customer-build evidence if present;
- existing governance/status/task/agent/control files.

Never blindly assume `main`, `master`, `develop`, `integration/current`, or similarly named branch is the actual current development lineage.

## VERSION BASELINE DISCOVERY

For any customer/user-visible product also inspect:

1. current application/customer-visible version if discoverable;
2. all package/project/manifest/version files that may act as version sources;
3. Git tags and release records and their exact SHAs;
4. deployed/customer version evidence if discoverable;
5. artifact names/build metadata/version endpoints/About screens where evidence exists;
6. conflicting version sources or reused version identities;
7. current release candidate/development version conventions.

Do not create `VERSION`, change manifests, retag history, or invent historical versions in this read-only step. Determine candidate `CURRENT_RELEASE_VERSION`, `TARGET_DEVELOPMENT_VERSION`, `VERSION_SOURCE`, tag/artifact conventions and `VERSION_BASELINE_CONFIDENCE` (`HIGH|MEDIUM|LOW|UNKNOWN`). If history is ambiguous, preserve the ambiguity explicitly.

Identify candidate production lineage separately from candidate development/integration lineage. Preserve all unique unmerged work and flag orphan, stale, duplicate and conflicting active branches without deleting/rewrite.

## Required output

Produce evidence-backed discovery report containing repository identity; candidate production/development branches+SHAs; open work graph; unique commits; PR/CI/QA/release state; governance maturity; **version baseline discovery** with sources/tags/releases/display evidence/conflicts/confidence; unknowns; risks; and exact evidence needed for PCC-21.

Do not modify target repository.
