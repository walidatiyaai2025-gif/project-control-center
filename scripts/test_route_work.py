import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route_work


class RouteWorkTests(unittest.TestCase):
    def make_root(self):
        d = tempfile.TemporaryDirectory()
        root = Path(d.name)
        (root / "portfolio").mkdir(parents=True)
        (root / "portfolio/projects.yml").write_text(json.dumps({
            "PROJECTS": [
                {"PROJECT_ID": "P1", "REPOSITORY": "o/p1"},
                {"PROJECT_ID": "FAM", "REPOSITORY": "o/fam"}
            ]
        }))
        (root / "portfolio/project-routing.json").write_text(json.dumps({
            "CONTROL_PLANE_VERSION": "v1",
            "ROUTING_CONTRACT_VERSION": "1.0.0",
            "PROJECTS": [
                {
                    "PROJECT_ID": "P1", "DISPLAY_NAME": "Project One", "REPOSITORY": "o/p1",
                    "PROJECT_MODEL": "STANDALONE", "ALIASES": ["client one"],
                    "CONSTITUTION_STATE": "READY", "CONSTITUTION_PATH": "AGENTS.md",
                    "FAMILY_MANIFEST_PATH": None, "VARIANTS": []
                },
                {
                    "PROJECT_ID": "FAM", "DISPLAY_NAME": "Family", "REPOSITORY": "o/fam",
                    "PROJECT_MODEL": "PRODUCT_FAMILY", "ALIASES": ["family"],
                    "CONSTITUTION_STATE": "READY", "CONSTITUTION_PATH": "AGENTS.md",
                    "FAMILY_MANIFEST_PATH": ".pcc/project-family.json",
                    "VARIANTS": [
                        {"VARIANT_ID": "BASE", "DISPLAY_NAME": "Base", "STATUS": "ACTIVE", "ALIASES": ["base"]},
                        {"VARIANT_ID": "CLIENTA", "DISPLAY_NAME": "Client A", "STATUS": "ACTIVE", "ALIASES": ["client a", "clienta"]}
                    ]
                }
            ]
        }))
        return d, root

    def test_standalone_alias_routes(self):
        d, root = self.make_root()
        try:
            r = route_work.route(root, "client one", task="fix")
            self.assertEqual(r["ROUTING_STATUS"], "ROUTED")
            self.assertEqual(r["PROJECT_ID"], "P1")
            self.assertEqual(r["TARGET_SCOPE"], "PROJECT")
        finally:
            d.cleanup()

    def test_variant_alias_routes_directly_to_parent(self):
        d, root = self.make_root()
        try:
            r = route_work.route(root, "client a", task="branding")
            self.assertEqual(r["ROUTING_STATUS"], "ROUTED")
            self.assertEqual(r["PROJECT_ID"], "FAM")
            self.assertEqual(r["TARGET_VARIANT"], "CLIENTA")
            self.assertEqual(r["TARGET_SCOPE"], "VARIANT")
            self.assertEqual(r["CHANGE_BOUNDARY"], "CLIENTA_ONLY")
        finally:
            d.cleanup()

    def test_family_core_requires_cross_variant_validation(self):
        d, root = self.make_root()
        try:
            r = route_work.route(root, "family", scope="CORE")
            self.assertTrue(r["REQUIRES_CROSS_VARIANT_VALIDATION"])
            self.assertEqual(set(r["IMPACTED_VARIANTS"]), {"BASE", "CLIENTA"})
        finally:
            d.cleanup()

    def test_family_without_scope_or_variant_blocks(self):
        d, root = self.make_root()
        try:
            r = route_work.route(root, "family")
            self.assertEqual(r["ROUTING_STATUS"], "BLOCKED")
            self.assertEqual(r["REASON"], "TARGET_SCOPE_REQUIRED_FOR_PRODUCT_FAMILY")
        finally:
            d.cleanup()

    def test_pending_constitution_blocks_write_routing(self):
        d, root = self.make_root()
        try:
            routing = json.loads((root / "portfolio/project-routing.json").read_text())
            routing["PROJECTS"][0]["CONSTITUTION_STATE"] = "PENDING"
            (root / "portfolio/project-routing.json").write_text(json.dumps(routing))
            r = route_work.route(root, "P1")
            self.assertEqual(r["ROUTING_STATUS"], "BLOCKED")
            self.assertEqual(r["REASON"], "REPOSITORY_CONSTITUTION_NOT_READY")
        finally:
            d.cleanup()


if __name__ == "__main__":
    unittest.main()
