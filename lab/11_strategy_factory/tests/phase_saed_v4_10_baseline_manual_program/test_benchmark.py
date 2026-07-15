from saed_v4_baseline_manual.service import build_bundle
from helpers import program

def test_benchmark_is_descriptive_and_complete(load,upstream):
 v,h,l,t=upstream;b=build_bundle(v,h,l,t,[program(load),program(load,'manual_conservative_reference_v1.json')]);x=b['benchmark'];assert x['baseline_count']==3;assert x['ranking_semantics']=='none';assert not x['promotion_evidence'];assert x['synthetic_watermark'];assert b['exposure_ledger']['complete']
def test_every_baseline_has_scenario_metrics(load,upstream):
 v,h,l,t=upstream;b=build_bundle(v,h,l,t,[program(load)]);assert all(r['scenario_count']==5 and len(r['scenario_metrics'])==5 for r in b['benchmark']['results'])
