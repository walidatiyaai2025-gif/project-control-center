import json, pathlib, datetime
root=pathlib.Path(__file__).resolve().parents[1]
registry=json.loads((root/'portfolio/projects.yml').read_text())
observed=json.loads((root/'orchestration/observed-state.json').read_text()) if (root/'orchestration/observed-state.json').exists() else {'PROJECTS':[]}
obs={p.get('PROJECT_ID'):p for p in observed.get('PROJECTS',[]) if p.get('PROJECT_ID')}
projects=[]
for registered in registry.get('PROJECTS',[]):
    p=dict(registered)
    o=obs.get(p.get('PROJECT_ID'),{})
    if o:
        p['OBSERVED_POLICY_VERSION']=o.get('OBSERVED_POLICY_VERSION',p.get('OBSERVED_POLICY_VERSION'))
        p['DRIFT']=o.get('DRIFT',p.get('DRIFT',[]))
    projects.append(p)
out={
 'CONTROL_PLANE_VERSION':registry.get('CONTROL_PLANE_VERSION'),
 'GENERATED_AT':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'TOTAL_PROJECTS':len(projects),
 'HEALTHY':sum(p.get('HEALTH')=='HEALTHY' for p in projects),
 'NEEDS_ATTENTION':sum(p.get('HEALTH')=='NEEDS_ATTENTION' for p in projects),
 'CRITICAL':sum(p.get('HEALTH')=='CRITICAL' for p in projects),
 'ACTIVE_TASKS':sum(int(p.get('ACTIVE_TASKS',0)) for p in projects),
 'WAITING_FOR_USER':sum(int(p.get('WAITING_FOR_USER',0)) for p in projects),
 'UNTRACKED_REQUESTS':sum(int(p.get('UNTRACKED_REQUESTS',0)) for p in projects),
 'VERSION_DRIFT_PROJECTS':sum(bool(p.get('DRIFT')) for p in projects),
 'PROJECTS':projects
}
(root/'portfolio/status/index.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
