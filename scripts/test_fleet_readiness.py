import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet_readiness as fr


class ReadinessTests(unittest.TestCase):
    def make_root(self, projects=None, constitution_state="READY"):
        d = tempfile.TemporaryDirectory()
        root = Path(d.name)
        for rel in [
            "portfolio", "orchestration", "templates", "scripts", "policies", ".github/workflows"
        ]:
            (root / rel).mkdir(parents=True, exist_ok=True)
        (root / "VERSION").write_text("v1.5.0\n")
        projects = projects or [self.project("P1", "o/r1"), self.project("P2", "o/r2")]
        (root / "portfolio/projects.yml").write_text(json.dumps({"CONTROL_PLANE_VERSION":"v1.5.0","PROJECTS":projects}))
        desired = []
        for p in projects:
            desired.append({k:p.get(k) for k in fr.DESIRED_PARITY_KEYS})
        (root / "orchestration/desired-state.json").write_text(json.dumps({"CONTROL_PLANE_VERSION":"v1.5.0","PROJECTS":desired}))
        routing = []
        for p in projects:
            routing.append({
                "PROJECT_ID": p["PROJECT_ID"], "DISPLAY_NAME": p["DISPLAY_NAME"], "REPOSITORY": p["REPOSITORY"],
                "PROJECT_MODEL": "STANDALONE", "ALIASES": [p["PROJECT_ID"].lower()], "ROUTING_REQUIRED": True,
                "CONSTITUTION_PATH": "AGENTS.md", "CONSTITUTION_STATE": constitution_state,
                "FAMILY_MANIFEST_PATH": None, "DEFAULT_SCOPE": "PROJECT", "VARIANTS": []
            })
        (root / "portfolio/project-routing.json").write_text(json.dumps({"CONTROL_PLANE_VERSION":"v1.5.0","ROUTING_CONTRACT_VERSION":"1.0.0","PROJECTS":routing}))
        (root / "templates/PROJECT_PROFILE.yml").write_text('{"CONTROL_PLANE_VERSION":"v1.5.0"}')
        (root / "templates/MANAGED_REPOSITORY_CONTROL.yml").write_text('{"CONTROL_PLANE_VERSION":"v1.5.0"}')
        (root / "templates/PROJECT_ROUTING.json").write_text('{"CONSTITUTION_STATE":"PENDING"}')
        (root / "scripts/enrollment_controller.py").write_text("PCC-local idempotent fleet enrollment TARGET_MUTATED")
        (root / "scripts/fleet_control.py").write_text("OBSERVE CANARY ENFORCE apply_policy_sync PATH_NOT_ALLOWLISTED BREAK_GLASS_ACTIVE WRITE_AUTH_PROVIDER_REQUIRED")
        (root / "scripts/route_work.py").write_text("PCC worker routing packet REPOSITORY_CONSTITUTION_NOT_READY TARGET_SCOPE_REQUIRED_FOR_PRODUCT_FAMILY")
        (root / "scripts/self_protection.py").write_text("MAIN_PROTECTION_NOT_CONFIGURED REPOSITORY_ADMIN_WRITE_CREDENTIAL_REQUIRED")
        (root / "policies/FLEET_CONTROL_POLICY.md").write_text("read before write OBSERVE -> WARN -> CANARY -> ENFORCE Automatic deletion is forbidden")
        (root / "policies/PROJECT_FAMILY_ROUTING_POLICY.md").write_text("Every implementation worker MUST receive CONSTITUTION_STATE=PENDING Alias collisions are governance blockers")
        (root / ".github/workflows/fleet-control.yml").write_text("workflow_dispatch apply_policy_sync fleet_readiness.py")
        (root / ".github/workflows/control-plane-validation.yml").write_text("fleet_readiness.py test_fleet_readiness.py test_route_work.py")
        return d, root

    def project(self, pid, repo, **kw):
        p = {
            "PROJECT_ID":pid, "DISPLAY_NAME":pid, "REPOSITORY":repo,
            "ENROLLMENT_STATE":"REGISTERED", "DISCOVERY_STATE":"PENDING_DISCOVERY",
            "POLICY_ENFORCEMENT_MODE":"OBSERVE", "ROLLOUT_WAVE":0,
            "CONTROL_PLANE_VERSION":"v1.5.0", "DESIRED_POLICY_VERSION":"1.1.0",
            "MANAGED_FILES":[".pcc/managed-repository-control.json"],
            "WRITE_AUTHORIZED":False, "CANARY":False,
            "CANONICAL_DEVELOPMENT_LINEAGE":"UNRESOLVED",
        }
        p.update(kw)
        return p

    def test_two_project_onboarding_static_ready(self):
        d, root = self.make_root()
        try:
            r = fr.validate_static(root)
            self.assertTrue(r["ONBOARDING_READY"])
            self.assertEqual(r["READINESS_PERCENT"], 100)
            self.assertEqual(r["REGISTERED_PROJECTS"], 2)
            self.assertEqual(r["ROUTABLE_PROJECTS"], 2)
        finally:
            d.cleanup()

    def test_duplicate_repository_blocks(self):
        p1 = self.project("P1", "o/r")
        p2 = self.project("P2", "o/r")
        d, root = self.make_root([p1, p2])
        try:
            r = fr.validate_static(root)
            self.assertFalse(r["ONBOARDING_READY"])
            self.assertIn("REGISTRY_IDENTITY_INVALID_OR_DUPLICATE", r["BLOCKERS"])
        finally:
            d.cleanup()

    def test_write_mode_requires_authorization_and_lineage(self):
        p = self.project("P1", "o/r", POLICY_ENFORCEMENT_MODE="CANARY", CANARY=True)
        d, root = self.make_root([p])
        try:
            r = fr.validate_static(root)
            self.assertIn("P1:WRITE_MODE_WITHOUT_AUTHORIZATION", r["BLOCKERS"])
            self.assertIn("P1:WRITE_MODE_WITH_UNRESOLVED_LINEAGE", r["BLOCKERS"])
        finally:
            d.cleanup()

    def test_non_allowlisted_managed_file_blocks(self):
        p = self.project("P1", "o/r", MANAGED_FILES=["src/app.py"])
        d, root = self.make_root([p])
        try:
            r = fr.validate_static(root)
            self.assertTrue(any(x.startswith("P1:NON_ALLOWLISTED_MANAGED_FILES") for x in r["BLOCKERS"]))
        finally:
            d.cleanup()

    def test_new_project_pending_constitution_blocks_onboarding(self):
        d, root = self.make_root(constitution_state="PENDING")
        try:
            r = fr.validate_static(root)
            self.assertFalse(r["ONBOARDING_READY"])
            self.assertTrue(any("CONSTITUTION_NOT_READY_FOR_ONBOARDING" in x for x in r["BLOCKERS"]))
        finally:
            d.cleanup()

    def test_legacy_pending_is_visible_but_not_routable(self):
        d, root = self.make_root(constitution_state="LEGACY_PENDING")
        try:
            r = fr.validate_static(root)
            self.assertTrue(r["ONBOARDING_READY"])
            self.assertEqual(r["ROUTABLE_PROJECTS"], 0)
            self.assertTrue(any("LEGACY_CONSTITUTION_PENDING_WORKER_ROUTING" in x for x in r["WARNINGS"]))
        finally:
            d.cleanup()

    def test_live_report_acceptance_for_all_registered_projects(self):
        d, root = self.make_root()
        try:
            result = fr.validate_static(root)
            live = {
                "CONTROL_PLANE_VERSION":"v1.5.0",
                "PROJECTS":[
                    {"PROJECT_ID":pid,"RESULT":"PASS","SNAPSHOT":{"DISCOVERY_COMPLETE":True},"BASELINE":{"RESULT":"LOCKED"},"RECONCILIATION":{"RESULT":"RECONCILED_READ_ONLY"}}
                    for pid in ("P1","P2")
                ],
            }
            path = root / "live.json"
            path.write_text(json.dumps(live))
            result = fr.validate_live(root, path, result)
            self.assertTrue(result["ONBOARDING_READY"])
            self.assertEqual(result["READINESS_PERCENT"], 100)
        finally:
            d.cleanup()


if __name__ == "__main__":
    unittest.main()
