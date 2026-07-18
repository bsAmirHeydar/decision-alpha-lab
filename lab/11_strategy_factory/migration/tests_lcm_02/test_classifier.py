from tools.strategy_factory.lcm.lcm_02.classifier import classify

def row(path='lab/x/context.mqh',family='EXP0018_DAYE_TRADER',language='MQL5_HEADER'):
 return {'path':path,'sha256':'sha256:'+'a'*64,'source_layer_id':'BASE','family_candidate':family,'family_confidence_bps':'8000','language':language,'extension':'.mqh','semantic_role_candidate':'UNKNOWN_ROLE'}
def test_security_precedence():
 r=classify(row('mql5/Experts/x.mq5',language='MQL5_COMPILE_UNIT'),{'ORDER_API'},{'mql5/Experts/x.mq5'},0,False); assert r['primary_disposition']=='SECURITY_RESTRICTED'; assert not r['live_order_authorized']
def test_protected_platform():
 r=classify(row('lab/11_strategy_factory/acl_os/x.py','ACL_OS_PLATFORM','PYTHON'),set(),set(),0,False); assert r['protected_platform_asset']; assert r['primary_disposition']=='KEEP_CANONICAL'
def test_generated_not_canonical():
 r=classify(row('docs/x/13_ATOMIC_CONCEPTS/a.md','DOCUMENTATION_OTHER','MARKDOWN'),set(),set(),0,False); assert r['artifact_role']=='GENERATED_PROJECTION'; assert not r['generated_projection_canonical_authority']
def test_unknown_quarantined():
 r=classify(row('lab/unknown.bin','LAB_OTHER','UNKNOWN'),set(),set(),0,False); assert r['primary_disposition']=='QUARANTINE_UNCERTAIN'
def test_exactly_one_disposition():
 r=classify(row(),set(),set(),0,False); assert isinstance(r['primary_disposition'],str)
