# 52 — Overlap Audit

PROMPT_ID: PCC-52
VERSION: 1.0.0
APPLIES_TO: SUSPECTED_DUPLICATE_ACTIVE_WORK
PREVIOUS_STEP: PCC-40_OR_PCC-53
NEXT_STEP: PCC-53_OR_TARGETED_RECOVERY
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Two or more candidate Tasks/branches/PRs/requests suspected to implement the same logical scope.
- Read access to their exact heads, diffs, requirements, and status.

## Mission

Detect logical duplicate work before it creates competing branches or conflicting releases.

## Audit

Compare requirement intent, acceptance criteria, files/components, APIs/data contracts, branch ancestry, commits, PR descriptions/reviews, and current integration presence. Distinguish legitimate parallel subtasks from duplicate implementations.

Recommend one canonical Task/branch based on traceability, implementation quality/evidence, and preserved unique work—not Worker identity. Identify commits that must be retained from non-canonical branches.

Make no destructive writes in this audit.

## Required output

Return overlap matrix, SAME_TASK/PARTIAL_OVERLAP/INDEPENDENT classification, recommended canonical task/branch, unique work to preserve, and exact recovery/reconciliation prompt to run next.
