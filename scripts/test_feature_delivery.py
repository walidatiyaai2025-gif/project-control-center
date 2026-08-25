import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('fd',ROOT/'scripts/feature_delivery_audit.py'); fd=importlib.util.module_from_spec(spec); spec.loader.exec_module(fd)

def base_dims():
    return {k:'NOT_APPLICABLE' for k in ['REQUIREMENT_DEFINED','BUSINESS_RULES_DEFINED','BACKEND_IMPLEMENTED','DATABASE_IMPLEMENTED','API_IMPLEMENTED','SERVICE_IMPLEMENTED','UI_IMPLEMENTED','NAVIGATION_CONNECTED','UI_API_CONNECTED','DATA_BINDING_CONNECTED','MUTATION_CONNECTED','PERMISSIONS_CONNECTED','VALIDATION_CONNECTED','LOADING_STATE_IMPLEMENTED','EMPTY_STATE_IMPLEMENTED','ERROR_STATE_IMPLEMENTED','RETRY_IMPLEMENTED','PERSISTENCE_VERIFIED','RELOAD_VERIFIED','BACKGROUND_PROCESS_CONNECTED','NOTIFICATION_CONNECTED','FEATURE_FLAG_ENABLED','END_TO_END_VERIFIED','QA_VERIFIED','CUSTOMER_VISIBLE','RELEASED','USER_ACCEPTED']}

class FeatureDeliveryTests(unittest.TestCase):
    def test_implemented_not_connected(self):
        d=base_dims(); d.update(BACKEND_IMPLEMENTED='IMPLEMENTED',API_IMPLEMENTED='IMPLEMENTED',UI_IMPLEMENTED='IMPLEMENTED',NAVIGATION_CONNECTED='CONNECTED',UI_API_CONNECTED='NOT_STARTED')
        state,findings,_=fd.audit_feature({'FEATURE_ID':'F','DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d})
        self.assertEqual(state,'IMPLEMENTED_NOT_CONNECTED'); self.assertIn('MISSING_UI_BINDING',{x['TYPE'] for x in findings})
    def test_backend_only(self):
        d=base_dims(); d.update(BACKEND_IMPLEMENTED='IMPLEMENTED',API_IMPLEMENTED='IMPLEMENTED',UI_IMPLEMENTED='NOT_STARTED')
        self.assertEqual(fd.derive_feature_state({'DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d}),'BACKEND_ONLY')
    def test_ui_only(self):
        d=base_dims(); d.update(UI_IMPLEMENTED='IMPLEMENTED',BACKEND_IMPLEMENTED='NOT_STARTED',API_IMPLEMENTED='NOT_STARTED')
        self.assertEqual(fd.derive_feature_state({'DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d}),'UI_ONLY')
    def test_false_done_is_detected(self):
        d=base_dims(); d.update(BACKEND_IMPLEMENTED='IMPLEMENTED',API_IMPLEMENTED='IMPLEMENTED',UI_IMPLEMENTED='IMPLEMENTED',UI_API_CONNECTED='NOT_STARTED')
        _,findings,_=fd.audit_feature({'FEATURE_ID':'F','SUMMARY_STATE':'DONE','DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d})
        self.assertIn('FALSE_DONE_FEATURE',{x['TYPE'] for x in findings})
    def test_unreachable_screen(self):
        findings,_,_=fd.audit_screen({'DIMENSIONS':{'ROUTE_EXISTS':'IMPLEMENTED','NAVIGATION_REACHABLE':'NOT_STARTED'}})
        self.assertIn('UNREACHABLE_SCREEN',{x['TYPE'] for x in findings})
    def test_persistence_and_false_success(self):
        action={'STATE_CHANGING':True,'SUCCESS_CONFIRMED_BY':'LOCAL_ONLY','DIMENSIONS':{'VISIBLE':'VERIFIED','HANDLER_CONNECTED':'CONNECTED','BACKEND_CONNECTED':'CONNECTED','SUCCESS_PATH':'VERIFIED','PERSISTENCE':'NOT_STARTED','RELOAD_VERIFICATION':'NOT_STARTED'}}
        types={x['TYPE'] for x in fd.audit_action(action)}; self.assertIn('PERSISTENCE_GAP',types); self.assertIn('FALSE_SUCCESS_RISK',types)
    def test_customer_ready_requires_official_candidate(self):
        d=base_dims(); d.update({k:'VERIFIED' for k in d if k not in {'RELEASED','USER_ACCEPTED'}}); d['RELEASED']='NOT_STARTED'; d['USER_ACCEPTED']='NOT_STARTED'
        f={'DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d,'PRESENT_IN_CANDIDATE':False,'PRESENT_IN_PRODUCTION':False}
        self.assertEqual(fd.derive_feature_state(f),'QA_VERIFIED'); f['PRESENT_IN_CANDIDATE']=True; self.assertEqual(fd.derive_feature_state(f),'CUSTOMER_READY')
    def test_released_requires_production_presence(self):
        d=base_dims(); d.update({k:'VERIFIED' for k in d}); d['USER_ACCEPTED']='NOT_STARTED'
        f={'DELIVERY_TYPE':'CUSTOMER_UI','DIMENSIONS':d,'PRESENT_IN_CANDIDATE':True,'PRESENT_IN_PRODUCTION':False}
        _,findings,_=fd.audit_feature(f); self.assertIn('RELEASE_IDENTITY_GAP',{x['TYPE'] for x in findings})
if __name__=='__main__': unittest.main()
