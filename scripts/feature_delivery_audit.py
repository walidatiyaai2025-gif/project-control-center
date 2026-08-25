from __future__ import annotations
import argparse, json
from pathlib import Path

DIMENSION_STATES={"NOT_APPLICABLE","NOT_STARTED","IN_PROGRESS","IMPLEMENTED","CONNECTED","VERIFIED","FAILED","BLOCKED"}
CODE_DIMS={"BACKEND_IMPLEMENTED","DATABASE_IMPLEMENTED","API_IMPLEMENTED","SERVICE_IMPLEMENTED","UI_IMPLEMENTED"}
CONNECTIVITY_DIMS={"NAVIGATION_CONNECTED","UI_API_CONNECTED","DATA_BINDING_CONNECTED","MUTATION_CONNECTED","PERMISSIONS_CONNECTED","VALIDATION_CONNECTED","BACKGROUND_PROCESS_CONNECTED","NOTIFICATION_CONNECTED","FEATURE_FLAG_ENABLED"}
VERIFY_DIMS={"PERSISTENCE_VERIFIED","RELOAD_VERIFIED","END_TO_END_VERIFIED","QA_VERIFIED"}
UX_DIMS={"LOADING_STATE_IMPLEMENTED","EMPTY_STATE_IMPLEMENTED","ERROR_STATE_IMPLEMENTED","RETRY_IMPLEMENTED"}

def is_pass(name,state):
    if state=="NOT_APPLICABLE": return True
    if name.endswith("_IMPLEMENTED") or name in {"REQUIREMENT_DEFINED","BUSINESS_RULES_DEFINED"}: return state in {"IMPLEMENTED","CONNECTED","VERIFIED"}
    if name.endswith("_CONNECTED") or name=="FEATURE_FLAG_ENABLED": return state in {"CONNECTED","VERIFIED"}
    return state=="VERIFIED"

def pct(dimensions,names):
    vals=[(k,v) for k,v in dimensions.items() if k in names and v!="NOT_APPLICABLE"]
    if not vals: return None
    return round(100*sum(is_pass(k,v) for k,v in vals)/len(vals),1)

def any_progress(d,names):
    return any(v not in {"NOT_APPLICABLE","NOT_STARTED"} for k,v in d.items() if k in names)

def all_applicable_pass(d,exclude=None):
    exclude=exclude or set(); vals=[(k,v) for k,v in d.items() if k not in exclude and v!="NOT_APPLICABLE"]
    return bool(vals) and all(is_pass(k,v) for k,v in vals)

def derive_feature_state(feature):
    d=feature.get("DIMENSIONS",{}); delivery=feature.get("DELIVERY_TYPE","CUSTOMER_UI")
    if d.get("QA_VERIFIED")=="FAILED" or d.get("END_TO_END_VERIFIED")=="FAILED": return "QA_FAILED"
    backend=any_progress(d,{"BACKEND_IMPLEMENTED","API_IMPLEMENTED","SERVICE_IMPLEMENTED","DATABASE_IMPLEMENTED"}); ui=any_progress(d,{"UI_IMPLEMENTED"})
    if backend and delivery!="API_ONLY" and d.get("UI_IMPLEMENTED") in {"NOT_STARTED","FAILED","BLOCKED"}: return "BACKEND_ONLY"
    if ui and delivery!="UI_ONLY" and not backend and any(d.get(k)!="NOT_APPLICABLE" for k in {"BACKEND_IMPLEMENTED","API_IMPLEMENTED","SERVICE_IMPLEMENTED"}): return "UI_ONLY"
    implemented=any_progress(d,CODE_DIMS)
    connectivity=[(k,v) for k,v in d.items() if k in CONNECTIVITY_DIMS and v!="NOT_APPLICABLE"]
    if implemented and connectivity and not all(is_pass(k,v) for k,v in connectivity): return "IMPLEMENTED_NOT_CONNECTED"
    if implemented and connectivity and all(is_pass(k,v) for k,v in connectivity) and d.get("END_TO_END_VERIFIED")!="NOT_APPLICABLE" and not is_pass("END_TO_END_VERIFIED",d.get("END_TO_END_VERIFIED","NOT_STARTED")): return "CONNECTED_NOT_VERIFIED"
    if d.get("END_TO_END_VERIFIED")!="NOT_APPLICABLE" and is_pass("END_TO_END_VERIFIED",d.get("END_TO_END_VERIFIED","NOT_STARTED")) and d.get("QA_VERIFIED")!="NOT_APPLICABLE" and not is_pass("QA_VERIFIED",d.get("QA_VERIFIED","NOT_STARTED")): return "END_TO_END_WORKING"
    if d.get("QA_VERIFIED")!="NOT_APPLICABLE" and is_pass("QA_VERIFIED",d.get("QA_VERIFIED","NOT_STARTED")):
        pre=all_applicable_pass(d,{"RELEASED","USER_ACCEPTED"}); released=d.get("RELEASED")=="NOT_APPLICABLE" or is_pass("RELEASED",d.get("RELEASED","NOT_STARTED")); accepted=d.get("USER_ACCEPTED")=="NOT_APPLICABLE" or is_pass("USER_ACCEPTED",d.get("USER_ACCEPTED","NOT_STARTED")); official=bool(feature.get("PRESENT_IN_CANDIDATE") or feature.get("PRESENT_IN_PRODUCTION"))
        if pre and not released and official: return "CUSTOMER_READY"
        if pre and released and feature.get("PRESENT_IN_PRODUCTION") and not accepted: return "RELEASED"
        if pre and released and feature.get("PRESENT_IN_PRODUCTION") and accepted and all_applicable_pass(d): return "DONE"
        return "QA_VERIFIED"
    if not implemented and not any_progress(d,set(d)): return "PLANNED"
    if implemented: return "PARTIALLY_IMPLEMENTED"
    return "IMPLEMENTATION_STARTED"

def audit_feature(feature):
    d=feature.get("DIMENSIONS",{}); findings=[]
    for k,v in d.items():
        if v not in DIMENSION_STATES: findings.append({"TYPE":"INVALID_DIMENSION_STATE","DETAIL":f"{k}={v}"})
    state=derive_feature_state(feature); declared=feature.get("SUMMARY_STATE")
    if declared and declared!=state: findings.append({"TYPE":"DERIVED_STATE_MISMATCH","DETAIL":f"declared={declared} derived={state}"})
    if state=="BACKEND_ONLY": findings.append({"TYPE":"BACKEND_ONLY_FEATURE"})
    if state=="UI_ONLY": findings.append({"TYPE":"UI_ONLY_FEATURE"})
    if state=="IMPLEMENTED_NOT_CONNECTED": findings.append({"TYPE":"UNCONNECTED_FEATURE"})
    if d.get("API_IMPLEMENTED") in {"IMPLEMENTED","CONNECTED","VERIFIED"} and d.get("UI_API_CONNECTED") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"} and feature.get("DELIVERY_TYPE","CUSTOMER_UI")!="API_ONLY": findings.append({"TYPE":"MISSING_UI_BINDING"})
    if d.get("UI_IMPLEMENTED") in {"IMPLEMENTED","CONNECTED","VERIFIED"} and d.get("NAVIGATION_CONNECTED") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"}: findings.append({"TYPE":"MISSING_NAVIGATION"})
    if d.get("MUTATION_CONNECTED") in {"CONNECTED","VERIFIED"} and (d.get("PERSISTENCE_VERIFIED") not in {"NOT_APPLICABLE","VERIFIED"} or d.get("RELOAD_VERIFIED") not in {"NOT_APPLICABLE","VERIFIED"}): findings.append({"TYPE":"PERSISTENCE_GAP"})
    if feature.get("USES_FAKE_DATA") is True: findings.append({"TYPE":"FAKE_DATA_PATH"})

    signals=feature.get("DETECTION_SIGNALS",{}) or {}
    if signals.get("UNUSED_PRODUCTION_SERVICE"): findings.append({"TYPE":"DEAD_CODE_CANDIDATE","DETAIL":"UNUSED_PRODUCTION_SERVICE"})
    if signals.get("ENDPOINT_WITHOUT_EXPECTED_CONSUMER"): findings.append({"TYPE":"UNUSED_ENDPOINT","DETAIL":"ENDPOINT_WITHOUT_EXPECTED_CONSUMER"})
    if signals.get("BACKGROUND_JOB_WITHOUT_CONSUMER"): findings.append({"TYPE":"MISSING_CONSUMER","DETAIL":"BACKGROUND_JOB_WITHOUT_CONSUMER"})
    if signals.get("EVENT_PRODUCER_WITHOUT_LISTENER"): findings.append({"TYPE":"MISSING_CONSUMER","DETAIL":"EVENT_PRODUCER_WITHOUT_LISTENER"})
    if signals.get("NOTIFICATION_PATH_DISCONNECTED"): findings.append({"TYPE":"UNCONNECTED_FEATURE","DETAIL":"NOTIFICATION_PATH_DISCONNECTED"})
    if signals.get("DUPLICATE_LOCAL_ONLY_IMPLEMENTATION"): findings.append({"TYPE":"UNCONNECTED_FEATURE","DETAIL":"DUPLICATE_LOCAL_ONLY_IMPLEMENTATION"})

    expected=set(feature.get("EXPECTED_CONSUMERS",[]) or []); observed=set(feature.get("OBSERVED_CONSUMERS",[]) or [])
    if d.get("API_IMPLEMENTED") in {"IMPLEMENTED","CONNECTED","VERIFIED"} and expected and not expected.intersection(observed):
        findings.append({"TYPE":"UNUSED_ENDPOINT","DETAIL":"NO_EXPECTED_CONSUMER_OBSERVED"})
        findings.append({"TYPE":"MISSING_CONSUMER","DETAIL":"EXPECTED_CONSUMER_NOT_OBSERVED"})

    if feature.get("PRESENT_IN_DEVELOPMENT") and not (feature.get("PRESENT_IN_CANDIDATE") or feature.get("PRESENT_IN_PRODUCTION")): findings.append({"TYPE":"NOT_IN_OFFICIAL_BUILD"})
    elif d.get("CUSTOMER_VISIBLE")=="VERIFIED" and not (feature.get("PRESENT_IN_CANDIDATE") or feature.get("PRESENT_IN_PRODUCTION")): findings.append({"TYPE":"NOT_IN_OFFICIAL_BUILD"})
    if d.get("CUSTOMER_VISIBLE")=="VERIFIED" and d.get("QA_VERIFIED") not in {"NOT_APPLICABLE","VERIFIED"}: findings.append({"TYPE":"CUSTOMER_VISIBLE_WITHOUT_QA"})
    if d.get("RELEASED")=="VERIFIED" and not feature.get("PRESENT_IN_PRODUCTION"): findings.append({"TYPE":"RELEASE_IDENTITY_GAP"})
    if d.get("FEATURE_FLAG_ENABLED") in {"NOT_STARTED","FAILED","BLOCKED"} and any(is_pass(k,v) for k,v in d.items() if k in CODE_DIMS): findings.append({"TYPE":"UNCONNECTED_FEATURE","DETAIL":"FEATURE_FLAG_OFF"})
    if declared=="DONE" and (state!="DONE" or findings): findings.append({"TYPE":"FALSE_DONE_FEATURE"})
    metrics={"CODE_COMPLETION":pct(d,CODE_DIMS),"CONNECTIVITY_COMPLETION":pct(d,CONNECTIVITY_DIMS),"QA_COMPLETION":pct(d,VERIFY_DIMS|UX_DIMS),"CUSTOMER_READY_COMPLETION":pct(d,VERIFY_DIMS|CONNECTIVITY_DIMS|{"CUSTOMER_VISIBLE"}),"RELEASE_COMPLETION":pct(d,{"RELEASED","USER_ACCEPTED"})}
    return state,findings,metrics

def audit_screen(screen):
    d=screen.get("DIMENSIONS",{}); findings=[]
    if d.get("ROUTE_EXISTS") in {"IMPLEMENTED","CONNECTED","VERIFIED"} and d.get("NAVIGATION_REACHABLE") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"} and not screen.get("INTENTIONALLY_HIDDEN",False): findings.append({"TYPE":"UNREACHABLE_SCREEN"})
    if d.get("REAL_DATA_CONNECTED") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"} and d.get("CUSTOMER_VISIBLE")=="VERIFIED": findings.append({"TYPE":"FAKE_OR_DISCONNECTED_DATA_RISK"})
    visual={"SCREEN_DEFINED","DESIGN_IMPLEMENTED","RESPONSIVE","ACCESSIBILITY","RTL","LTR"}; functional=set(d)-visual
    return findings,pct(d,visual),pct(d,functional)

def audit_action(action):
    d=action.get("DIMENSIONS",{}); findings=[]
    if d.get("VISIBLE")=="VERIFIED" and d.get("HANDLER_CONNECTED") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"}: findings.append({"TYPE":"UNCONNECTED_FEATURE","DETAIL":"VISIBLE_ACTION_WITHOUT_HANDLER"})
    if d.get("HANDLER_CONNECTED") in {"CONNECTED","VERIFIED"} and d.get("BACKEND_CONNECTED") not in {"NOT_APPLICABLE","CONNECTED","VERIFIED"}: findings.append({"TYPE":"MISSING_CONSUMER"})
    if action.get("STATE_CHANGING"):
        if d.get("PERSISTENCE")!="VERIFIED" or d.get("RELOAD_VERIFICATION")!="VERIFIED": findings.append({"TYPE":"PERSISTENCE_GAP"})
        if d.get("SUCCESS_PATH")=="VERIFIED" and (d.get("BACKEND_CONNECTED") not in {"CONNECTED","VERIFIED"} or d.get("PERSISTENCE")!="VERIFIED"): findings.append({"TYPE":"FALSE_SUCCESS_RISK"})
        if action.get("SUCCESS_CONFIRMED_BY") not in {"SERVER_AUTHORITATIVE","SERVER_COMMIT_AND_RECONCILIATION"}: findings.append({"TYPE":"FALSE_SUCCESS_RISK","DETAIL":"SUCCESS_AUTHORITY_NOT_SERVER_CONFIRMED"})
    return findings

def audit_documents(matrix,screens,actions):
    report={"FEATURES":[],"SCREENS":[],"ACTIONS":[],"FINDINGS":[]}
    for f in matrix.get("FEATURES",[]):
        state,findings,metrics=audit_feature(f); report["FEATURES"].append({"FEATURE_ID":f.get("FEATURE_ID"),"DERIVED_STATE":state,**metrics,"FINDINGS":findings})
        report["FINDINGS"] += [{"FEATURE_ID":f.get("FEATURE_ID"),**x} for x in findings]
    for s in screens.get("SCREENS",[]):
        findings,visual,functional=audit_screen(s); report["SCREENS"].append({"SCREEN_ID":s.get("SCREEN_ID"),"VISUAL_COMPLETION":visual,"FUNCTIONAL_COMPLETION":functional,"FINDINGS":findings}); report["FINDINGS"] += [{"SCREEN_ID":s.get("SCREEN_ID"),**x} for x in findings]
    for screen in actions.get("SCREENS",[]):
        for a in screen.get("ACTIONS",[]):
            findings=audit_action(a); report["ACTIONS"].append({"SCREEN_ID":screen.get("SCREEN_ID"),"ACTION_ID":a.get("ACTION_ID"),"FINDINGS":findings}); report["FINDINGS"] += [{"SCREEN_ID":screen.get("SCREEN_ID"),"ACTION_ID":a.get("ACTION_ID"),**x} for x in findings]
    counts={}
    for finding in report["FINDINGS"]: counts[finding["TYPE"]]=counts.get(finding["TYPE"],0)+1
    gap_types={"UNCONNECTED_FEATURE","MISSING_UI_BINDING","MISSING_NAVIGATION","MISSING_CONSUMER","UNUSED_ENDPOINT","PERSISTENCE_GAP","FALSE_SUCCESS_RISK","UNREACHABLE_SCREEN","BACKEND_ONLY_FEATURE","UI_ONLY_FEATURE","NOT_IN_OFFICIAL_BUILD","CUSTOMER_VISIBLE_WITHOUT_QA"}
    report["SUMMARY"]={"FALSE_DONE_FEATURES":counts.get("FALSE_DONE_FEATURE",0),"INTEGRATION_GAPS":sum(v for k,v in counts.items() if k in gap_types),"DEAD_CODE_CANDIDATES":counts.get("DEAD_CODE_CANDIDATE",0),"UNUSED_ENDPOINTS":counts.get("UNUSED_ENDPOINT",0),"MISSING_CONSUMERS":counts.get("MISSING_CONSUMER",0),"UNREACHABLE_SCREENS":counts.get("UNREACHABLE_SCREEN",0),"BACKEND_ONLY_FEATURES":counts.get("BACKEND_ONLY_FEATURE",0),"UI_ONLY_FEATURES":counts.get("UI_ONLY_FEATURE",0),"MISSING_BINDINGS":counts.get("MISSING_UI_BINDING",0),"CUSTOMER_READY_FEATURES":sum(r["DERIVED_STATE"] in {"CUSTOMER_READY","RELEASED","USER_ACCEPTED","DONE"} for r in report["FEATURES"])}
    report["PASS"]=report["SUMMARY"]["FALSE_DONE_FEATURES"]==0
    return report

def load_json(path): return json.loads(Path(path).read_text())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--matrix",required=True); ap.add_argument("--screens",required=True); ap.add_argument("--actions",required=True); ap.add_argument("--report-out"); args=ap.parse_args()
    report=audit_documents(load_json(args.matrix),load_json(args.screens),load_json(args.actions)); out=json.dumps(report,indent=2)
    if args.report_out: Path(args.report_out).write_text(out+"\n")
    print(out); raise SystemExit(0 if report["PASS"] else 2)
if __name__=="__main__": main()
