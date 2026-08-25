import datetime as dt
import tempfile
import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import fleet_control as fc
from github_fleet_client import AuthContext, GitHubClient
import io, urllib.error

class FakeClient:
    auth=AuthContext("fixture",None,False)
    def repo(self,repo):
        if repo=="bad/repo": raise RuntimeError("boom")
        return {"default_branch":"main"}
    def branches(self,repo):
        return [{"name":"main","commit":{"sha":"m1"},"protected":True},{"name":"feature/a","commit":{"sha":"a1"},"protected":False},{"name":"orphan/x","commit":{"sha":"o1"},"protected":False}]
    def pulls(self,repo,state="open"):
        return [{"number":7,"title":"A","draft":False,"head":{"ref":"feature/a","sha":"a1"},"base":{"ref":"main","sha":"m1"},"updated_at":"2026-08-25T00:00:00Z"}]
    def issues(self,repo,state="open"): return [{"number":1,"title":"i","updated_at":"x"}]
    def releases(self,repo): return []
    def tags(self,repo): return []
    def workflow_runs(self,repo,per_page=20): return [{"id":1,"name":"CI","head_branch":"feature/a","head_sha":"a1","status":"completed","conclusion":"success","updated_at":"x"}]
    def branch_protection(self,repo,branch): return {"enabled":True}
    def content(self,repo,path): return None

def project(**kw):
    base={
        "PROJECT_ID":"P","REPOSITORY":"o/r","ENROLLMENT_STATE":"REGISTERED",
        "POLICY_ENFORCEMENT_MODE":"OBSERVE","ROLLOUT_WAVE":0,
        "DESIRED_POLICY_VERSION":"1.1.0","OBSERVED_POLICY_VERSION":None,
        "CANARY":True,"WRITE_AUTHORIZED":False,
        "MANAGED_FILES":[".pcc/managed-repository-control.json"],
        "REQUIRE_DEFAULT_BRANCH_PROTECTION":True,
        "TASKS":[]
    }
    base.update(kw); return base

class FleetTests(unittest.TestCase):
    def test_enrollment_idempotent(self):
        reg={"PROJECTS":[]}; reg,res=fc.enroll(reg,project())
        self.assertEqual(res["RESULT"],"ENROLLED")
        reg2,res2=fc.enroll(reg,project())
        self.assertEqual(reg2,reg); self.assertEqual(res2["RESULT"],"NOOP")
    def test_collection_and_baseline(self):
        s=fc.collect_project(project(),FakeClient())
        self.assertTrue(s["DISCOVERY_COMPLETE"]); self.assertEqual(s["BRANCH_COUNT"],3)
        b=fc.lock_baseline(s); self.assertEqual(b["RESULT"],"LOCKED"); self.assertFalse(b["MUTATES_TARGET"])
    def test_reconcile_preserves_unique_work(self):
        p=project(); s=fc.collect_project(p,FakeClient()); b=fc.lock_baseline(s)
        r=fc.reconcile_existing_work(p,s,b)
        self.assertTrue(r["UNIQUE_WORK_PRESERVATION_REQUIRED"])
        self.assertEqual(r["ORPHAN_AUDIT"]["COUNT"],1)
        self.assertFalse(r["ORPHAN_AUDIT"]["AUTO_DELETE_ALLOWED"])
    def test_observe_never_mutates(self):
        p=project(POLICY_ENFORCEMENT_MODE="OBSERVE",WRITE_AUTHORIZED=True)
        s=fc.collect_project(p,FakeClient()); b=fc.lock_baseline(s); r=fc.reconcile_existing_work(p,s,b)
        m=fc.migration_plan(p,s,b,r)
        self.assertEqual(m["RESULT"],"DRY_RUN"); self.assertFalse(m["TARGET_MUTATION_ALLOWED"])
    def test_canary_requires_write_authorization(self):
        p=project(POLICY_ENFORCEMENT_MODE="CANARY",WRITE_AUTHORIZED=False)
        s=fc.collect_project(p,FakeClient()); b=fc.lock_baseline(s); r=fc.reconcile_existing_work(p,s,b)
        self.assertIn("WRITE_NOT_AUTHORIZED",fc.migration_plan(p,s,b,r)["BLOCKERS"])
    def test_canary_ready_when_authorized(self):
        p=project(POLICY_ENFORCEMENT_MODE="CANARY",WRITE_AUTHORIZED=True,CANONICAL_DEVELOPMENT_LINEAGE="main")
        s=fc.collect_project(p,FakeClient()); b=fc.lock_baseline(s); r=fc.reconcile_existing_work(p,s,b)
        m=fc.migration_plan(p,s,b,r)
        self.assertEqual(m["RESULT"],"READY"); self.assertTrue(m["TARGET_MUTATION_ALLOWED"])
    def test_break_glass_blocks(self):
        future=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat()
        p=project(POLICY_ENFORCEMENT_MODE="CANARY",WRITE_AUTHORIZED=True,BREAK_GLASS={"ENABLED":True,"EXPIRES_AT":future})
        s=fc.collect_project(p,FakeClient()); b=fc.lock_baseline(s); r=fc.reconcile_existing_work(p,s,b)
        self.assertIn("BREAK_GLASS_ACTIVE",fc.migration_plan(p,s,b,r)["BLOCKERS"])
    def test_stale_recovery_continues_same_branch(self):
        past=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(hours=1)).isoformat()
        p=project(TASKS=[{"TASK_ID":"T1","STATE":"IN_PROGRESS","LEASE_EXPIRES_AT":past,"BRANCH":"task/t1","LATEST_PUSHED_SHA":"abc"}])
        row=fc.stale_task_recovery(p)[0]
        self.assertEqual((row["TASK_ID"],row["CONTINUE_BRANCH"],row["CONTINUE_SHA"]),("T1","task/t1","abc"))
    def test_drift_detection(self):
        p=project()
        s=fc.collect_project(p,FakeClient())
        types={x["TYPE"] for x in fc.drift_detect(p,s)}
        self.assertIn("POLICY_VERSION_DRIFT",types); self.assertIn("CONTROL_MANIFEST_MISSING",types)
    def test_failure_isolation(self):
        reg={"CONTROL_PLANE_VERSION":"v1.3.0","PROJECTS":[project(),project(PROJECT_ID="B",REPOSITORY="bad/repo")]}
        r=fc.run_fleet(reg,FakeClient())
        self.assertEqual(len(r["PROJECTS"]),2)
        by={x["PROJECT_ID"]:x for x in r["PROJECTS"]}
        self.assertEqual(by["P"]["RESULT"],"PASS"); self.assertEqual(by["B"]["RESULT"],"FAILED")
    def test_ledger_idempotency(self):
        l={"EVENTS":[]}; e={"OPERATION_KEY":"k","RESULT":"PASS"}
        self.assertTrue(fc.append_ledger(l,e)); self.assertFalse(fc.append_ledger(l,e)); self.assertEqual(len(l["EVENTS"]),1)
    def test_concurrency_lock(self):
        with tempfile.TemporaryDirectory() as d:
            p=fc.acquire_lock("P","K",Path(d))
            with self.assertRaises(FileExistsError): fc.acquire_lock("P","K",Path(d))
            fc.release_lock(p)
    def test_portfolio_aggregation(self):
        reg={"CONTROL_PLANE_VERSION":"v1.3.0","PROJECTS":[project()]}
        r=fc.run_fleet(reg,FakeClient()); a=fc.aggregate_portfolio(reg,r)
        self.assertEqual(a["TOTAL_PROJECTS"],1); self.assertEqual(a["COLLECTION_PASS"],1); self.assertEqual(a["BASELINE_LOCKED"],1)


class FakeWriteClient(FakeClient):
    auth=AuthContext("fixture_write","token",True)
    def __init__(self): self.writes=[]
    def content(self,repo,path): return None
    def upsert_text_file(self,repo,path,content,message,branch,sha=None):
        self.writes.append((repo,path,content,branch,sha)); return {"commit":{"sha":"new"}}

class MigrationApplyTests(unittest.TestCase):
    def test_policy_sync_apply_is_allowlisted_and_idempotent_contract(self):
        p=project(POLICY_ENFORCEMENT_MODE="CANARY",WRITE_AUTHORIZED=True,CANONICAL_DEVELOPMENT_LINEAGE="main")
        c=FakeWriteClient(); s=fc.collect_project(p,c); b=fc.lock_baseline(s); r=fc.reconcile_existing_work(p,s,b)
        plan=fc.migration_plan(p,s,b,r)
        out=fc.apply_policy_sync(p,plan,c,{".pcc/managed-repository-control.json":"{}\n"},"main")
        self.assertEqual(out["RESULT"],"APPLIED"); self.assertEqual(len(c.writes),1)
    def test_policy_exception_expiry(self):
        future=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat()
        p=project(POLICY_EXCEPTIONS=[{"ID":"E1","TYPE":"POLICY_VERSION_DRIFT","ENABLED":True,"EXPIRES_AT":future}])
        self.assertEqual(fc.active_policy_exceptions(p)[0]["ID"],"E1")


class _Resp:
    def __init__(self,obj): self.obj=obj
    def __enter__(self): return self
    def __exit__(self,*a): return False
    def read(self): return json.dumps(self.obj).encode()

class RetryTests(unittest.TestCase):
    def test_retry_on_server_error(self):
        calls={"n":0}; sleeps=[]
        def opener(req,timeout=0):
            calls["n"]+=1
            if calls["n"]==1:
                raise urllib.error.HTTPError(req.full_url,503,"busy",{"Retry-After":"0"},io.BytesIO(b"busy"))
            return _Resp({"ok":True})
        c=GitHubClient(auth=AuthContext("fixture",None,False),max_retries=2,sleep=lambda x:sleeps.append(x),opener=opener)
        self.assertEqual(c.get("/x"),{"ok":True}); self.assertEqual(calls["n"],2); self.assertEqual(sleeps,[0.0])

if __name__=="__main__": unittest.main()
