from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from saed_v4_continual_meta_transfer import run

ARTIFACT_NAME_MAP = {
    "upstream_receipt": "GOLDEN_UPSTREAM_RECEIPT.JSON",
    "meta_dataset_summary": "GOLDEN_META_DATASET_SUMMARY.JSON",
    "meta_features": "GOLDEN_META_FEATURES.JSON",
    "drift_report": "GOLDEN_DRIFT_REPORT.JSON",
    "transfer_map": "GOLDEN_TRANSFER_MAP.JSON",
    "adaptations": "GOLDEN_ADAPTATIONS.JSON",
    "regularizations": "GOLDEN_REGULARIZATIONS.JSON",
    "transfer_evaluations": "GOLDEN_TRANSFER_EVALUATIONS.JSON",
    "transfer_report": "GOLDEN_TRANSFER_REPORT.JSON",
    "negative_transfer_guards": "GOLDEN_NEGATIVE_TRANSFER_GUARDS.JSON",
    "continual_calibration_states": "GOLDEN_CONTINUAL_CALIBRATION_STATES.JSON",
    "replay_buffer": "GOLDEN_REPLAY_BUFFER.JSON",
    "recalibration_experiment": "GOLDEN_RECALIBRATION_EXPERIMENT.JSON",
    "trial_ledger": "GOLDEN_TRIAL_LEDGER.JSON",
    "exposure_ledger": "GOLDEN_EXPOSURE_LEDGER.JSON",
    "budget_snapshot": "GOLDEN_BUDGET_SNAPSHOT.JSON",
    "authority_boundary": "GOLDEN_AUTHORITY_BOUNDARY.JSON",
    "certificate": "GOLDEN_CONTINUAL_META_TRANSFER_CERTIFICATE.JSON",
    "handoff": "V4_25_TO_V4_26_HANDOFF.JSON",
    "replay_receipt": "GOLDEN_REPLAY_RECEIPT.JSON",
}


def test_service_reproduces_all_golden_outputs(config, upstream, tasks, golden_outputs):
    outputs = run(config, upstream, tasks)
    for key, filename in ARTIFACT_NAME_MAP.items():
        assert outputs[key] == golden_outputs[filename], key


def test_certificate_is_research_only(config, upstream, tasks):
    certificate = run(config, upstream, tasks)["certificate"]
    assert certificate["accepted_for_continual_meta_transfer_research"]
    assert all(certificate["gates"].values())
    assert certificate["research_only"]
    for field in ["decision_authority","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","real_alpha_claim","prospective_success_claim","runtime_parity_claim"]:
        assert certificate[field] is False


def test_handoff_scope_is_exact(config, upstream, tasks):
    handoff = run(config, upstream, tasks)["handoff"]
    assert handoff["next_phase"] == "SAED_V4_26"
    assert set(handoff["allowed_next_work"]) == {
        "frozen_feature_attribution","transfer_pathway_attribution","adaptation_parameter_mechanism_analysis",
        "continual_calibration_component_analysis","counterfactual_mechanism_probes","mechanistic_failure_catalogue",
    }
    assert not any(handoff["authority"].values())


def test_query_outcome_mutation_preserves_decision_time_artifacts(config, upstream, tasks):
    first = run(config, upstream, tasks)
    mutated = copy.deepcopy(tasks)
    mutated[30]["query_targets"] = [value + 500 for value in mutated[30]["query_targets"]]
    second = run(config, upstream, mutated)
    assert first["meta_features"] == second["meta_features"]
    assert first["transfer_map"] == second["transfer_map"]
    assert first["adaptations"] == second["adaptations"]
    assert first["regularizations"] == second["regularizations"]
    assert first["negative_transfer_guards"] != second["negative_transfer_guards"]
