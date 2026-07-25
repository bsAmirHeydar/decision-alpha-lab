import hashlib,json,pytest
from saed_v4_causal_treatment_policy_value.canonical import content_hash,artifact_hash

@pytest.mark.parametrize('name',[
 'GOLDEN_UPSTREAM_VALIDATION.JSON','GOLDEN_SPLIT_AUDIT.JSON','GOLDEN_OVERLAP_REPORT.JSON','GOLDEN_ATE_REPORT.JSON','GOLDEN_CATE_REPORT.JSON','GOLDEN_POLICY_VALUE_REPORT.JSON','GOLDEN_NEGATIVE_CONTROL_REPORT.JSON','GOLDEN_POLICY_TOURNAMENT.JSON','GOLDEN_CLAIM_TIER_REPORT.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','GOLDEN_REPLAY_RECEIPT.JSON','V4_18_TO_V4_19_HANDOFF.JSON'])
def test_artifact_exists(root,art,name):assert (root/art/name).is_file()

def test_integrity_receipt(load,art):
 x=load(f'{art}/GOLDEN_INTEGRITY_RECEIPT.JSON');assert x['all_hashes_verified'] and x['immutable'] and x['artifact_count']>25

def test_registry_immutable(load,art):
 x=load(f'{art}/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert x['immutable'] and not x['production_registry'] and len(x['checkpoints'])==7

def test_claim_ceiling(load,art):
 x=load(f'{art}/GOLDEN_CLAIM_TIER_REPORT.JSON');assert x['claim_tier'] in {'synthetic_treatment_and_policy_value','abstain'} and not x['real_treatment_effect'] and not x['real_policy_value'] and not x['production_authorization']

def test_handoff_narrow(load,art):
 h=load(f'{art}/V4_18_TO_V4_19_HANDOFF.JSON');assert h['next_phase']=='SAED_V4_19' and all(h['entry_gates'].values()) and not h['authority']['select_live_treatment'] and not h['authority']['sign_promotion'] and not h['authority']['send_order']

def test_replay_deterministic(load,art):assert load(f'{art}/GOLDEN_REPLAY_RECEIPT.JSON')['deterministic']
