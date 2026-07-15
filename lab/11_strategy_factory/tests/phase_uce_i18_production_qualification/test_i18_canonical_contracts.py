from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.canonical import canonical_json, canonical_sha256
from strategy_factory_qualification_v3.contracts import ArtifactRef, DifferentialCase, EnvironmentFingerprint, ReleaseManifest
from strategy_factory_qualification_v3.enums import ReleaseStage
from strategy_factory_qualification_v3.errors import QualificationError
from strategy_factory_qualification_v3.golden import H, H2, environment


def test_environment_identity_is_deterministic():
    assert environment().fingerprint_hash == environment().fingerprint_hash


def test_canonical_dictionary_order_is_stable():
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})


def test_negative_zero_is_normalized():
    assert canonical_json({"x": -0.0}) == '{"x":0.0}'


def test_non_finite_values_are_rejected():
    with pytest.raises(QualificationError):
        canonical_json({"x": float("nan")})


def test_invalid_hash_is_rejected():
    with pytest.raises(QualificationError):
        replace(environment(), symbol_spec_hash="bad")


def test_artifact_parent_traversal_is_rejected():
    with pytest.raises(QualificationError):
        ArtifactRef("x", "1.0.0", H, "../secret", 1)


def test_differential_case_accepts_exact_hash():
    case = DifferentialCase("x", H, H, 100, 100, 0, 0, 1, 0)
    assert case.passed


def test_differential_case_accepts_tolerance_when_hash_differs():
    case = DifferentialCase("x", H, H2, 1e-9, 1e-9, 1e-8, 1e-8, 1, 0)
    assert case.passed


def test_differential_case_rejects_mismatch_count():
    case = DifferentialCase("x", H, H, 0, 0, 0, 0, 2, 1)
    assert not case.passed
