import copy,pytest
from saed_v4_multimodal_fusion.validation import validate_upstream
from saed_v4_multimodal_fusion.errors import IntegrityError

def args(load):return [load(p) for p in ['releases/history/strategy_factory/artifacts/saed_v4_14/V4_14_TO_V4_15_HANDOFF.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_CHECKPOINT_REGISTRY.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_ADAPTER_FEATURES.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_TOKEN_SEQUENCE.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_CALIBRATION_REPORT.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_DOMAIN_SHIFT_REPORT.JSON','releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_TOURNAMENT.JSON','releases/history/strategy_factory/artifacts/saed_v4_04/GOLDEN_MULTIMODAL_VIEW_PACKAGE.json','releases/history/strategy_factory/artifacts/saed_v4_04/V4_04_TO_V4_05_HANDOFF.json']]
def test_upstream_valid(load):assert validate_upstream(*args(load))['passed']
@pytest.mark.parametrize('index,key',[ (0,'foundation_checkpoint_registry_hash'),(0,'source_token_sequence_hash'),(0,'calibration_report_hash'),(0,'domain_shift_report_hash'),(8,'package_hash')])
def test_hash_mutations_fail(load,index,key):
 a=args(load);a[index][key]='0'*64
 with pytest.raises(IntegrityError):validate_upstream(*a)
def test_authority_mutation_fails(load):
 a=args(load);a[0]['authority']['send_order']=True
 with pytest.raises(IntegrityError):validate_upstream(*a)
