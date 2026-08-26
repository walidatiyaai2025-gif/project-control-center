from __future__ import annotations
import argparse, json, re
from pathlib import Path

CONFIDENCE={"VERIFIED","PARTIALLY_VERIFIED","BLOCKED","UNKNOWN"}
SHA40=re.compile(r"^[0-9a-f]{40}$")
REQUIRED={
"worker":["HANDOFF_TYPE","RESULT_CONFIDENCE","TASK","STATUS","HEAD","CHANGED","VALIDATION","BLOCKER","NEXT_ACTION"],
"qa":["HANDOFF_TYPE","RESULT_CONFIDENCE","QA_RESULT","EXACT_HEAD","BUILD_VERSION","ACCEPTANCE_GATES","FAILED_GATES","EVIDENCE","PROVENANCE_VERIFIED","AUTHORITATIVE","BLOCKER","NEXT_ACTION"],
"ci":["HANDOFF_TYPE","RESULT_CONFIDENCE","EXACT_HEAD","WORKFLOW","JOB","STEP","TEST","ROOT_CAUSE","CLASSIFICATION","OWNER","BLOCKER","NEXT_ACTION"],
"visual_qa":["HANDOFF_TYPE","RESULT_CONFIDENCE","EXACT_HEAD","REFERENCE_SOURCE","REFERENCE_VERSION","REFERENCE_SHA","CANDIDATE_SOURCE_SHA","CANDIDATE_ARTIFACT","ARTIFACT_GENERATED_AT","PROVENANCE_VERIFIED","AUTHORITATIVE","DELTA","CLASSIFICATION","QA_RESULT","BLOCKER","NEXT_ACTION"],
"integration":["HANDOFF_TYPE","RESULT_CONFIDENCE","INTEGRATION_HEAD","CANDIDATE","MERGE_STATE","CI","QA","BLOCKERS","RESULT","NEXT_ACTION"],
"release":["HANDOFF_TYPE","RESULT_CONFIDENCE","VERSION","SOURCE_SHA","BUILD_ID","QA","RELEASE_STATE","PRODUCTION_STATE","OPEN_PRODUCTION_INCIDENTS","INCIDENT_CARRY_FORWARD","ROLLBACK","BLOCKER","NEXT_ACTION"]}
TYPE_EXPECTED={"worker":"WORKER_HANDOFF","qa":"QA_HANDOFF","ci":"CI_HANDOFF","visual_qa":"VISUAL_QA_HANDOFF","integration":"INTEGRATION_HANDOFF","release":"RELEASE_HANDOFF"}
HEAD_KEY={"worker":"HEAD","qa":"EXACT_HEAD","ci":"EXACT_HEAD","visual_qa":"EXACT_HEAD","integration":"INTEGRATION_HEAD","release":"SOURCE_SHA"}
PROHIBITED=("i will check","i am reviewing","i found the first","next i will","i will now compare","next i will inspect","it seems","probably","maybe","i suspect")

def _strings(value):
    if isinstance(value,str): yield value
    elif isinstance(value,dict):
        for v in value.values(): yield from _strings(v)
    elif isinstance(value,list):
        for v in value: yield from _strings(v)

def _nonempty(value):
    if value is None: return False
    if isinstance(value,(str,list,dict)): return len(value)>0
    return True

def _blocked(data):
    return data.get("RESULT_CONFIDENCE")=="BLOCKED" or data.get("STATUS")=="BLOCKED" or data.get("RESULT")=="BLOCKED" or data.get("QA_RESULT")=="BLOCKED"

def validate_handoff(kind:str,data:dict)->list[str]:
    errors=[]
    if kind not in REQUIRED: return [f"unknown handoff kind {kind}"]
    if data.get("HANDOFF_TYPE")!=TYPE_EXPECTED[kind]: errors.append("HANDOFF_TYPE mismatch")
    if data.get("RESULT_CONFIDENCE") not in CONFIDENCE: errors.append("invalid RESULT_CONFIDENCE")
    blocked=_blocked(data)
    if blocked:
        head=data.get(HEAD_KEY[kind])
        if not _nonempty(head): errors.append("blocker missing exact HEAD or explicit UNKNOWN")
        if not _nonempty(data.get("BLOCKER") or (data.get("BLOCKERS") if kind=="integration" else None)): errors.append("blocker missing BLOCKER")
        if not _nonempty(data.get("REQUIRED_ACTION")): errors.append("blocker missing REQUIRED_ACTION")
        if not _nonempty(data.get("NEXT_ACTION")): errors.append("blocker missing NEXT_ACTION")
    else:
        for field in REQUIRED[kind]:
            if field not in data: errors.append(f"missing {field}")
        head=data.get(HEAD_KEY[kind])
        if not isinstance(head,str) or not SHA40.fullmatch(head): errors.append("missing or invalid exact HEAD")
    if data.get("STATUS")=="DONE": errors.append("unsupported DONE")
    text="\n".join(_strings(data)).lower()
    for phrase in PROHIBITED:
        if phrase in text: errors.append(f"narration/speculation prohibited: {phrase}")
    if "ci green" in text and "ci failed" in text: errors.append("contradictory CI states")
    if "qa pass" in text and "qa fail" in text: errors.append("contradictory QA states")
    if "mergeable" in text and "not_mergeable" in text: errors.append("contradictory merge states")
    if kind=="qa":
        authoritative=bool(data.get("AUTHORITATIVE")); result=data.get("QA_RESULT")
        if authoritative and result in {"PASS","FAIL"}:
            if not data.get("PROVENANCE_VERIFIED"): errors.append("authoritative QA requires verified provenance")
            if not _nonempty(data.get("EVIDENCE")): errors.append("authoritative QA requires evidence")
        if result=="PASS" and _nonempty(data.get("FAILED_GATES")): errors.append("QA PASS with failed gates")
        artifact_sha=data.get("ARTIFACT_SOURCE_SHA")
        if artifact_sha and artifact_sha!=data.get("EXACT_HEAD"): errors.append("artifact SHA does not match exact HEAD")
    if kind=="visual_qa":
        authoritative=bool(data.get("AUTHORITATIVE")); result=data.get("QA_RESULT")
        if data.get("CANDIDATE_SOURCE_SHA")!=data.get("EXACT_HEAD"): errors.append("candidate artifact SHA does not match exact HEAD")
        if authoritative and result in {"PASS","FAIL"} and not data.get("PROVENANCE_VERIFIED"): errors.append("stale/unverified visual artifact cannot produce authoritative QA")
        if authoritative and result in {"PASS","FAIL"}:
            for f in ("REFERENCE_SOURCE","REFERENCE_VERSION","CANDIDATE_ARTIFACT","ARTIFACT_GENERATED_AT"):
                if not _nonempty(data.get(f)): errors.append(f"authoritative visual QA missing {f}")
    if kind=="integration" and str(data.get("RESULT")).upper() in {"PASS","READY","MERGED"} and _nonempty(data.get("BLOCKERS")):
        errors.append("successful integration result has blockers")
    if kind=="release":
        if str(data.get("RELEASE_STATE")).upper()=="RELEASED" and str(data.get("QA")).upper() in {"FAIL","FAILED"}:
            errors.append("released state contradicts QA failure")
        incidents=data.get("OPEN_PRODUCTION_INCIDENTS")
        if isinstance(incidents,list) and incidents and not _nonempty(data.get("INCIDENT_CARRY_FORWARD")):
            errors.append("open production incidents require incident carry-forward accounting")
    return errors

def main():
    p=argparse.ArgumentParser(); p.add_argument("--type",choices=sorted(REQUIRED),required=True); p.add_argument("--input",required=True)
    a=p.parse_args(); data=json.loads(Path(a.input).read_text(encoding="utf-8")); errors=validate_handoff(a.type,data)
    print(json.dumps({"PASS":not errors,"ERRORS":errors},indent=2)); raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()
