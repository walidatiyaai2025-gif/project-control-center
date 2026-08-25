# 52 — Overlap Audit

PROMPT_ID: PCC-52
VERSION: 1.4.0
APPLIES_TO: SUSPECTED_DUPLICATE_ACTIVE_WORK
PREVIOUS_STEP: PCC-40_OR_PCC-53
NEXT_STEP: PCC-53_OR_TARGETED_RECOVERY
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running
- Two or more candidate Tasks/branches/PRs/requests suspected to implement the same logical scope.
- Read access to their exact heads, diffs, requirements, and status.

## Mission
Detect logical duplicate work before it creates competing branches or conflicting releases.

## Audit
Compare requirement intent, acceptance criteria, files/components, APIs/data contracts, branch ancestry, commits, PR descriptions/reviews, and current integration presence. Distinguish legitimate parallel subtasks from duplicate implementations. Recommend one canonical Task/branch based on traceability, implementation quality/evidence, and preserved unique work. Make no destructive writes.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return a structured final handoff with exact candidate HEAD identities, overlap classification, recommended canonical task/branch, unique work to preserve, evidence and NEXT_ACTION. Do not stream comparison narration.
