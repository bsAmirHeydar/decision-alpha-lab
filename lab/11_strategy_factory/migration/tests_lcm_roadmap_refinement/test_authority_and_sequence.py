import json

def test_authority_is_negative(repo_root):
    d=json.loads((repo_root/'registry/legacy_context_migration/roadmaps/LCM_ROADMAP_R1_BALANCED_PARTITION/roadmap_registry.json').read_text(encoding='utf-8'))
    assert d['authority']=={'runtime':False,'live_order':False,'capital':False,'deletion':False}
    assert all(not r['live_order_authority_created'] and not r['capital_authority_created'] for r in d['records'])

def test_sequence_chain(repo_root):
    d=json.loads((repo_root/'registry/legacy_context_migration/roadmaps/LCM_ROADMAP_R1_BALANCED_PARTITION/roadmap_registry.json').read_text(encoding='utf-8'))
    rec=d['records']
    assert rec[0]['predecessor']=='LCM-07'
    assert rec[-1]['successor'] is None
    for a,b in zip(rec,rec[1:]):
        assert a['successor']==b['subphase_id']
        assert b['predecessor']==a['subphase_id']
