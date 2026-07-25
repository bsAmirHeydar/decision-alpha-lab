import json,pytest
@pytest.mark.parametrize('name',['AUTHORITY_BOUNDARY.JSON','CLAIM_LEDGER.JSON','CONFORMANCE_RESULTS.JSON','GOLDEN_ALIGNED_VIEW_SET.JSON','GOLDEN_DOMAIN_SUBSET_MATRIX.JSON','GOLDEN_FOUNDATION_SUBSET_MATRIX.JSON','GOLDEN_FUSION_OUTPUTS.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','V4_15_TO_V4_16_HANDOFF.JSON'])
def test_artifact_exists(root,name):
 p=root/'releases/history/strategy_factory/artifacts/saed_v4_15'/name;assert p.is_file();json.loads(p.read_text())
def test_claims_conservative(load):
 c=load('releases/history/strategy_factory/artifacts/saed_v4_15/CLAIM_LEDGER.JSON')['claims'];assert c['multimodal_fusion_boundary_implemented'] and c['explicit_missingness_masks'] and not c['economic_uplift_established'] and not c['production_authorization'] and not c['live_trading']
def test_conformance(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_15/CONFORMANCE_RESULTS.JSON')['passed']
