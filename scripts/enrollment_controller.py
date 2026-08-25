#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

MODES={"OBSERVE","WARN","CANARY","ENFORCE"}

# v1.2 public API contract. Do not expand this set: legacy 2-argument callers
# must remain valid without fleet-only metadata.
LEGACY_REQUIRED_FIELDS=[
    "PROJECT_ID",
    "REPOSITORY",
    "CONTROL_PLANE_VERSION",
    "POLICY_ENFORCEMENT_MODE",
    "VERSION_POLICY",
    "VERSION_SOURCE",
]

# v1.3 fleet enrollment contract. Modern 3-argument callers are intentionally
# held to the complete fleet metadata requirements.
FLEET_REQUIRED_FIELDS={
    "PROJECT_ID",
    "DISPLAY_NAME",
    "REPOSITORY",
    "ENROLLMENT_STATE",
    "DISCOVERY_STATE",
    "POLICY_ENFORCEMENT_MODE",
    "ROLLOUT_WAVE",
}

_UNSET=object()

def load(path): return json.loads(Path(path).read_text())
def dump(path,doc): Path(path).write_text(json.dumps(doc,indent=2)+"\n")
def by_id(doc): return {p.get("PROJECT_ID"):p for p in doc.get("PROJECTS",[]) if p.get("PROJECT_ID")}

def desired_from(profile):
    keys=["PROJECT_ID","REPOSITORY","CONTROL_PLANE_VERSION","DESIRED_POLICY_VERSION","POLICY_ENFORCEMENT_MODE","ROLLOUT_WAVE","CANARY","WRITE_AUTHORIZED","CANONICAL_DEVELOPMENT_LINEAGE","AUTH_PROVIDER","VERSION_POLICY","VERSION_SOURCE","MANAGED_FILES","REQUIRE_DEFAULT_BRANCH_PROTECTION","BREAK_GLASS","POLICY_EXCEPTIONS"]
    return {k:profile.get(k) for k in keys if k in profile}

def _legacy_plan(profile,registry):
    """Preserve the v1.2 two-argument enrollment planning contract exactly."""
    missing=[k for k in LEGACY_REQUIRED_FIELDS if k not in profile]
    if missing:
        return {"RESULT":"BLOCKED","MISSING":missing}
    pid=profile["PROJECT_ID"]
    existing=next((p for p in registry.get("PROJECTS",[]) if p.get("PROJECT_ID")==pid),None)
    if existing==profile:
        return {"RESULT":"NOOP","PROJECT_ID":pid,"REPOSITORY":profile["REPOSITORY"]}
    if existing and existing.get("REPOSITORY")!=profile.get("REPOSITORY"):
        return {"RESULT":"BLOCKED","PROJECT_ID":pid,"REASON":"PROJECT_ID_REPOSITORY_CONFLICT"}
    return {
        "RESULT":"PLANNED_UPDATE" if existing else "PLANNED_ENROLLMENT",
        "PROJECT_ID":pid,
        "REPOSITORY":profile["REPOSITORY"],
        "PROFILE":profile,
    }

def _fleet_plan(profile,registry,desired):
    """v1.3 fleet-control enrollment validation and desired-state semantics."""
    if not isinstance(desired,dict):
        return {"RESULT":"BLOCKED","REASON":"DESIRED_STATE_REQUIRED","TARGET_MUTATED":False}
    missing=sorted(FLEET_REQUIRED_FIELDS-set(profile))
    if missing: return {"RESULT":"BLOCKED","MISSING":missing,"TARGET_MUTATED":False}
    if profile.get("POLICY_ENFORCEMENT_MODE") not in MODES: return {"RESULT":"BLOCKED","REASON":"INVALID_MODE","TARGET_MUTATED":False}
    pid=profile["PROJECT_ID"]
    r=by_id(registry).get(pid); d=by_id(desired).get(pid); want=desired_from(profile)
    if r and r.get("REPOSITORY")!=profile.get("REPOSITORY"): return {"RESULT":"BLOCKED","REASON":"PROJECT_ID_REPOSITORY_CONFLICT","TARGET_MUTATED":False}
    if d and d.get("REPOSITORY")!=profile.get("REPOSITORY"): return {"RESULT":"BLOCKED","REASON":"DESIRED_STATE_REPOSITORY_CONFLICT","TARGET_MUTATED":False}
    result="NOOP" if r==profile and d==want else ("PLANNED_UPDATE" if r or d else "PLANNED_ENROLLMENT")
    return {"RESULT":result,"PROJECT_ID":pid,"REPOSITORY":profile["REPOSITORY"],"TARGET_MUTATED":False}

def plan(profile,registry,desired=_UNSET):
    # The sentinel distinguishes the legacy two-argument API from the modern
    # three-argument API. Explicit desired=None is therefore modern and blocked.
    if desired is _UNSET:
        return _legacy_plan(profile,registry)
    return _fleet_plan(profile,registry,desired)

def apply(profile,registry,desired):
    p=plan(profile,registry,desired)
    if not p["RESULT"].startswith("PLANNED"): return registry,desired,p
    pid=profile["PROJECT_ID"]
    registry=dict(registry); desired=dict(desired)
    registry["PROJECTS"]=sorted([x for x in registry.get("PROJECTS",[]) if x.get("PROJECT_ID")!=pid]+[profile],key=lambda x:x["PROJECT_ID"])
    want=desired_from(profile)
    desired["PROJECTS"]=sorted([x for x in desired.get("PROJECTS",[]) if x.get("PROJECT_ID")!=pid]+[want],key=lambda x:x["PROJECT_ID"])
    p["RESULT"]="ENROLLED" if p["RESULT"]=="PLANNED_ENROLLMENT" else "UPDATED"
    return registry,desired,p

def main():
    ap=argparse.ArgumentParser(description="PCC-local idempotent fleet enrollment; never mutates target repositories")
    ap.add_argument("--profile",required=True); ap.add_argument("--registry",default="portfolio/projects.yml"); ap.add_argument("--desired",default="orchestration/desired-state.json"); ap.add_argument("--apply",action="store_true")
    a=ap.parse_args(); profile=load(a.profile); reg=load(a.registry); des=load(a.desired)
    if a.apply:
        reg,des,result=apply(profile,reg,des)
        if result["RESULT"] in {"ENROLLED","UPDATED"}: dump(a.registry,reg); dump(a.desired,des)
    else: result=plan(profile,reg,des)
    print(json.dumps(result,indent=2)); return 2 if result["RESULT"]=="BLOCKED" else 0
if __name__=="__main__": raise SystemExit(main())
