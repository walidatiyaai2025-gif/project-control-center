#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

REQUIRED = ["PROJECT_ID","REPOSITORY","CONTROL_PLANE_VERSION","POLICY_ENFORCEMENT_MODE","VERSION_POLICY","VERSION_SOURCE"]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def plan(profile: dict, desired_doc: dict) -> dict:
    missing=[k for k in REQUIRED if k not in profile]
    if missing:
        return {"RESULT":"BLOCKED","MISSING":missing}
    pid=profile["PROJECT_ID"]
    existing=next((p for p in desired_doc.get("PROJECTS",[]) if p.get("PROJECT_ID")==pid),None)
    if existing==profile:
        return {"RESULT":"NOOP","PROJECT_ID":pid,"REPOSITORY":profile["REPOSITORY"]}
    if existing and existing.get("REPOSITORY")!=profile.get("REPOSITORY"):
        return {"RESULT":"BLOCKED","PROJECT_ID":pid,"REASON":"PROJECT_ID_REPOSITORY_CONFLICT"}
    return {"RESULT":"PLANNED_UPDATE" if existing else "PLANNED_ENROLLMENT","PROJECT_ID":pid,"REPOSITORY":profile["REPOSITORY"],"PROFILE":profile}


def apply(profile: dict, desired_doc: dict) -> dict:
    result=plan(profile,desired_doc)
    if not result["RESULT"].startswith("PLANNED"):
        return result
    projects=[p for p in desired_doc.get("PROJECTS",[]) if p.get("PROJECT_ID")!=profile["PROJECT_ID"]]
    projects.append(profile)
    desired_doc["PROJECTS"]=sorted(projects,key=lambda p:p["PROJECT_ID"])
    return result


def main():
    ap=argparse.ArgumentParser(description="PCC repository enrollment controller; modifies PCC desired state only")
    ap.add_argument("--profile",required=True)
    ap.add_argument("--desired",default="orchestration/desired-state.json")
    ap.add_argument("--apply",action="store_true")
    args=ap.parse_args()
    profile=load(Path(args.profile)); path=Path(args.desired); desired=load(path)
    result=apply(profile,desired) if args.apply else plan(profile,desired)
    if args.apply and result["RESULT"].startswith("PLANNED"):
        path.write_text(json.dumps(desired,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 1 if result["RESULT"]=="BLOCKED" else 0

if __name__=="__main__": sys.exit(main())
