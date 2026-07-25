from tools.strategy_factory.acl_os.acl_07.gate_engine import preliminary,replace_family_gates
from tools.strategy_factory.acl_os.acl_07.handoff_input import load_acl06_bundle

def _first(acl06_root,policy):
 b=load_acl06_bundle(acl06_root); c=dict(b['candidates'][0]); c['_test_accuracy']=b['segments_by_setup'][c['setup_id']]['TEST']['accuracy']; return c,b['segments_by_setup'][c['setup_id']],b
def test_preliminary_has_all_gates(acl06_root,policy):
 c,s,b=_first(acl06_root,policy); assert len(preliminary(c,s,policy,b['bundle_digest']))==15
def test_support_fails_reference(acl06_root,policy):
 c,s,b=_first(acl06_root,policy); assert preliminary(c,s,policy,b['bundle_digest'])['MINIMUM_SUPPORT']['status']=='FAIL'
def test_economics_unknown(acl06_root,policy):
 c,s,b=_first(acl06_root,policy); assert preliminary(c,s,policy,b['bundle_digest'])['EXECUTION_ECONOMICS']['status']=='UNKNOWN'
def test_prospective_unknown(acl06_root,policy):
 c,s,b=_first(acl06_root,policy); assert preliminary(c,s,policy,b['bundle_digest'])['PROSPECTIVE_EVIDENCE']['status']=='UNKNOWN'
def test_family_gate_replacement(acl06_root,policy):
 c,s,b=_first(acl06_root,policy); g=preliminary(c,s,policy,b['bundle_digest']); replace_family_gates(g,c,0.2,0.6,policy); assert g['MULTIPLE_TESTING']['status']=='FAIL'
def test_diagnostic_not_applicable_family(acl06_root,policy):
 b=load_acl06_bundle(acl06_root); c=next(dict(x) for x in b['candidates'] if x['lane']=='DIAGNOSTIC'); c['_test_accuracy']=b['segments_by_setup'][c['setup_id']]['TEST']['accuracy']; g=preliminary(c,b['segments_by_setup'][c['setup_id']],policy,b['bundle_digest']); replace_family_gates(g,c,None,0.6,policy); assert g['BASELINE_DOMINANCE']['status']=='NOT_APPLICABLE'
