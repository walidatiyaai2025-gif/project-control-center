import copy
import unittest

from incident_governance import validate_incident


class IncidentGovernanceTests(unittest.TestCase):
    def base(self):
        return {
            "SCHEMA_VERSION": "1.0.0",
            "INCIDENT_ID": "INC-QR-2026-0001",
            "PROJECT_ID": "QR",
            "REPOSITORY": "owner/qr",
            "TARGET_SCOPE": "PROJECT",
            "TARGET_VARIANT": None,
            "SEVERITY": "P0",
            "STATE": "DETECTED",
            "PRODUCTION_BASE_SHA": "abcdef1234567890",
            "AFFECTED_PRODUCTION_VERSION": "1.0.0",
            "DISCOVERED_AT": "2026-08-26T21:00:00Z",
            "TEMPORARY_MITIGATION": {
                "APPLIED": False,
                "TASK_ID": None,
                "BRANCH": None,
                "SHA": None,
                "DEPLOYMENT_EVIDENCE": [],
                "ROLLBACK_PLAN": None,
            },
            "ROOT_CAUSE_STATUS": "UNKNOWN",
            "ROOT_CAUSE_SUMMARY": None,
            "PERMANENT_FIX_REQUIRED": True,
            "PERMANENT_FIX_TASK_ID": None,
            "PERMANENT_FIX_TARGET_VERSION": None,
            "PERMANENT_FIX_SHA": None,
            "REGRESSION_TEST_REQUIRED": True,
            "REGRESSION_TEST_EVIDENCE": [],
            "CARRY_FORWARD_TO_FUTURE_RELEASES": True,
            "RELEASE_GATE_STATE": "OPEN",
        }

    def temporary_restoration(self):
        doc = self.base()
        doc["STATE"] = "SERVICE_RESTORED_TEMPORARY"
        doc["TEMPORARY_MITIGATION"] = {
            "APPLIED": True,
            "TASK_ID": "TASK-QR-001",
            "BRANCH": "hotfix/qr-incident-0001",
            "SHA": "1234567890abcdef",
            "DEPLOYMENT_EVIDENCE": ["production verification"],
            "ROLLBACK_PLAN": "revert 1234567",
        }
        return doc

    def test_temporary_service_restoration_is_valid_but_not_closed(self):
        result = validate_incident(self.temporary_restoration())
        self.assertTrue(result["PASS"], result["ERRORS"])

    def test_tracking_requires_permanent_task_and_target_version(self):
        doc = self.temporary_restoration()
        doc["STATE"] = "TRACKED_FOR_PERMANENT_FIX"
        result = validate_incident(doc)
        self.assertFalse(result["PASS"])
        self.assertIn("PERMANENT_FIX_TASK_REQUIRED", result["ERRORS"])
        self.assertIn("PERMANENT_FIX_TARGET_VERSION_REQUIRED", result["ERRORS"])

    def test_unresolved_temporary_fix_must_carry_forward(self):
        doc = self.temporary_restoration()
        doc["CARRY_FORWARD_TO_FUTURE_RELEASES"] = False
        result = validate_incident(doc)
        self.assertFalse(result["PASS"])
        self.assertIn("TEMPORARY_MITIGATION_MUST_CARRY_FORWARD_UNTIL_PERMANENT_RESOLUTION", result["ERRORS"])

    def test_variant_scope_requires_variant(self):
        doc = self.base()
        doc["TARGET_SCOPE"] = "VARIANT"
        result = validate_incident(doc)
        self.assertFalse(result["PASS"])
        self.assertIn("VARIANT_SCOPE_REQUIRES_TARGET_VARIANT", result["ERRORS"])

    def test_temporary_fix_cannot_close_without_permanent_evidence(self):
        doc = self.temporary_restoration()
        doc["STATE"] = "CLOSED"
        doc["PERMANENT_FIX_TASK_ID"] = "TASK-QR-002"
        doc["PERMANENT_FIX_TARGET_VERSION"] = "1.0.1"
        result = validate_incident(doc)
        self.assertFalse(result["PASS"])
        self.assertIn("CLOSED_REQUIRES_CONFIRMED_ROOT_CAUSE", result["ERRORS"])
        self.assertIn("CLOSED_REQUIRES_PERMANENT_FIX_SHA", result["ERRORS"])
        self.assertIn("CLOSED_REQUIRES_REGRESSION_EVIDENCE", result["ERRORS"])
        self.assertIn("CLOSED_REQUIRES_CLEARED_RELEASE_GATE", result["ERRORS"])
        self.assertIn("CLOSED_CANNOT_RETAIN_CARRY_FORWARD_OBLIGATION", result["ERRORS"])

    def test_permanent_closure_passes_with_complete_evidence(self):
        doc = self.temporary_restoration()
        doc.update({
            "STATE": "CLOSED",
            "ROOT_CAUSE_STATUS": "CONFIRMED",
            "ROOT_CAUSE_SUMMARY": "Clock calculation used local time instead of UTC.",
            "PERMANENT_FIX_TASK_ID": "TASK-QR-002",
            "PERMANENT_FIX_TARGET_VERSION": "1.0.1",
            "PERMANENT_FIX_SHA": "fedcba0987654321",
            "REGRESSION_TEST_EVIDENCE": ["test expiry around timezone boundaries"],
            "CARRY_FORWARD_TO_FUTURE_RELEASES": False,
            "RELEASE_GATE_STATE": "CLEARED",
        })
        result = validate_incident(doc)
        self.assertTrue(result["PASS"], result["ERRORS"])


if __name__ == "__main__":
    unittest.main()
