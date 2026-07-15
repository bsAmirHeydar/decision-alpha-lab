from saed_v4_baseline_manual.service import build_bundle
from helpers import program

def test_registry_contains_null_and_manual(load,upstream):
 v,h,l,t=upstream;b=build_bundle(v,h,l,t,[program(load),program(load,'manual_conservative_reference_v1.json')]);r=b['baseline_registry'];assert r['entry_count']==3;assert {x['baseline_key'] for x in r['entries']}=={'null_abstain','manual_doctrine_reference_v1','manual_conservative_reference_v1'};assert all(x['frozen'] and not x['outcome_fitted'] for x in r['entries'])
