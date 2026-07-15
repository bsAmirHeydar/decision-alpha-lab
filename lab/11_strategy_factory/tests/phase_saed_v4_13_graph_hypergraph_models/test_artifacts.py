import json,pytest
ART='lab/11_strategy_factory/artifacts/saed_v4_13'
@pytest.mark.parametrize('name',['UPSTREAM_VALIDATION.JSON','GOLDEN_COMPILED_MODEL_GRAPH.JSON','GOLDEN_CANDIDATE_METRICS.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','GOLDEN_REPLAY_RECEIPT.JSON','V4_13_TO_V4_14_HANDOFF.JSON','CLAIM_LEDGER.JSON','CONFORMANCE_RESULTS.JSON'])
def test_artifact_loads(root,name):assert isinstance(json.loads((root/ART/name).read_text()),dict)
def test_conformance(root):assert json.loads((root/ART/'CONFORMANCE_RESULTS.JSON').read_text())['passed']
