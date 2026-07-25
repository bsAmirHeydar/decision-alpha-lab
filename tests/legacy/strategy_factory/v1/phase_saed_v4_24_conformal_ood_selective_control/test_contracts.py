import copy
import pytest
from saed_v4_conformal_ood_selective_control.contracts import *
CASES = [
    ('upstream_intake', UpstreamIntakeContract),
    ('calibration_dataset_contract', CalibrationDatasetContract),
    ('conformal_contract', ConformalContract),
    ('ood_contract', OODContract),
    ('selective_control_contract', SelectiveControlContract),
    ('coverage_risk_contract', CoverageRiskContract),
    ('abstention_contract', AbstentionContract),
    ('drift_contract', DriftContract),
    ('research_budget', ResearchBudget),
]
@pytest.mark.parametrize('key,contract', CASES)
def test_valid_contract(config, key, contract): assert contract.from_mapping(config[key])
@pytest.mark.parametrize('key,contract', CASES)
def test_unknown_field_rejected(config, key, contract):
    value = copy.deepcopy(config[key]); value['unknown_field'] = 1
    with pytest.raises(ContractError): contract.from_mapping(value)
@pytest.mark.parametrize('key,contract', CASES)
def test_missing_field_rejected(config, key, contract):
    value = copy.deepcopy(config[key]); value.pop(next(iter(value)))
    with pytest.raises(ContractError): contract.from_mapping(value)
