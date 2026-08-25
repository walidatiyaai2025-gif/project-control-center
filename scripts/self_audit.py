from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[1]
errors=[]
def need(path):
    if not (root/path).exists(): errors.append(f"missing {path}")
def contain(path,values):
    p=root/path
    if not p.exists(): return
    text=p.read_text(encoding="utf-8")
    for v in values:
        if v not in text: errors.append(f"{path} missing required content: {v}")
def has(path,*values):
    p=root/path
    if not p.exists(): return False
    text=p.read_text(encoding="utf-8")
    return all(v in text for v in values)

required=[
"README.md","START_HERE.md","VERSION","portfolio/projects.yml","portfolio/priorities.yml","portfolio/status/index.json","portfolio/version-history/README.md",
"dashboard/index.html","dashboard/app.js","dashboard/build_portfolio.py",
"policies/GOVERNANCE_LAWS.md","policies/TASK_LIFECYCLE_AND_LEASE.md","policies/CENTRAL_ORCHESTRATION_POLICY.md","policies/IMMUTABLE_PRODUCT_VERSION_POLICY.md","policies/END_TO_END_FEATURE_DELIVERY_POLICY.md","policies/FLEET_CONTROL_POLICY.md","policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md",
"orchestration/desired-state.json","orchestration/observed-state.json","orchestration/audit-ledger.json","orchestration/baselines/AIMWWEB.json","orchestration/reconciliation/AIMWWEB.json",
"scripts/version_governance.py","scripts/orchestrator.py","scripts/enrollment_controller.py","scripts/feature_delivery_audit.py","scripts/github_fleet_client.py","scripts/fleet_control.py","scripts/self_protection.py","scripts/output_discipline.py",
"scripts/test_control_plane.py","scripts/test_feature_delivery.py","scripts/test_fleet_control.py","scripts/test_output_discipline.py",
"schemas/worker-handoff.schema.json","schemas/qa-handoff.schema.json","schemas/ci-handoff.schema.json","schemas/visual-qa-handoff.schema.json","schemas/integration-handoff.schema.json","schemas/release-handoff.schema.json",
".github/CODEOWNERS",".github/pull_request_template.md",".github/workflows/control-plane-validation.yml",".github/workflows/portfolio-dashboard.yml",".github/workflows/central-orchestrator.yml",".github/workflows/fleet-control.yml",".github/workflows/reusable-version-governance.yml",".github/workflows/reusable-feature-delivery-governance.yml",
"docs/FLEET_CONTROL_CLOSURE_v1.3.0.md","docs/EXECUTION_OUTPUT_DISCIPLINE_ADDON_v1.4.0.md"]
for p in required: need(p)
mandatory_prompts=['00-control-center/00-bootstrap-control-center.md','00-control-center/01-self-audit.md','00-control-center/02-upgrade-control-plane.md','10-new-project/10-initialize-new-project.md','10-new-project/11-register-new-project.md','10-new-project/12-new-project-readiness-audit.md','20-existing-project/20-discover-existing-project.md','20-existing-project/21-baseline-lock.md','20-existing-project/22-reconcile-existing-work.md','20-existing-project/23-install-control-plane.md','20-existing-project/24-enable-enforcement.md','20-existing-project/25-existing-project-acceptance.md','30-legacy-project/30-legacy-inventory.md','30-legacy-project/31-archive-or-maintenance.md','30-legacy-project/32-reactivate-project.md','40-daily-operations/40-dispatcher.md','40-daily-operations/41-task-worker.md','40-daily-operations/42-continuation-worker.md','40-daily-operations/43-qa-worker.md','40-daily-operations/44-integration-lead.md','40-daily-operations/45-release-lead.md','40-daily-operations/46-user-delivery-lead.md','50-recovery/50-stale-task-recovery.md','50-recovery/51-orphan-recovery.md','50-recovery/52-overlap-audit.md','50-recovery/53-full-reconciliation.md','60-portfolio/60-register-project.md','60-portfolio/61-portfolio-audit.md','60-portfolio/62-priority-controller.md','60-portfolio/63-executive-status.md']
metadata=['PROMPT_ID','VERSION','APPLIES_TO','PREVIOUS_STEP','NEXT_STEP','REQUIRES_WRITE_ACCESS','CONTROL_PLANE_VERSION']
for rel in mandatory_prompts:
    p=root/'prompts'/rel
    if not p.exists(): errors.append(f"missing prompts/{rel}"); continue
    text=p.read_text(encoding="utf-8")
    for k in metadata:
        if f"{k}:" not in text: errors.append(f"prompts/{rel} missing {k}")
    if '## Must exist before running' not in text: errors.append(f"prompts/{rel} missing prerequisites section")
actual=list((root/'prompts').glob('**/*.md'))
if len(actual)!=30: errors.append(f"expected 30 prompts, found {len(actual)}")
managed_output_prompts=['00-control-center/01-self-audit.md','40-daily-operations/41-task-worker.md','40-daily-operations/42-continuation-worker.md','40-daily-operations/43-qa-worker.md','40-daily-operations/44-integration-lead.md','40-daily-operations/45-release-lead.md','40-daily-operations/46-user-delivery-lead.md','50-recovery/50-stale-task-recovery.md','50-recovery/51-orphan-recovery.md','50-recovery/52-overlap-audit.md','50-recovery/53-full-reconciliation.md']
for rel in managed_output_prompts:
    contain('prompts/'+rel,["OUTPUT MODE: SILENT EXECUTION","Do not narrate investigation.","Do not send intermediate hypotheses."])
contain("policies/END_TO_END_FEATURE_DELIVERY_POLICY.md",["CODE EXISTS != FEATURE COMPLETE","IMPLEMENTED_NOT_CONNECTED","FALSE_DONE_FEATURES = 0"])
contain("policies/FLEET_CONTROL_POLICY.md",["OBSERVE -> WARN -> CANARY -> ENFORCE","read before write","ORPHAN_CANDIDATES","break-glass","write-capable"])
contain("policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md",["SILENT_EXECUTION_BY_DEFAULT: TRUE","Exact-head evidence gate","Artifact provenance gate","No-premature-finding law","Contradiction gate","WORKER_HANDOFF","VISUAL_QA_HANDOFF"])
contain("scripts/output_discipline.py",["validate_handoff","unsupported DONE","artifact SHA does not match exact HEAD","stale/unverified visual artifact cannot produce authoritative QA","contradictory CI states"])
contain("scripts/github_fleet_client.py",["paginate","X-RateLimit-Remaining","Retry-After","write_capable","protect_branch"])
contain("scripts/self_protection.py",["MAIN_PROTECTION_NOT_CONFIGURED","REPOSITORY_ADMIN_WRITE_CREDENTIAL_REQUIRED","Control Plane Validation / self-audit"])
contain("scripts/fleet_control.py",["collect_project","lock_baseline","reconcile_existing_work","migration_plan","apply_policy_sync","stale_task_recovery","orphan_audit","append_ledger","acquire_lock"])
contain(".github/workflows/fleet-control.yml",["Live GitHub fleet collection","concurrency:","PCC_GITHUB_TOKEN"])
contain(".github/workflows/portfolio-dashboard.yml",["Detect Pages site","pcc-dashboard-static-","actions/configure-pages@v5","steps.pages_preflight.outputs.enabled == 'true'","actions/deploy-pages@v4","PAGES=EXTERNAL_BLOCKER"])
contain("portfolio/projects.yml",["AIMWWEB","PENDING_DISCOVERY","OBSERVE","WRITE_AUTHORIZED"])
contain("orchestration/reconciliation/AIMWWEB.json",["UNIQUE_WORK_PRESERVATION_REQUIRED","TARGET_MUTATED"])
json_files=["portfolio/projects.yml","portfolio/priorities.yml","portfolio/status/index.json","orchestration/desired-state.json","orchestration/observed-state.json","orchestration/audit-ledger.json","orchestration/baselines/AIMWWEB.json","orchestration/reconciliation/AIMWWEB.json","orchestration/policy-catalog.json"]
for p in json_files:
    try: json.loads((root/p).read_text())
    except Exception as e: errors.append(f"{p} invalid JSON-compatible YAML/JSON: {e}")
status_checks={
"OUTPUT_DISCIPLINE_POLICY":has("policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md","POLICY_ID: EXECUTION_OUTPUT_DISCIPLINE_POLICY","SILENT_EXECUTION_BY_DEFAULT: TRUE"),
"STRUCTURED_HANDOFF_ENFORCEMENT":all((root/p).exists() for p in ["schemas/worker-handoff.schema.json","schemas/qa-handoff.schema.json","schemas/ci-handoff.schema.json","schemas/visual-qa-handoff.schema.json","schemas/integration-handoff.schema.json","schemas/release-handoff.schema.json","scripts/output_discipline.py"]),
"ARTIFACT_PROVENANCE_GATE":has("policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md","Artifact provenance gate","STALE_OR_UNVERIFIED_ARTIFACT") and has("schemas/visual-qa-handoff.schema.json","PROVENANCE_VERIFIED","CANDIDATE_SOURCE_SHA"),
"NO_PREMATURE_QA_CONCLUSIONS":has("policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md","No-premature-finding law","Raw signals are not conclusions"),
"CONTRADICTORY_OUTPUT_GATE":has("scripts/output_discipline.py","contradictory CI states","QA PASS with failed gates"),
"SILENT_EXECUTION_DEFAULT":has("policies/EXECUTION_OUTPUT_DISCIPLINE_POLICY.md","SILENT_EXECUTION_BY_DEFAULT: TRUE") and all(has('prompts/'+p,"OUTPUT MODE: SILENT EXECUTION") for p in managed_output_prompts)}
for k,v in status_checks.items():
    if not v: errors.append(f"{k} failed")
version=(root/"VERSION").read_text().strip()
if version!="v1.4.0": errors.append(f"unexpected VERSION {version!r}")
print(f"CONTROL_PLANE_VERSION={version}")
print(f"prompts={len(actual)} mandatory_prompts={len(mandatory_prompts)} errors={len(errors)}")
for k,v in status_checks.items(): print(f"{k}: {'PASS' if v else 'FAIL'}")
for e in errors: print("ERROR",e)
sys.exit(1 if errors else 0)
