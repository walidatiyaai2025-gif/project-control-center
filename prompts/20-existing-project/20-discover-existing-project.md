# 20 — Discover Existing Project

PROMPT_ID: PCC-20
VERSION: 1.2.0
APPLIES_TO: ACTIVE_EXISTING_PROJECT
PREVIOUS_STEP: START_HERE_OR_PCC-32
NEXT_STEP: PCC-21
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.6.0

## Must exist before running

- Repository URL and read access to its live GitHub state.
- Access to PCC constitution/governance/version laws.
- No assumption that any named branch, client name, or version file is authoritative.

## Mission

Perform read-only live baseline discovery, including automatic project-family/variant discovery, while preserving existing development.

## Mandatory live inspection

Fetch/inspect current branches/heads, open/merged PR lineage, Issues, releases/tags, unique commits/divergence, CI, QA/release evidence, governance/status/task/agent/control files, repository tree, configuration/manifests, domains/deployment clues, branding/client identifiers, and historical names.

Classify candidate `STANDALONE` vs `PRODUCT_FAMILY`. For any known/owner-declared variants, determine candidate aliases, relationships, implementation locations, and whether each boundary is `MAPPED`, `EXTERNAL_REPOSITORY`, `UNRESOLVED`, or `UNMATERIALIZED`.

Do not infer variant identity from branch names and do not create missing variant folders/branches in this read-only step.

Perform normal version baseline discovery for customer-visible products. Preserve ambiguity explicitly.

Identify production lineage separately from development/integration lineage and preserve all unique unmerged work.

## Required output

Produce evidence-backed discovery report containing repository identity; project-model classification; family/variant inventory with implementation-location evidence and routing blockers; candidate production/development branches+SHAs; open work graph; CI/QA/release state; governance maturity; version baseline; unknowns/risks; and exact evidence needed for PCC-21.

Do not modify target repository.
