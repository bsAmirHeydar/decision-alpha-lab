import json

def test_registry_reference_only(load):
 r=load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert r['admitted_count']==6 and all(not x['production_eligible'] and not x['runtime_authority'] for x in r['entries'])
def test_tournament_baseline(load):
 t=load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_TOURNAMENT.JSON');assert t['baseline_preserved'] and not t['production_promotion'] and not t['treatment_authority']
