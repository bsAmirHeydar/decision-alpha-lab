import copy
import pytest
from saed_v4_conformal_ood_selective_control.budget import ResearchLedger
from saed_v4_conformal_ood_selective_control.contracts import CalibrationDatasetContract, ResearchBudget, UpstreamIntakeContract
from saed_v4_conformal_ood_selective_control.dataset import by_role, validate
from saed_v4_conformal_ood_selective_control.errors import DatasetError, UpstreamError
from saed_v4_conformal_ood_selective_control.upstream import verify

def ledger(config): return ResearchLedger(ResearchBudget.from_mapping(config['research_budget']))
def test_valid_dataset(config, records): assert validate(records, CalibrationDatasetContract.from_mapping(config['calibration_dataset_contract']), ledger(config))['record_count'] == 180
def test_role_counts(records): assert {key: len(value) for key, value in by_role(records).items()} == {'calibration': 90, 'drift_reference': 30, 'selection_validation': 60}
def test_valid_upstream(config, upstream): assert verify(UpstreamIntakeContract.from_mapping(config['upstream_intake']), upstream)['scope_verified']
@pytest.mark.parametrize('field,value', [('future_suffix_accessed', True), ('protected_evidence_accessed', True), ('behavior_probability', 0), ('candidate_action', 'buy')])
def test_bad_record_rejected(config, records, field, value):
    mutated = copy.deepcopy(records); mutated[0][field] = value
    with pytest.raises(DatasetError): validate(mutated, CalibrationDatasetContract.from_mapping(config['calibration_dataset_contract']), ledger(config))
@pytest.mark.parametrize('mutation', range(6))
def test_bad_upstream_rejected(config, upstream, mutation):
    value = copy.deepcopy(upstream)
    if mutation == 0: value['handoff']['phase'] = 'SAED_V4_22'
    elif mutation == 1: value['handoff']['next_phase'] = 'SAED_V4_25'
    elif mutation == 2: value['handoff']['handoff_hash'] = 'bad'
    elif mutation == 3: value['handoff']['authority']['runtime'] = True
    elif mutation == 4: value['handoff']['allowed_next_work'] = []
    else: value['handoff']['research_policy_id'] = 'wrong'
    with pytest.raises(UpstreamError): verify(UpstreamIntakeContract.from_mapping(config['upstream_intake']), value)
