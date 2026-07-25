from dataclasses import replace

import pytest

from strategy_factory_experiments_v3.canonical import canonical_sha256
from strategy_factory_experiments_v3.contracts import (
    CandidateAdmission,
    ExperimentDeclaration,
    ParameterSpec,
    make_trial_identity,
)
from strategy_factory_experiments_v3.enums import AdmissionDecision, ParameterKind
from strategy_factory_experiments_v3.errors import ExperimentError
from strategy_factory_experiments_v3.golden import golden_candidates, golden_declaration


def test_rejected_candidate_requires_blocker():
    with pytest.raises(ExperimentError, match="rejected_candidate_without_blocker"):
        CandidateAdmission("x", "1.0.0", "f", "t", AdmissionDecision.REJECT, "a" * 64)


def test_admitted_candidate_cannot_keep_blocker():
    with pytest.raises(ExperimentError, match="admitted_candidate_with_blocker"):
        CandidateAdmission("x", "1.0.0", "f", "t", AdmissionDecision.ACCEPT, "a" * 64, blockers=("bad",))


def test_search_parameter_must_be_identity_bearing():
    with pytest.raises(ExperimentError, match="non_identity_search_parameter_forbidden"):
        ParameterSpec("alpha", ParameterKind.FLOAT, low=0.0, high=1.0, behavior_changing=False)


def test_hidden_test_role_is_rejected_at_declaration_boundary():
    base = golden_declaration()
    with pytest.raises(ExperimentError, match="hidden_test_role_requested"):
        replace(base, requested_roles=("train", "final_test"))


def test_trial_identity_changes_for_every_behavior_axis():
    declaration = golden_declaration()
    candidate = golden_candidates()[0]
    first = make_trial_identity(
        declaration=declaration,
        candidate=candidate,
        parameter_values={"alpha": 0.01},
        fold_id="wf_00",
        seed=7,
        resource_level=9,
    )
    second = make_trial_identity(
        declaration=declaration,
        candidate=candidate,
        parameter_values={"alpha": 0.02},
        fold_id="wf_00",
        seed=7,
        resource_level=9,
    )
    third = make_trial_identity(
        declaration=declaration,
        candidate=candidate,
        parameter_values={"alpha": 0.01},
        fold_id="wf_00",
        seed=8,
        resource_level=9,
    )
    assert len({first.trial_id, second.trial_id, third.trial_id}) == 3
    assert len({first.identity_hash, second.identity_hash, third.identity_hash}) == 3


def test_candidate_admission_hash_covers_capabilities():
    original = golden_candidates()[0]
    changed = replace(original, capability_flags={"deterministic": False})
    assert original.admission_hash != changed.admission_hash


def test_numeric_parameter_rejects_inverted_bounds():
    with pytest.raises(ExperimentError, match="inverted_parameter_bounds"):
        ParameterSpec("depth", ParameterKind.INTEGER, low=5, high=1)


def test_log_parameter_requires_positive_low():
    with pytest.raises(ExperimentError, match="invalid_log_parameter"):
        ParameterSpec("alpha", ParameterKind.FLOAT, low=0.0, high=1.0, log_scale=True)
