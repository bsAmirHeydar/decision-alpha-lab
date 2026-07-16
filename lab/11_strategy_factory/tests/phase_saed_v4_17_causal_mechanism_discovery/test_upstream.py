import pytest
from saed_v4_causal_mechanism_discovery.validation import validate_upstream
from saed_v4_causal_mechanism_discovery.errors import IntegrityError

def args(load):return [load(p) for p in ['lab/11_strategy_factory/artifacts/saed_v4_16/V4_16_TO_V4_17_HANDOFF.JSON','lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON','lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_CHECKPOINT_REGISTRY.JSON','lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_INTEGRITY_RECEIPT.JSON','lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TAIL_CALIBRATION_REPORT.JSON','lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TIME_CALIBRATION_REPORT.JSON']]
def test_valid_upstream(load):assert validate_upstream(*args(load))['passed']
@pytest.mark.parametrize('idx,key',[(0,'survival_dataset_hash'),(0,'model_checkpoint_registry_hash'),(0,'integrity_receipt_hash'),(0,'tail_calibration_report_hash'),(0,'time_calibration_report_hash'),(1,'dataset_hash'),(2,'registry_hash'),(3,'receipt_hash')])
def test_hash_mutations_fail(load,idx,key):
 a=args(load);a[idx][key]='0'*64
 with pytest.raises(IntegrityError):validate_upstream(*a)
def test_authority_widening_fails(load):
 a=args(load);a[0]['authority']['assert_causality']=True
 with pytest.raises(IntegrityError):validate_upstream(*a)
