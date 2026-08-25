#!/usr/bin/env python3
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,os,tempfile
from pathlib import Path
from github_fleet_client import GitHubClient
MODES=("OBSERVE","WARN","CANARY","ENFORCE"); WRITE_MODES={"CANARY","ENFORCE"}
ALLOW={".github/workflows/reusable-version-governance.yml",".github/workflows/reusable-feature-delivery-governance.yml",".pcc/managed-repository-control.json"}
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text())
def dump(p,d):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2)+"\n")
def h(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def pmap(d): return {x["PROJECT_ID"]:x for x in d.get("PROJECTS",[]) if x.get("PROJECT_ID")}
def enroll(reg,p):
 req={"PROJECT_ID","REPOSITORY","ENROLLMENT_STATE","POLICY_ENFORCEMENT_MODE","ROLLOUT_WAVE"}; miss=sorted(req-set(p))
 if miss:return reg,{"RESULT":"BLOCKED","MISSING":miss}
 if p["POLICY_ENFORCEMENT_MODE"] not in MODES:return reg,{"RESULT":"BLOCKED","REASON":"INVALID_MODE"}
 old=pmap(reg).get(p["PROJECT_ID"])
 if old and old.get("REPOSITORY")!=p["REPOSITORY"]:return reg,{"RESULT":"BLOCKED","REASON":"PROJECT_ID_REPOSITORY_CONFLICT"}
 if old==p:return reg,{"RESULT":"NOOP","PROJECT_ID":p["PROJECT_ID"]}
 out=dict(reg); out["PROJECTS"]=sorted([x for x in reg.get("PROJECTS",[]) if x.get("PROJECT_ID")!=p["PROJECT_ID"]]+[p],key=lambda x:x["PROJECT_ID"])
 return out,{"RESULT":"UPDATED" if old else "ENROLLED","PROJECT_ID":p["PROJECT_ID"]}
def collect_project(p,c):
 repo=p["REPOSITORY"]; meta=c.repo(repo); default=meta["default_branch"]; branches=c.branches(repo); pulls=c.pulls(repo,"open"); issues=[x for x in c.issues(repo,"open") if "pull_request" not in x]
 br=[{"NAME":x.get("name"),"SHA":(x.get("commit") or {}).get("sha"),"PROTECTED":bool(x.get("protected"))} for x in branches]
 prs=[{"NUMBER":x.get("number"),"TITLE":x.get("title"),"HEAD_BRANCH":(x.get("head") or {}).get("ref"),"HEAD_SHA":(x.get("head") or {}).get("sha"),"BASE_BRANCH":(x.get("base") or {}).get("ref"),"BASE_SHA":(x.get("base") or {}).get("sha"),"UPDATED_AT":x.get("updated_at")} for x in pulls]
 gov={}; paths=["AGENTS.md","VERSION",".github/CODEOWNERS",".pcc/managed-repository-control.json",".github/workflows/reusable-version-governance.yml",".github/workflows/reusable-feature-delivery-governance.yml"]
 for path in paths:
  x=c.content(repo,path); gov[path]={"EXISTS":x is not None,"SHA":x.get("sha") if isinstance(x,dict) else None}
 rel=c.releases(repo); tags=c.tags(repo); runs=c.workflow_runs(repo,20); prot=c.branch_protection(repo,default)
 s={"PROJECT_ID":p["PROJECT_ID"],"REPOSITORY":repo,"COLLECTED_AT":now(),"COLLECTOR_RESULT":"PASS","AUTH_PROVIDER":c.auth.provider,"DEFAULT_BRANCH":default,"DEFAULT_BRANCH_SHA":next((x["SHA"] for x in br if x["NAME"]==default),None),"DEFAULT_BRANCH_PROTECTED":bool(prot) or next((x["PROTECTED"] for x in br if x["NAME"]==default),False),"BRANCHES":br,"BRANCH_COUNT":len(br),"OPEN_PRS":prs,"OPEN_PR_COUNT":len(prs),"OPEN_ISSUE_COUNT":len(issues),"RELEASES":[{"ID":x.get("id"),"TAG":x.get("tag_name")} for x in rel],"RELEASE_COUNT":len(rel),"TAGS":[{"NAME":x.get("name"),"SHA":(x.get("commit") or {}).get("sha")} for x in tags],"TAG_COUNT":len(tags),"RECENT_WORKFLOW_RUNS":[{"ID":x.get("id"),"NAME":x.get("name"),"HEAD_SHA":x.get("head_sha"),"CONCLUSION":x.get("conclusion")} for x in runs],"GOVERNANCE_FILES":gov}
 s["BRANCH_INVENTORY_HASH"]=h(br); s["DISCOVERY_FINGERPRINT"]=h({"default":s["DEFAULT_BRANCH_SHA"],"branches":br,"prs":prs,"releases":s["RELEASES"],"tags":s["TAGS"],"governance":gov}); s["DISCOVERY_COMPLETE"]=bool(s["DEFAULT_BRANCH_SHA"] and br); return s
def lock_baseline(s):
 if not s.get("DISCOVERY_COMPLETE"):return {"PROJECT_ID":s.get("PROJECT_ID"),"RESULT":"BLOCKED","REASON":"DISCOVERY_INCOMPLETE"}
 a={"DEFAULT_BRANCH":s["DEFAULT_BRANCH"],"DEFAULT_BRANCH_SHA":s["DEFAULT_BRANCH_SHA"],"BRANCH_COUNT":s["BRANCH_COUNT"],"BRANCH_INVENTORY_HASH":s["BRANCH_INVENTORY_HASH"],"OPEN_PR_HEADS":sorted([{"NUMBER":x["NUMBER"],"HEAD_BRANCH":x["HEAD_BRANCH"],"HEAD_SHA":x["HEAD_SHA"],"BASE_BRANCH":x["BASE_BRANCH"],"BASE_SHA":x["BASE_SHA"]} for x in s["OPEN_PRS"]],key=lambda x:x["NUMBER"] or 0),"RELEASES":s["RELEASES"],"TAGS":s["TAGS"]}
 return {"PROJECT_ID":s["PROJECT_ID"],"REPOSITORY":s["REPOSITORY"],"RESULT":"LOCKED","LOCKED_AT":now(),"DISCOVERY_FINGERPRINT":s["DISCOVERY_FINGERPRINT"],"BASELINE_HASH":h(a),"ANCHORS":a,"MUTATES_TARGET":False}
def active_break_glass(p,at=None):
 b=p.get("BREAK_GLASS") or {}
 if not b.get("ENABLED"):return False
 if not b.get("EXPIRES_AT"):return True
 try:return dt.datetime.fromisoformat(b["EXPIRES_AT"].replace("Z","+00:00"))>(at or dt.datetime.now(dt.timezone.utc))
 except ValueError:return True
def active_policy_exceptions(p,at=None):
 at=at or dt.datetime.now(dt.timezone.utc); out=[]
 for x in p.get("POLICY_EXCEPTIONS",[]):
  if not x.get("ENABLED",True):continue
  try:
   if x.get("EXPIRES_AT") and dt.datetime.fromisoformat(x["EXPIRES_AT"].replace("Z","+00:00"))<=at:continue
  except ValueError:continue
  out.append(x)
 return out
def stale_task_recovery(p,at=None):
 at=at or dt.datetime.now(dt.timezone.utc); out=[]
 for x in p.get("TASKS",[]):
  if x.get("STATE") in {"DONE","RELEASED","INTEGRATED","QA_PASS"} or not x.get("LEASE_EXPIRES_AT"):continue
  try: expired=dt.datetime.fromisoformat(x["LEASE_EXPIRES_AT"].replace("Z","+00:00"))<=at
  except ValueError: expired=False
  if expired:out.append({"TASK_ID":x.get("TASK_ID"),"RESULT":"RECLAIMABLE","CONTINUE_BRANCH":x.get("BRANCH"),"CONTINUE_SHA":x.get("LATEST_PUSHED_SHA"),"LAW":"SAME_TASK_SAME_BRANCH_LATEST_PUSHED_SHA_NEW_WORKER"})
 return out
def orphan_audit(p,s):
 refs={s.get("DEFAULT_BRANCH")}|{x.get("HEAD_BRANCH") for x in s.get("OPEN_PRS",[])}|{x.get("BRANCH") for x in p.get("TASKS",[]) if x.get("BRANCH")}; cand=[x for x in s.get("BRANCHES",[]) if x.get("NAME") not in refs]
 return {"PROJECT_ID":p["PROJECT_ID"],"ORPHAN_CANDIDATES":cand,"COUNT":len(cand),"AUTO_DELETE_ALLOWED":False,"REQUIRES_UNIQUE_COMMIT_RECONCILIATION":True}
def reconcile_existing_work(p,s,b):
 if b.get("RESULT")!="LOCKED":return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"BLOCKED","REASON":"BASELINE_NOT_LOCKED"}
 return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"RECONCILED_READ_ONLY","BASELINE_HASH":b["BASELINE_HASH"],"OPEN_PR_COUNT":s["OPEN_PR_COUNT"],"ACTIVE_PR_BRANCHES":sorted(x.get("HEAD_BRANCH") for x in s["OPEN_PRS"] if x.get("HEAD_BRANCH")),"STALE_RECOVERY":stale_task_recovery(p),"ORPHAN_AUDIT":orphan_audit(p,s),"CANONICAL_DEVELOPMENT_LINEAGE":p.get("CANONICAL_DEVELOPMENT_LINEAGE","UNRESOLVED"),"UNIQUE_WORK_PRESERVATION_REQUIRED":True,"TARGET_MUTATED":False}
def drift_detect(p,s):
 d=[]
 if p.get("DESIRED_POLICY_VERSION")!=p.get("OBSERVED_POLICY_VERSION"):d.append({"TYPE":"POLICY_VERSION_DRIFT","OBSERVED":p.get("OBSERVED_POLICY_VERSION"),"DESIRED":p.get("DESIRED_POLICY_VERSION")})
 for path in p.get("MANAGED_FILES",[]):
  if not s.get("GOVERNANCE_FILES",{}).get(path,{}).get("EXISTS"):d.append({"TYPE":"MANAGED_FILE_MISSING","PATH":path})
 if p.get("REQUIRE_DEFAULT_BRANCH_PROTECTION") and not s.get("DEFAULT_BRANCH_PROTECTED"):d.append({"TYPE":"DEFAULT_BRANCH_UNPROTECTED"})
 if not s.get("GOVERNANCE_FILES",{}).get(".pcc/managed-repository-control.json",{}).get("EXISTS"):d.append({"TYPE":"CONTROL_MANIFEST_MISSING"})
 codes={c for e in active_policy_exceptions(p) for c in e.get("CODES",[])}
 for x in d:x["EXCEPTED"]=x["TYPE"] in codes
 return d
def migration_plan(p,s,b,r):
 mode=p.get("POLICY_ENFORCEMENT_MODE","OBSERVE"); z=[]
 if mode not in MODES:z.append("INVALID_MODE")
 if not s.get("DISCOVERY_COMPLETE"):z.append("DISCOVERY_INCOMPLETE")
 if b.get("RESULT")!="LOCKED":z.append("BASELINE_NOT_LOCKED")
 if r.get("RESULT")!="RECONCILED_READ_ONLY":z.append("RECONCILIATION_INCOMPLETE")
 if active_break_glass(p):z.append("BREAK_GLASS_ACTIVE")
 if mode in WRITE_MODES and not p.get("WRITE_AUTHORIZED"):z.append("WRITE_NOT_AUTHORIZED")
 if mode=="CANARY" and not p.get("CANARY"):z.append("NOT_CANARY")
 if mode in WRITE_MODES and p.get("CANONICAL_DEVELOPMENT_LINEAGE","UNRESOLVED")=="UNRESOLVED":z.append("CANONICAL_LINEAGE_UNRESOLVED")
 acts=[]
 for path in p.get("MANAGED_FILES",[]):
  if path not in ALLOW:z.append("PATH_NOT_ALLOWLISTED:"+path)
  else:acts.append({"ACTION":"UPSERT_MANAGED_FILE","PATH":path})
 return {"PROJECT_ID":p["PROJECT_ID"],"MODE":mode,"RESULT":"BLOCKED" if z else ("DRY_RUN" if mode in {"OBSERVE","WARN"} else "READY"),"BLOCKERS":sorted(set(z)),"ACTIONS":acts,"TARGET_MUTATION_ALLOWED":not z and mode in WRITE_MODES}
def policy_payloads(p,root=None):
 root=root or Path(__file__).resolve().parents[1]; out={}
 for path in p.get("MANAGED_FILES",[]):
  if path==".pcc/managed-repository-control.json":out[path]=json.dumps({"PROJECT_ID":p["PROJECT_ID"],"CONTROL_PLANE_REPOSITORY":"walidatiyaai2025-gif/project-control-center","CONTROL_PLANE_VERSION":p.get("CONTROL_PLANE_VERSION"),"POLICY_VERSION":p.get("DESIRED_POLICY_VERSION"),"ENFORCEMENT_MODE":p.get("POLICY_ENFORCEMENT_MODE")},indent=2)+"\n"
  elif path in ALLOW and (root/path).is_file():out[path]=(root/path).read_text()
 return out
def apply_policy_sync(p,plan,c,payloads,branch=None):
 if plan.get("RESULT")!="READY" or not plan.get("TARGET_MUTATION_ALLOWED"):return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"BLOCKED","REASON":"MIGRATION_PLAN_NOT_READY","TARGET_MUTATED":False}
 if active_break_glass(p):return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"BLOCKED","REASON":"BREAK_GLASS_ACTIVE","TARGET_MUTATED":False}
 if not c.auth.write_capable:return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"BLOCKED","REASON":"WRITE_AUTH_PROVIDER_REQUIRED","TARGET_MUTATED":False}
 import base64; applied=[]; skipped=[]; repo=p["REPOSITORY"]; branch=branch or p.get("POLICY_TARGET_BRANCH") or "main"
 for a in plan["ACTIONS"]:
  path=a["PATH"]
  if path not in ALLOW:return {"RESULT":"BLOCKED","REASON":"PATH_NOT_ALLOWLISTED:"+path,"TARGET_MUTATED":bool(applied)}
  content=payloads.get(path)
  if content is None:return {"RESULT":"BLOCKED","REASON":"PAYLOAD_MISSING:"+path,"TARGET_MUTATED":bool(applied)}
  cur=c.content(repo,path); text=None
  if isinstance(cur,dict) and cur.get("content"):
   try:text=base64.b64decode(cur["content"]).decode()
   except Exception:pass
  if text==content:skipped.append(path);continue
  c.upsert_text_file(repo,path,content,f"chore(pcc): sync managed policy {p.get('DESIRED_POLICY_VERSION')}",branch,cur.get("sha") if isinstance(cur,dict) else None); applied.append(path)
 return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"APPLIED" if applied else "NOOP","APPLIED":applied,"SKIPPED":skipped,"TARGET_MUTATED":bool(applied)}
def operation_key(p,s,a="FLEET_RECONCILE"):return h({"PROJECT_ID":p["PROJECT_ID"],"ACTION":a,"DESIRED_POLICY_VERSION":p.get("DESIRED_POLICY_VERSION"),"DISCOVERY_FINGERPRINT":s.get("DISCOVERY_FINGERPRINT"),"MODE":p.get("POLICY_ENFORCEMENT_MODE"),"ROLLOUT_WAVE":p.get("ROLLOUT_WAVE",0)})[:32]
def append_ledger(l,e):
 if e.get("OPERATION_KEY") and any(x.get("OPERATION_KEY")==e["OPERATION_KEY"] and x.get("RESULT")==e.get("RESULT") for x in l.setdefault("EVENTS",[])):return False
 l["EVENTS"].append(e);return True
def acquire_lock(pid,key,root=None):
 root=root or Path(tempfile.gettempdir())/"pcc-fleet-locks"; root.mkdir(parents=True,exist_ok=True); p=root/f"{pid}-{key}.lock"; fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd);return p
def release_lock(p):
 try:p.unlink()
 except FileNotFoundError:pass
def run_project(p,c,apply=False):
 s=collect_project(p,c); b=lock_baseline(s); r=reconcile_existing_work(p,s,b); d=drift_detect(p,s); m=migration_plan(p,s,b,r); sync={"RESULT":"NOT_REQUESTED","TARGET_MUTATED":False}
 if apply:sync=apply_policy_sync(p,m,c,policy_payloads(p),p.get("POLICY_TARGET_BRANCH") or s.get("DEFAULT_BRANCH"))
 return {"PROJECT_ID":p["PROJECT_ID"],"RESULT":"PASS","OPERATION_KEY":operation_key(p,s),"SNAPSHOT":s,"BASELINE":b,"RECONCILIATION":r,"DRIFT":d,"ACTIVE_POLICY_EXCEPTIONS":active_policy_exceptions(p),"MIGRATION":m,"POLICY_SYNC":sync,"STALE_RECOVERY":r.get("STALE_RECOVERY",[]),"ORPHAN_AUDIT":r.get("ORPHAN_AUDIT",{})}
def run_fleet(reg,c,mode_override=None,project_filter=None,apply=False):
 rows=[]
 for raw in sorted(reg.get("PROJECTS",[]),key=lambda x:(x.get("ROLLOUT_WAVE",0),x.get("PROJECT_ID",""))):
  if project_filter and raw.get("PROJECT_ID")!=project_filter:continue
  p=dict(raw)
  if mode_override:p["POLICY_ENFORCEMENT_MODE"]=mode_override
  try:rows.append(run_project(p,c,apply))
  except Exception as e:rows.append({"PROJECT_ID":p.get("PROJECT_ID"),"RESULT":"FAILED","ERROR":str(e)})
 return {"CONTROL_PLANE_VERSION":reg.get("CONTROL_PLANE_VERSION"),"GENERATED_AT":now(),"PROJECTS":rows,"PASS":all(x.get("RESULT")=="PASS" for x in rows)}
def aggregate_portfolio(reg,report):
 rm={x.get("PROJECT_ID"):x for x in report.get("PROJECTS",[])}; rows=[]
 for p in reg.get("PROJECTS",[]):
  r=rm.get(p["PROJECT_ID"],{}); s=r.get("SNAPSHOT",{}); rows.append({**p,"COLLECTOR_RESULT":s.get("COLLECTOR_RESULT","FAILED" if r.get("RESULT")=="FAILED" else "UNKNOWN"),"DEFAULT_BRANCH":s.get("DEFAULT_BRANCH"),"DEFAULT_BRANCH_SHA":s.get("DEFAULT_BRANCH_SHA"),"DEFAULT_BRANCH_PROTECTED":s.get("DEFAULT_BRANCH_PROTECTED",False),"BRANCH_COUNT":s.get("BRANCH_COUNT",0),"OPEN_PR_COUNT":s.get("OPEN_PR_COUNT",0),"RELEASE_COUNT":s.get("RELEASE_COUNT",0),"DISCOVERY_COMPLETE":s.get("DISCOVERY_COMPLETE",False),"BASELINE_LOCKED":r.get("BASELINE",{}).get("RESULT")=="LOCKED","RECONCILIATION_RESULT":r.get("RECONCILIATION",{}).get("RESULT"),"DRIFT":r.get("DRIFT",[]),"DRIFT_COUNT":len(r.get("DRIFT",[])),"STALE_RECLAIMABLE":len(r.get("STALE_RECOVERY",[])),"ORPHAN_CANDIDATES":r.get("ORPHAN_AUDIT",{}).get("COUNT",0),"MIGRATION_RESULT":r.get("MIGRATION",{}).get("RESULT")})
 return {"CONTROL_PLANE_VERSION":reg.get("CONTROL_PLANE_VERSION"),"GENERATED_AT":now(),"TOTAL_PROJECTS":len(rows),"COLLECTION_PASS":sum(x["COLLECTOR_RESULT"]=="PASS" for x in rows),"DISCOVERED":sum(x["DISCOVERY_COMPLETE"] for x in rows),"BASELINE_LOCKED":sum(x["BASELINE_LOCKED"] for x in rows),"DRIFT_PROJECTS":sum(x["DRIFT_COUNT"]>0 for x in rows),"STALE_RECLAIMABLE":sum(x["STALE_RECLAIMABLE"] for x in rows),"ORPHAN_CANDIDATES":sum(x["ORPHAN_CANDIDATES"] for x in rows),"PROJECTS":rows}
def runtime_ledger(seed,report,c):
 l=dict(seed);l["CONTROL_PLANE_VERSION"]=report.get("CONTROL_PLANE_VERSION");l.setdefault("EVENTS",[])
 for r in report.get("PROJECTS",[]):
  pid=r.get("PROJECT_ID");op=r.get("OPERATION_KEY") or h({"pid":pid,"t":report.get("GENERATED_AT")})[:32]
  for typ,key in (("LIVE_DISCOVERY","SNAPSHOT"),("BASELINE_LOCK","BASELINE"),("RECONCILIATION","RECONCILIATION"),("MIGRATION_PLAN","MIGRATION"),("POLICY_SYNC","POLICY_SYNC")):
   x=r.get(key,{});append_ledger(l,{"PROJECT_ID":pid,"OPERATION_KEY":f"{op}:{typ}","TYPE":typ,"RESULT":x.get("RESULT",x.get("COLLECTOR_RESULT",r.get("RESULT"))),"AUTH_PROVIDER":c.auth.provider,"TARGET_MUTATED":bool(x.get("TARGET_MUTATED")),"TIMESTAMP":report.get("GENERATED_AT")})
  append_ledger(l,{"PROJECT_ID":pid,"OPERATION_KEY":f"{op}:ORPHAN_AUDIT","TYPE":"ORPHAN_AUDIT","RESULT":"PASS" if r.get("RESULT")=="PASS" else "FAILED","COUNT":r.get("ORPHAN_AUDIT",{}).get("COUNT",0),"TARGET_MUTATED":False,"TIMESTAMP":report.get("GENERATED_AT")})
 return l
def main():
 a=argparse.ArgumentParser();a.add_argument("--registry",default="portfolio/projects.yml");a.add_argument("--report-out",default="orchestration/fleet-report.json");a.add_argument("--portfolio-out",default="portfolio/status/fleet-live.json");a.add_argument("--mode",choices=MODES);a.add_argument("--project");a.add_argument("--apply-policy-sync",action="store_true");a.add_argument("--ledger-seed",default="orchestration/audit-ledger.json");a.add_argument("--ledger-out",default="/tmp/pcc-audit-ledger-runtime.json");x=a.parse_args();c=GitHubClient();reg=load(x.registry);r=run_fleet(reg,c,x.mode,x.project,x.apply_policy_sync);dump(x.report_out,r);dump(x.portfolio_out,aggregate_portfolio(reg,r));dump(x.ledger_out,runtime_ledger(load(x.ledger_seed),r,c));print(json.dumps({"PASS":r["PASS"],"AUTH_PROVIDER":c.auth.provider,"PROJECTS":[{"PROJECT_ID":q.get("PROJECT_ID"),"RESULT":q.get("RESULT"),"ERROR":q.get("ERROR")} for q in r["PROJECTS"]]},indent=2));return 0 if r["PASS"] else 2
if __name__=="__main__":raise SystemExit(main())
