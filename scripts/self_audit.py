from pathlib import Path
import json,sys

root=Path(__file__).resolve().parents[1]
errors=[]

def need(path):
    if not (root/path).exists(): errors.append(f'missing {path}')

def contain(path, values):
    p=root/path
    if not p.exists(): return
    text=p.read_text()
    for value in values:
        if value not in text: errors.append(f'{path} missing required content: {value}')

required_files=[
 'README.md','START_HERE.md','VERSION','portfolio/projects.yml','portfolio/priorities.yml',
 'portfolio/status/index.json','dashboard/index.html','dashboard/app.js','dashboard/build_portfolio.py',
 'policies/GOVERNANCE_LAWS.md','policies/TASK_LIFECYCLE_AND_LEASE.md',
 'templates/PROJECT_STATUS.yml','templates/TASK.yml','templates/REQUIREMENT.yml','templates/WORKER_LEASE.yml',
 'schemas/project.schema.json','schemas/project-status.schema.json','schemas/task.schema.json','schemas/requirement.schema.json',
 '.github/CODEOWNERS','.github/pull_request_template.md',
 '.github/workflows/control-plane-validation.yml','.github/workflows/portfolio-dashboard.yml'
]
for p in required_files: need(p)

mandatory_prompts=[
 '00-control-center/00-bootstrap-control-center.md','00-control-center/01-self-audit.md','00-control-center/02-upgrade-control-plane.md',
 '10-new-project/10-initialize-new-project.md','10-new-project/11-register-new-project.md','10-new-project/12-new-project-readiness-audit.md',
 '20-existing-project/20-discover-existing-project.md','20-existing-project/21-baseline-lock.md','20-existing-project/22-reconcile-existing-work.md','20-existing-project/23-install-control-plane.md','20-existing-project/24-enable-enforcement.md','20-existing-project/25-existing-project-acceptance.md',
 '30-legacy-project/30-legacy-inventory.md','30-legacy-project/31-archive-or-maintenance.md','30-legacy-project/32-reactivate-project.md',
 '40-daily-operations/40-dispatcher.md','40-daily-operations/41-task-worker.md','40-daily-operations/42-continuation-worker.md','40-daily-operations/43-qa-worker.md','40-daily-operations/44-integration-lead.md','40-daily-operations/45-release-lead.md','40-daily-operations/46-user-delivery-lead.md',
 '50-recovery/50-stale-task-recovery.md','50-recovery/51-orphan-recovery.md','50-recovery/52-overlap-audit.md','50-recovery/53-full-reconciliation.md',
 '60-portfolio/60-register-project.md','60-portfolio/61-portfolio-audit.md','60-portfolio/62-priority-controller.md','60-portfolio/63-executive-status.md'
]
metadata=['PROMPT_ID','VERSION','APPLIES_TO','PREVIOUS_STEP','NEXT_STEP','REQUIRES_WRITE_ACCESS','CONTROL_PLANE_VERSION']
for rel in mandatory_prompts:
    p=root/'prompts'/rel
    if not p.exists():
        errors.append(f'missing prompts/{rel}')
        continue
    text=p.read_text()
    for key in metadata:
        if f'{key}:' not in text: errors.append(f'prompts/{rel} missing {key}')
    if '## Must exist before running' not in text: errors.append(f'prompts/{rel} missing prerequisites section')

actual_prompts=sorted((root/'prompts').glob('**/*.md'))
if len(actual_prompts)!=30: errors.append(f'expected 30 prompts, found {len(actual_prompts)}')

contain('START_HERE.md',[
 '10-initialize-new-project.md','11-register-new-project.md','12-new-project-readiness-audit.md',
 '20-discover-existing-project.md','21-baseline-lock.md','22-reconcile-existing-work.md','23-install-control-plane.md','24-enable-enforcement.md','25-existing-project-acceptance.md',
 '30-legacy-inventory.md','31-archive-or-maintenance.md','32-reactivate-project.md','REQUIRES_WRITE_ACCESS','DELIVERY / CONTROL LEAD'
])
contain('prompts/20-existing-project/20-discover-existing-project.md',[
 'current remote branches','open PRs','recently merged PRs','active Issues','releases and tags','unique commits','CI/workflow','governance/status','Never blindly assume'
])
contain('policies/TASK_LIFECYCLE_AND_LEASE.md',[
 'AVAILABLE','READY','CLAIMED','IN_PROGRESS','BLOCKED','STALE','RECLAIMABLE','READY_FOR_REVIEW','READY_FOR_QA','QA_PASS','INTEGRATED','RELEASED','DONE'
])
contain('templates/PROJECT_STATUS.yml',[
 'REQUESTED_SCOPE','COMPLETED_SCOPE','IN_PROGRESS','BLOCKED','QA','INTEGRATED','RELEASED','WAITING_FOR_USER','STALE_RECLAIMABLE','ORPHAN_WORK','DUPLICATE_ACTIVE_WORK','PRODUCTION_SHA','CANONICAL_DEVELOPMENT_SHA','CANONICAL_INTEGRATION_SHA','LATEST_RELEASE','LAST_SYNC'
])
contain('policies/GOVERNANCE_LAWS.md',[
 'NO REQUEST WITHOUT TASK ID','NO CODING WITHOUT A TASK','NO NEW TASK BEFORE DUPLICATE CHECK','STALE WORK IS RECLAIMED, NOT RECREATED','CONTINUATION FIRST. NEW BRANCH LAST','OFFICIAL PROJECT STATUS MUST HAVE ONE CANONICAL SOURCE','NEVER DISCARD UNIQUE UNMERGED WORK','UNTRACKED REQUESTS MUST TREND TO ZERO'
])

for p in ['portfolio/projects.yml','portfolio/priorities.yml','portfolio/status/index.json','schemas/project.schema.json','schemas/project-status.schema.json','schemas/task.schema.json','schemas/requirement.schema.json','templates/PROJECT_STATUS.yml','templates/TASK.yml','templates/REQUIREMENT.yml','templates/WORKER_LEASE.yml']:
    try: json.loads((root/p).read_text())
    except Exception as e: errors.append(f'{p} invalid JSON-compatible YAML/JSON: {e}')

version=(root/'VERSION').read_text().strip() if (root/'VERSION').exists() else ''
if version!='v1.0.0': errors.append(f'unexpected VERSION {version!r}')

print(f'CONTROL_PLANE_VERSION={version}')
print(f'prompts={len(actual_prompts)} mandatory_prompts={len(mandatory_prompts)} errors={len(errors)}')
for e in errors: print('ERROR',e)
sys.exit(1 if errors else 0)
