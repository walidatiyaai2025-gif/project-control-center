# 01 — Self Audit

PROMPT_ID: PCC-01
VERSION: 1.4.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: PCC-00_OR_PCC-02
NEXT_STEP: PCC-02_OR_PILOT
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.4.0

## Must exist before running

- Completed PCC bootstrap/upgrade.
- `START_HERE.md`, prompt directories, policies, templates, schemas, portfolio files, orchestration files, dashboard files, and validation workflows.
- Read access to the exact control-plane HEAD being audited.

## Mission

Prove that a human with no previous chat history can operate the control plane safely and that fleet, version, feature-delivery and execution-output governance are enforceable representations, not documentation-only claims.

## Audit

Verify all mandatory paths exist and all prompt metadata is complete. Walk each START_HERE scenario end-to-end and confirm the operator can identify the correct project type, exact current prompt, next prompt, and whether writes are allowed.

Verify existing PCC data/work remains preserved; fleet collection/enrollment/baseline/reconciliation remain safe; immutable version identity remains enforced; no product repository was unintentionally modified; and the execution-output layer enforces structured final state rather than narration.

Required output-discipline checks:
- `OUTPUT_DISCIPLINE_POLICY: PASS/FAIL`
- `STRUCTURED_HANDOFF_ENFORCEMENT: PASS/FAIL`
- `ARTIFACT_PROVENANCE_GATE: PASS/FAIL`
- `NO_PREMATURE_QA_CONCLUSIONS: PASS/FAIL`
- `CONTRADICTORY_OUTPUT_GATE: PASS/FAIL`
- `SILENT_EXECUTION_DEFAULT: PASS/FAIL`

Run `python scripts/self_audit.py` and `python -m unittest scripts/test_control_plane.py scripts/test_feature_delivery.py scripts/test_fleet_control.py scripts/test_output_discipline.py -v` plus repository workflows where available.

## Output mode
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.

## Required output
Return the six output-discipline checks, overall PASS/FAIL, exact audited SHA, missing/invalid files, product-repository modification check, and next action.
