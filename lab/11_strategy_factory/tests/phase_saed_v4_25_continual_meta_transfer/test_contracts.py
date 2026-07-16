from __future__ import annotations

import copy

import pytest

from saed_v4_continual_meta_transfer.contracts import (
    AdaptationContract,
    ContinualCalibrationContract,
    DriftTaxonomyContract,
    ForgettingContract,
    MetaDatasetContract,
    RecalibrationExperimentContract,
    ReplayContract,
    ResearchBudget,
    TransferContract,
    UpstreamIntakeContract,
)
from saed_v4_continual_meta_transfer.errors import ContractError

CASES = [
    ("upstream_intake", UpstreamIntakeContract),
    ("meta_dataset_contract", MetaDatasetContract),
    ("drift_taxonomy_contract", DriftTaxonomyContract),
    ("transfer_contract", TransferContract),
    ("adaptation_contract", AdaptationContract),
    ("continual_calibration_contract", ContinualCalibrationContract),
    ("replay_contract", ReplayContract),
    ("forgetting_contract", ForgettingContract),
    ("recalibration_experiment_contract", RecalibrationExperimentContract),
    ("research_budget", ResearchBudget),
]


@pytest.mark.parametrize("key,contract_type", CASES)
def test_valid_contracts(config, key, contract_type):
    assert contract_type.from_mapping(config[key])


@pytest.mark.parametrize("key,contract_type", CASES)
def test_unknown_fields_rejected(config, key, contract_type):
    value = copy.deepcopy(config[key])
    value["unknown_field"] = "forbidden"
    with pytest.raises(ContractError):
        contract_type.from_mapping(value)


@pytest.mark.parametrize("key,contract_type", CASES)
def test_missing_fields_rejected(config, key, contract_type):
    value = copy.deepcopy(config[key])
    value.pop(next(iter(value)))
    with pytest.raises(ContractError):
        contract_type.from_mapping(value)
