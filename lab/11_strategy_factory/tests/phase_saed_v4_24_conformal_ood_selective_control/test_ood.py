import copy
import math
import pytest
from saed_v4_conformal_ood_selective_control.budget import ResearchLedger
from saed_v4_conformal_ood_selective_control.contracts import OODContract, ResearchBudget
from saed_v4_conformal_ood_selective_control.dataset import by_role
from saed_v4_conformal_ood_selective_control.ood import evaluate

def test_detector(outputs):
    detector = outputs['ood_detector']; assert detector['calibration_count'] == 90 and len(detector['feature_statistics']) == 6
@pytest.mark.parametrize('index', range(30))
def test_selection_ood_result(outputs, index):
    value = outputs['selection_ood_evaluations'][index]
    assert math.isfinite(value['ood_score']) and 0 < value['ood_pvalue'] <= 1 and isinstance(value['is_ood'], bool)
    assert value['uses_outcome_at_decision'] is False
@pytest.mark.parametrize('shift', [4,6,8,10,12])
def test_extreme_shift_detected(config, records, outputs, shift):
    record = copy.deepcopy(by_role(records)['selection_validation'][0]); record['features']['momentum'] += shift; record['features']['spread_z'] += shift
    contract = OODContract.from_mapping(config['ood_contract'])
    value = evaluate(record, outputs['ood_detector'], contract, by_role(records)['calibration'])
    assert value['is_ood'] and value['ood_pvalue'] <= contract.minimum_pvalue
