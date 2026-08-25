import json, pathlib, datetime
root=pathlib.Path(__file__).resolve().parents[1]
registry=json.loads((root/'portfolio/projects.yml').read_text())
observed=json.loads((root/'orchestration/observed-state.json').read_text()) if (root/'orchestration/observed-state.json').exists() else {'PROJECTS':[]}
obs={p.get('PROJECT_ID'):p for p in observed.get('PROJECTS',[]) if p.get('PROJECT_ID')}
live_path=root/'portfolio/status/fleet-live.json'
live=json.loads(live_path.read_text()) if live_path.exists() else {'PROJECTS':[]}
live_map={p.get('PROJECT_ID'):p for p in live.get('PROJECTS',[]) if p.get('PROJECT_ID')}
projects=[]
for registered in registry.get('PROJECTS',[]):
    p=dict(registered); o=obs.get(p.get('PROJECT_ID'),{}); l=live_map.get(p.get('PROJECT_ID'),{})
    p['COLLECTOR_RESULT']=l.get('COLLECTOR_RESULT',o.get('COLLECTOR_RESULT','UNKNOWN'))
    p['DISCOVERY_COMPLETE']=bool(l.get('DISCOVERY_COMPLETE',o.get('DISCOVERY_COMPLETE')))
    p['BASELINE_LOCKED']=bool(l.get('BASELINE_LOCKED',o.get('BASELINE_LOCKED')))
    p['DEFAULT_BRANCH']=l.get('DEFAULT_BRANCH',o.get('DEFAULT_BRANCH',p.get('PRODUCTION_BRANCH')))
    p['DEFAULT_BRANCH_SHA']=l.get('DEFAULT_BRANCH_SHA',o.get('DEFAULT_BRANCH_SHA',p.get('PRODUCTION_SHA')))
    p['DEFAULT_BRANCH_PROTECTED']=bool(l.get('DEFAULT_BRANCH_PROTECTED',o.get('DEFAULT_BRANCH_PROTECTED')))
    p['BRANCH_COUNT']=l.get('BRANCH_COUNT',o.get('BRANCH_COUNT',0))
    p['OPEN_PR_COUNT']=l.get('OPEN_PR_COUNT',o.get('OPEN_PR_COUNT',0))
    p['RELEASE_COUNT']=l.get('RELEASE_COUNT',o.get('RELEASE_COUNT',0))
    p['OBSERVED_POLICY_VERSION']=o.get('OBSERVED_POLICY_VERSION',p.get('OBSERVED_POLICY_VERSION'))
    p['DRIFT']=l.get('DRIFT',o.get('DRIFT',p.get('DRIFT',[])))
    p['TARGET_MUTATED']=bool(o.get('TARGET_MUTATED',False))
    projects.append(p)
def isum(key): return sum(int(p.get(key,0) or 0) for p in projects)
out={
 'CONTROL_PLANE_VERSION':registry.get('CONTROL_PLANE_VERSION'),
 'GENERATED_AT':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'TOTAL_PROJECTS':len(projects),
 'COLLECTION_PASS':sum(p.get('COLLECTOR_RESULT')=='PASS' for p in projects),
 'DISCOVERED':sum(bool(p.get('DISCOVERY_COMPLETE')) for p in projects),
 'BASELINE_LOCKED':sum(bool(p.get('BASELINE_LOCKED')) for p in projects),
 'OBSERVE_PROJECTS':sum(p.get('POLICY_ENFORCEMENT_MODE')=='OBSERVE' for p in projects),
 'WARN_PROJECTS':sum(p.get('POLICY_ENFORCEMENT_MODE')=='WARN' for p in projects),
 'CANARY_PROJECTS':sum(bool(p.get('CANARY')) for p in projects),
 'ENFORCE_PROJECTS':sum(p.get('POLICY_ENFORCEMENT_MODE')=='ENFORCE' for p in projects),
 'DRIFT_PROJECTS':sum(bool(p.get('DRIFT')) for p in projects),
 'UNPROTECTED_DEFAULT_BRANCHES':sum(not p.get('DEFAULT_BRANCH_PROTECTED') for p in projects if p.get('DEFAULT_BRANCH')),
 'TOTAL_BRANCHES':sum(int(p.get('BRANCH_COUNT',0) or 0) for p in projects),
 'TOTAL_OPEN_PRS':sum(int(p.get('OPEN_PR_COUNT',0) or 0) for p in projects if isinstance(p.get('OPEN_PR_COUNT',0),(int,float))),
 'TOTAL_REQUIREMENTS':isum('TOTAL_REQUIREMENTS'),
 'FEATURES_IMPLEMENTED_NOT_CONNECTED':isum('FEATURES_IMPLEMENTED_NOT_CONNECTED'),
 'FEATURES_CUSTOMER_READY':isum('FEATURES_CUSTOMER_READY'),
 'FEATURES_RELEASED':isum('FEATURES_RELEASED'),
 'INTEGRATION_GAPS':isum('INTEGRATION_GAPS'),
 'FALSE_DONE_FEATURES':isum('FALSE_DONE_FEATURES'),
 'UNREACHABLE_SCREENS':isum('UNREACHABLE_SCREENS'),
 'BACKEND_ONLY_FEATURES':isum('BACKEND_ONLY_FEATURES'),
 'UI_ONLY_FEATURES':isum('UI_ONLY_FEATURES'),
 'MISSING_BINDINGS':isum('MISSING_BINDINGS'),
 'PROJECTS':projects
}
(root/'portfolio/status/index.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
