# 01 — Self Audit

PROMPT_ID: PCC-01
VERSION: 1.0.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: PCC-00
NEXT_STEP: PCC-02_OR_PILOT
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- Completed PCC-00 bootstrap.
- `START_HERE.md`, prompt directories, policies, templates, schemas, portfolio files, dashboard files, and validation workflow.
- Read access to the exact control-plane HEAD being audited.

## Mission

Prove that a human with no previous chat history can operate the control plane safely.

## Audit

Verify all mandatory paths exist and all prompt metadata is complete. Walk each START_HERE scenario end-to-end and confirm the operator can identify the correct project type, exact current prompt, next prompt, and whether writes are allowed.

Specifically prove the operator can: onboard a new project; migrate an active existing project without assuming a branch; inventory a legacy project; reactivate legacy through existing-project discovery; dispatch/continue/QA/integrate/release/deliver work; recover stale/orphan work; detect overlap; reconcile project state; register/audit/prioritize/report a portfolio; and identify the single authoritative status publisher.

Validate the 16 governance laws, worker lifecycle states, project maturity states, canonical status fields, portfolio fields, traceability chain, official-build rule, and control-plane version marker.

Run repository validation scripts/workflows where available. Report failures as concrete file/rule defects, not generic comments.

## Required output

Return PASS/FAIL per capability, exact audited SHA, missing/invalid files, any ambiguous operator path, and whether the control plane is `READY_FOR_FIRST_PILOT`.
