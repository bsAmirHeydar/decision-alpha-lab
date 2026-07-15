import json,pytest
ARTS=['GOLDEN_SEQUENCE_MANIFEST.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','GOLDEN_DISTILLATION.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','V4_12_TO_V4_13_HANDOFF.JSON','CLAIM_LEDGER.JSON','AUTHORITY_BOUNDARY.JSON']
@pytest.mark.parametrize('name',ARTS)
def test_artifact_loads(root,name):assert json.loads((root/'lab/11_strategy_factory/artifacts/saed_v4_12'/name).read_text())
def test_claims(root):
 d=json.loads((root/'lab/11_strategy_factory/artifacts/saed_v4_12/CLAIM_LEDGER.JSON').read_text());assert d['claims']['streaming_batch_parity_reference'] and not d['claims']['live_trading']
