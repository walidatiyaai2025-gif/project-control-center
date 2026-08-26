import unittest
from scripts.output_discipline import validate_handoff
SHA="a"*40

def worker(**kw):
    d={"HANDOFF_TYPE":"WORKER_HANDOFF","RESULT_CONFIDENCE":"VERIFIED","TASK":"T-1","STATUS":"READY_FOR_QA","HEAD":SHA,"CHANGED":["x"],"VALIDATION":["tests green"],"BLOCKER":None,"NEXT_ACTION":"QA"}; d.update(kw); return d

def qa(**kw):
    d={"HANDOFF_TYPE":"QA_HANDOFF","RESULT_CONFIDENCE":"VERIFIED","QA_RESULT":"PASS","EXACT_HEAD":SHA,"BUILD_VERSION":"1.0.0","ACCEPTANCE_GATES":["A"],"FAILED_GATES":[],"EVIDENCE":[{"run":1}],"PROVENANCE_VERIFIED":True,"AUTHORITATIVE":True,"BLOCKER":None,"NEXT_ACTION":"integration"}; d.update(kw); return d

def visual(**kw):
    d={"HANDOFF_TYPE":"VISUAL_QA_HANDOFF","RESULT_CONFIDENCE":"VERIFIED","EXACT_HEAD":SHA,"REFERENCE_SOURCE":"REF01","REFERENCE_VERSION":"1","REFERENCE_SHA":SHA,"CANDIDATE_SOURCE_SHA":SHA,"CANDIDATE_ARTIFACT":"artifact-1","ARTIFACT_GENERATED_AT":"2026-08-25T00:00:00Z","PROVENANCE_VERIFIED":True,"AUTHORITATIVE":True,"DELTA":[],"CLASSIFICATION":"MATCH","QA_RESULT":"PASS","BLOCKER":None,"NEXT_ACTION":"integration"}; d.update(kw); return d

def release(**kw):
    d={"HANDOFF_TYPE":"RELEASE_HANDOFF","RESULT_CONFIDENCE":"VERIFIED","VERSION":"1.0.1","SOURCE_SHA":SHA,"BUILD_ID":"build-1","QA":"PASS","RELEASE_STATE":"RELEASED","PRODUCTION_STATE":"DEPLOYED","OPEN_PRODUCTION_INCIDENTS":[],"INCIDENT_CARRY_FORWARD":[],"ROLLBACK":"revert release","BLOCKER":None,"NEXT_ACTION":"monitor"}; d.update(kw); return d

class OutputDisciplineTests(unittest.TestCase):
    def test_final_structured_handoff_accepted(self): self.assertEqual(validate_handoff("worker",worker()),[])
    def test_narration_heavy_output_rejected(self): self.assertTrue(any("narration" in e for e in validate_handoff("worker",worker(NARRATIVE="I will check this, next I will inspect logs"))))
    def test_speculative_qa_finding_rejected(self): self.assertTrue(validate_handoff("qa",qa(NOTE="Maybe the page is broken")))
    def test_stale_screenshot_cannot_authoritative_fail(self): self.assertTrue(validate_handoff("visual_qa",visual(QA_RESULT="FAIL",PROVENANCE_VERIFIED=False)))
    def test_mismatched_artifact_sha_rejected(self): self.assertTrue(validate_handoff("qa",qa(ARTIFACT_SOURCE_SHA="b"*40)))
    def test_exact_head_qa_evidence_accepted(self): self.assertEqual(validate_handoff("qa",qa(ARTIFACT_SOURCE_SHA=SHA)),[])
    def test_contradictory_final_states_rejected(self): self.assertTrue(validate_handoff("qa",qa(SUMMARY="CI GREEN and CI FAILED")))
    def test_genuine_blocker_accepted(self):
        d=worker(RESULT_CONFIDENCE="BLOCKED",STATUS="BLOCKED",HEAD="UNKNOWN",BLOCKER="admin permission required",REQUIRED_ACTION="grant admin permission",NEXT_ACTION="rerun")
        self.assertEqual(validate_handoff("worker",d),[])
    def test_missing_head_rejected_for_exact_head_workflow(self): self.assertTrue(validate_handoff("qa",qa(EXACT_HEAD=None)))
    def test_unsupported_done_rejected(self): self.assertTrue(any("unsupported DONE"==e for e in validate_handoff("worker",worker(STATUS="DONE"))))
    def test_release_without_open_incidents_is_valid(self): self.assertEqual(validate_handoff("release",release()),[])
    def test_release_with_open_incident_requires_carry_forward(self):
        errors=validate_handoff("release",release(OPEN_PRODUCTION_INCIDENTS=["INC-QR-2026-0001"],INCIDENT_CARRY_FORWARD=[]))
        self.assertIn("open production incidents require incident carry-forward accounting",errors)
    def test_release_with_open_incident_and_carry_forward_is_valid(self):
        self.assertEqual(validate_handoff("release",release(OPEN_PRODUCTION_INCIDENTS=["INC-QR-2026-0001"],INCIDENT_CARRY_FORWARD=[{"INCIDENT_ID":"INC-QR-2026-0001","TARGET_VERSION":"1.0.2"}])),[])

if __name__=="__main__": unittest.main()
