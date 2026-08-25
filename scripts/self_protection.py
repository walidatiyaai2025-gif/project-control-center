#!/usr/bin/env python3
import argparse, json
from github_fleet_client import GitHubClient, GitHubAPIError

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",default="walidatiyaai2025-gif/project-control-center")
    ap.add_argument("--branch",default="main")
    ap.add_argument("--apply",action="store_true")
    args=ap.parse_args()
    c=GitHubClient()
    try:
        current=c.branch_protection(args.repo,args.branch)
    except GitHubAPIError as exc:
        if exc.status in {401,403}:
            print(json.dumps({"RESULT":"BLOCKED","PROTECTED":None,"BRANCH":args.branch,"REASON":"BRANCH_PROTECTION_READ_REQUIRES_REPOSITORY_ADMIN_AUTH","AUTH_PROVIDER":c.auth.provider},indent=2)); return 2
        raise
    if current:
        print(json.dumps({"RESULT":"PASS","PROTECTED":True,"BRANCH":args.branch,"AUTH_PROVIDER":c.auth.provider},indent=2)); return 0
    if not args.apply:
        print(json.dumps({"RESULT":"BLOCKED","PROTECTED":False,"BRANCH":args.branch,"REASON":"MAIN_PROTECTION_NOT_CONFIGURED_OR_NOT_VISIBLE_TO_TOKEN","AUTH_PROVIDER":c.auth.provider},indent=2)); return 2
    if not c.auth.write_capable:
        print(json.dumps({"RESULT":"BLOCKED","PROTECTED":False,"REASON":"REPOSITORY_ADMIN_WRITE_CREDENTIAL_REQUIRED","AUTH_PROVIDER":c.auth.provider},indent=2)); return 2
    c.protect_branch(args.repo,args.branch,["Control Plane Validation / self-audit"])
    verify=c.branch_protection(args.repo,args.branch)
    ok=bool(verify)
    print(json.dumps({"RESULT":"PASS" if ok else "FAILED","PROTECTED":ok,"BRANCH":args.branch,"AUTH_PROVIDER":c.auth.provider},indent=2))
    return 0 if ok else 2
if __name__=="__main__": raise SystemExit(main())
