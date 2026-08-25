import json, pathlib, datetime
root=pathlib.Path(__file__).resolve().parents[1]
registry=json.loads((root/'portfolio/projects.yml').read_text())
observed=json.loads((root/'orchestration/observed-state.json').read_text()) if (root/'orchestration/observed-state.json').exists() else {'PROJECTS':[]}
obs={p.get('PROJECT_ID'):p for p in observed.get('PROJECTS',[]) if p.get('PROJECT_ID')}
projects=[]
for registered in registry.get('PROJECTS',[]):
    p=dict(registered); o=obs.get(p.get('PROJECT_ID'),{})
    if o:
        p['OBSERVED_POLICY_VERSION']=o.get('OBSERVED_POLICY_VERSION',p.get('OBSERVED_POLICY_VERSION')); p['DRIFT']=o.get('DRIFT',p.get('DRIFT',[]))
    projects.append(p)

def isum(key): return sum(int(p.get(key,0) or 0) for p in projects)
out={
 'CONTROL_PLANE_VERSION':registry.get('CONTROL_PLANE_VERSION'),
 'GENERATED_AT':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'TOTAL_PROJECTS':len(projects),'HEALTHY':sum(p.get('HEALTH')=='HEALTHY' for p in projects),'NEEDS_ATTENTION':sum(p.get('HEALTH')=='NEEDS_ATTENTION' for p in projects),'CRITICAL':sum(p.get('HEALTH')=='CRITICAL' for p in projects),
 'ACTIVE_TASKS':isum('ACTIVE_TASKS'),'WAITING_FOR_USER':isum('WAITING_FOR_USER'),'UNTRACKED_REQUESTS':isum('UNTRACKED_REQUESTS'),'VERSION_DRIFT_PROJECTS':sum(bool(p.get('DRIFT')) for p in projects),
 'TOTAL_REQUIREMENTS':isum('TOTAL_REQUIREMENTS'),'FEATURES_IMPLEMENTED_NOT_CONNECTED':isum('FEATURES_IMPLEMENTED_NOT_CONNECTED'),'FEATURES_CUSTOMER_READY':isum('FEATURES_CUSTOMER_READY'),'FEATURES_RELEASED':isum('FEATURES_RELEASED'),
 'SCREENS_TOTAL':isum('SCREENS_TOTAL'),'SCREENS_VISUAL_COMPLETE':isum('SCREENS_VISUAL_COMPLETE'),'SCREENS_FUNCTIONAL_COMPLETE':isum('SCREENS_FUNCTIONAL_COMPLETE'),'SCREENS_CUSTOMER_READY':isum('SCREENS_CUSTOMER_READY'),
 'INTEGRATION_GAPS':isum('INTEGRATION_GAPS'),'UNREACHABLE_SCREENS':isum('UNREACHABLE_SCREENS'),'BACKEND_ONLY_FEATURES':isum('BACKEND_ONLY_FEATURES'),'UI_ONLY_FEATURES':isum('UI_ONLY_FEATURES'),'MISSING_BINDINGS':isum('MISSING_BINDINGS'),'FALSE_DONE_FEATURES':isum('FALSE_DONE_FEATURES'),
 'PROJECTS':projects
}
(root/'portfolio/status/index.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
