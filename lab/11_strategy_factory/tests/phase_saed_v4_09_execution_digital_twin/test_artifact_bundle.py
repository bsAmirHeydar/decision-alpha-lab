from conftest import load

def test_claim_ledger_blocks_stronger_claims():
    c=load('lab/11_strategy_factory/artifacts/saed_v4_09/CLAIM_LEDGER.JSON');assert 'production authorization' in c['blocked_claims'];assert 'shadow replacement' in c['blocked_claims']

def test_scenario_manifest_is_complete():
    m=load('lab/11_strategy_factory/artifacts/saed_v4_09/GOLDEN_SCENARIO_MANIFEST.JSON');p=load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json');assert m['scenario_count']==len(p['scenarios']);assert set(m['scenario_ids'])=={x['scenario_id'] for x in p['scenarios']}

def test_profile_registry_marks_reference_synthetic():
    r=load('lab/11_strategy_factory/artifacts/saed_v4_09/PROFILE_REGISTRY.JSON');assert r['profiles'][0]['synthetic_watermark'];assert r['profiles'][0]['evidence_class']=='reference_synthetic'
