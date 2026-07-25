import copy,pytest
from saed_v4_distributional_survival_tail.validation import validate_upstream
from saed_v4_distributional_survival_tail.errors import IntegrityError

def args(load):return [load(p) for p in ['releases/history/strategy_factory/artifacts/saed_v4_15/V4_15_TO_V4_16_HANDOFF.JSON','releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_CHECKPOINT_REGISTRY.JSON','releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUSION_OUTPUTS.JSON','releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_ALIGNED_VIEW_SET.JSON','releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_INTEGRITY_RECEIPT.JSON']]
def test_upstream_valid(load):assert validate_upstream(*args(load))['passed']
@pytest.mark.parametrize('idx,key',[(0,'fusion_checkpoint_registry_hash'),(0,'aligned_view_set_hash'),(0,'integrity_receipt_hash'),(1,'registry_hash')])
def test_hash_mutations_fail(load,idx,key):
 a=args(load);a[idx][key]='0'*64
 with pytest.raises(IntegrityError):validate_upstream(*a)
def test_authority_widening_fails(load):
 a=args(load);a[0]['authority']['send_order']=True
 with pytest.raises(IntegrityError):validate_upstream(*a)
