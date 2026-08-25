import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

vg = load_module("version_governance", ROOT / "scripts/version_governance.py")
orch = load_module("orchestrator", ROOT / "scripts/orchestrator.py")
enroll = load_module("enrollment_controller", ROOT / "scripts/enrollment_controller.py")

class VersionGovernanceTests(unittest.TestCase):
    def test_semver(self):
        self.assertTrue(vg.SEMVER.match("2.8.0-rc.2"))
        self.assertFalse(vg.SEMVER.match("final"))

    def test_duplicate_version_sha_rejected(self):
        err = vg.released_mapping_error("2.7.3", "def456", {"2.7.3": "abc123"})
        self.assertIn("VERSION_REUSE", err)

    def test_same_version_same_sha_allowed(self):
        self.assertIsNone(vg.released_mapping_error("2.7.3", "abc123", {"2.7.3": "abc123"}))

    def test_version_history_mapping_supported(self):
        doc={"VERSIONS":[{"PRODUCT_VERSION":"2.7.3","SOURCE_SHA":"abc123"}]}
        self.assertEqual(vg.normalize_mapping(doc)["2.7.3"],"abc123")

    def test_official_artifact_without_version_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td); (repo / "VERSION").write_text("2.7.3\n")
            _, _, errors = vg.validate(repo,"X","VERSION","semantic","abc1234",None,None,None,False,False,"final.zip","{project}-{version}",True,"v2.7.3","v{version}",{},None)
            self.assertTrue(any("OFFICIAL_ARTIFACT" in e or "AMBIGUOUS" in e for e in errors))

    def test_display_drift_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td); (repo / "VERSION").write_text("2.7.3\n")
            _, _, errors = vg.validate(repo,"X","VERSION","semantic","abc1234","2.7.2",None,None,True,False,"X-2.7.3.zip","{project}-{version}",False,None,"v{version}",{},None)
            self.assertTrue(any("VERSION_DRIFT" in e for e in errors))

    def test_official_requires_tag_and_release_notes(self):
        with tempfile.TemporaryDirectory() as td:
            repo=Path(td); (repo/"VERSION").write_text("2.7.3\n")
            _,_,errors=vg.validate(repo,"X","VERSION","semantic","abc1234",None,None,None,False,False,"X-2.7.3.zip","{project}-{version}",True,None,"v{version}",{},None)
            self.assertIn("OFFICIAL_RELEASE_TAG_REQUIRED",errors)
            self.assertIn("OFFICIAL_RELEASE_NOTES_REQUIRED",errors)

class OrchestratorTests(unittest.TestCase):
    def test_observe_detects_drift_without_product_mutation(self):
        desired={"CONTROL_PLANE_VERSION":"v1.1.0","PROJECTS":[{"PROJECT_ID":"P","CONTROL_PLANE_VERSION":"v1.1.0","DESIRED_POLICY_VERSION":"1.0.0","POLICY_ENFORCEMENT_MODE":"OBSERVE","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION"}]}
        observed={"PROJECTS":[{"PROJECT_ID":"P","CONTROL_PLANE_VERSION":"v1.0.0","OBSERVED_POLICY_VERSION":"0.9.0","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION"}]}
        report,_=orch.reconcile(desired,observed)
        self.assertEqual(report["PROJECTS"][0]["RESULT"],"DRIFT")
        self.assertTrue(report["DRY_RUN"])

    def test_enforce_requires_baselines(self):
        desired={"CONTROL_PLANE_VERSION":"v1.1.0","PROJECTS":[{"PROJECT_ID":"P","CONTROL_PLANE_VERSION":"v1.1.0","DESIRED_POLICY_VERSION":"1.0.0","POLICY_ENFORCEMENT_MODE":"ENFORCE","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION"}]}
        observed={"PROJECTS":[{"PROJECT_ID":"P","CONTROL_PLANE_VERSION":"v1.1.0","OBSERVED_POLICY_VERSION":"1.0.0","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION"}]}
        report,_=orch.reconcile(desired,observed)
        self.assertEqual(report["PROJECTS"][0]["RESULT"],"BLOCKED")
        self.assertIn("VERSION_BASELINE_NOT_ESTABLISHED",report["PROJECTS"][0]["BLOCKERS"])

    def test_safe_heal_is_allow_listed(self):
        observed={"DERIVED_STATUS_STALE":True,"UNRELATED":True}
        healed=orch.safe_heal(observed)
        self.assertEqual(healed,["DERIVED_STATUS_STALE"])
        self.assertTrue(observed["UNRELATED"])

class EnrollmentTests(unittest.TestCase):
    def legacy_profile(self, **kw):
        p={"PROJECT_ID":"P","REPOSITORY":"o/r","CONTROL_PLANE_VERSION":"v1.2.0","POLICY_ENFORCEMENT_MODE":"OBSERVE","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION"}
        p.update(kw); return p

    def fleet_profile(self, **kw):
        p={
            "PROJECT_ID":"P","DISPLAY_NAME":"Project P","REPOSITORY":"o/r",
            "ENROLLMENT_STATE":"REGISTERED","DISCOVERY_STATE":"PENDING_DISCOVERY",
            "CONTROL_PLANE_VERSION":"v1.3.0","DESIRED_POLICY_VERSION":"1.1.0",
            "POLICY_ENFORCEMENT_MODE":"OBSERVE","ROLLOUT_WAVE":0,
            "CANARY":True,"WRITE_AUTHORIZED":False,
            "CANONICAL_DEVELOPMENT_LINEAGE":"UNRESOLVED",
            "AUTH_PROVIDER":"none/read_only","VERSION_POLICY":"semantic","VERSION_SOURCE":"VERSION",
        }
        p.update(kw); return p

    def test_legacy_idempotent_same_profile(self):
        profile=self.legacy_profile()
        self.assertEqual(enroll.plan(profile,{"PROJECTS":[profile]})["RESULT"],"NOOP")

    def test_legacy_conflicting_repository_is_blocked(self):
        profile=self.legacy_profile(REPOSITORY="o/new")
        existing=self.legacy_profile(REPOSITORY="o/old")
        result=enroll.plan(profile,{"PROJECTS":[existing]})
        self.assertEqual(result["RESULT"],"BLOCKED")
        self.assertEqual(result["REASON"],"PROJECT_ID_REPOSITORY_CONFLICT")

    def test_legacy_required_fields_remain_v12_contract(self):
        profile=self.legacy_profile()
        self.assertNotIn("DISPLAY_NAME",profile)
        self.assertEqual(enroll.plan(profile,{"PROJECTS":[]})["RESULT"],"PLANNED_ENROLLMENT")

    def test_modern_plan_noop_identical(self):
        profile=self.fleet_profile(); desired=enroll.desired_from(profile)
        result=enroll.plan(profile,{"PROJECTS":[profile]},{"PROJECTS":[desired]})
        self.assertEqual(result["RESULT"],"NOOP")
        self.assertFalse(result["TARGET_MUTATED"])

    def test_modern_required_fleet_metadata_enforced(self):
        profile=self.fleet_profile(); profile.pop("DISPLAY_NAME")
        result=enroll.plan(profile,{"PROJECTS":[]},{"PROJECTS":[]})
        self.assertEqual(result["RESULT"],"BLOCKED")
        self.assertIn("DISPLAY_NAME",result["MISSING"])

    def test_modern_conflicting_repository_is_blocked(self):
        profile=self.fleet_profile(REPOSITORY="o/new")
        existing=self.fleet_profile(REPOSITORY="o/old")
        result=enroll.plan(profile,{"PROJECTS":[existing]},{"PROJECTS":[]})
        self.assertEqual(result["RESULT"],"BLOCKED")
        self.assertEqual(result["REASON"],"PROJECT_ID_REPOSITORY_CONFLICT")

    def test_modern_duplicate_apply_is_idempotent(self):
        profile=self.fleet_profile(); registry={"PROJECTS":[]}; desired={"PROJECTS":[]}
        registry,desired,first=enroll.apply(profile,registry,desired)
        self.assertEqual(first["RESULT"],"ENROLLED")
        registry2,desired2,second=enroll.apply(profile,registry,desired)
        self.assertEqual(second["RESULT"],"NOOP")
        self.assertEqual(registry2,registry); self.assertEqual(desired2,desired)

    def test_explicit_none_uses_modern_contract_and_blocks(self):
        result=enroll.plan(self.fleet_profile(),{"PROJECTS":[]},None)
        self.assertEqual(result["RESULT"],"BLOCKED")
        self.assertEqual(result["REASON"],"DESIRED_STATE_REQUIRED")

class RepresentationTests(unittest.TestCase):
    def test_target_and_release_versions_represented(self):
        task=json.loads((ROOT/"templates/TASK.yml").read_text())
        self.assertIn("TARGET_VERSION",task); self.assertIn("RELEASED_IN_VERSION",task)

    def test_rollback_version_represented(self):
        release=json.loads((ROOT/"templates/RELEASE_EVIDENCE.yml").read_text())
        self.assertIn("PREVIOUS_KNOWN_GOOD_VERSION",release); self.assertIn("PREVIOUS_KNOWN_GOOD_SHA",release)

if __name__ == "__main__": unittest.main()
