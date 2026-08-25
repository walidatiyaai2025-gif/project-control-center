# 01 — Self Audit

PROMPT_ID: PCC-01
VERSION: 1.1.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: PCC-00_OR_PCC-02
NEXT_STEP: PCC-02_OR_PILOT
REQUIRES_WRITE_ACCESS: false
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- Completed PCC bootstrap/upgrade.
- `START_HERE.md`, prompt directories, policies, templates, schemas, portfolio files, orchestration files, dashboard files, and validation workflows.
- Read access to the exact control-plane HEAD being audited.

## Mission

Prove that a human with no previous chat history can operate the control plane safely and that v1.1.0 orchestration/version controls are enforceable representations, not documentation-only claims.

## Audit

Verify all mandatory paths exist and all prompt metadata is complete. Walk each START_HERE scenario end-to-end and confirm the operator can identify the correct project type, exact current prompt, next prompt, and whether writes are allowed.

Prove the operator can onboard a new project; migrate an active existing project without assuming a branch/version; inventory/reactivate legacy; dispatch/continue/QA/integrate/release/deliver; recover stale/orphan/overlap; reconcile project state; register/audit/prioritize/report a portfolio; and identify the single authoritative status publisher.

Additionally verify:

- existing PCC data/work remains preserved through upgrade;
- central enrollment, desired-vs-observed state, compatibility scan, dry run, OBSERVE/WARN/CANARY/ENFORCE, rollout waves, rollback metadata, drift detection, safe self-healing boundary, concurrency, idempotency, failure isolation, auth abstraction, audit ledger and portfolio aggregation are represented;
- `IMMUTABLE_CUSTOMER_VERSION_POLICY` exists;
- duplicate version/different-SHA release is rejected;
- official artifact without its version is rejected;
- display/package version mismatch is detected as VERSION_DRIFT;
- customer-visible version requirement is represented;
- Task `TARGET_VERSION` and `RELEASED_IN_VERSION` exist;
- version manifest identity exists;
- release rollback records previous known-good version/SHA;
- existing-project migration discovers version conventions before enforcement;
- no product repository was unintentionally modified by the PCC bootstrap/upgrade.

Run `python scripts/self_audit.py` and `python -m unittest scripts/test_control_plane.py -v` plus repository workflows where available.

## Required output

Return PASS/FAIL per capability, exact audited SHA, missing/invalid files, any ambiguous operator path, product-repository modification check, and whether the control plane is `READY_FOR_FIRST_PILOT`.
