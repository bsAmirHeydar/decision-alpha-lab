from dataclasses import replace

import pytest

from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.golden import golden_bundle, golden_candidate, golden_signal
from fp_i02_kernel.identity import IdentityEnvelope, IdentityLedger, candidate_identity, projection_identity, signal_identity


def test_candidate_and_signal_identity_match_contract_properties():
    candidate = golden_candidate()
    signal = golden_signal()
    assert candidate_identity(candidate).compact_id == candidate.candidate_id
    assert signal_identity(signal).compact_id == signal.signal_id


def test_projection_identity_is_chart_and_style_specific():
    bundle = golden_bundle()
    signal = golden_signal()
    a = projection_identity(signal.signal_id, bundle.projection.config_hash, "SIGNAL_LINE", "CHART-A")
    b = projection_identity(signal.signal_id, bundle.projection.config_hash, "SIGNAL_LINE", "CHART-B")
    c = projection_identity(signal.signal_id, replace(bundle.projection, line_width=2).config_hash, "SIGNAL_LINE", "CHART-A")
    assert len({a.compact_id, b.compact_id, c.compact_id}) == 3


def test_identity_ledger_deduplicates_exact_payload():
    ledger = IdentityLedger()
    env = candidate_identity(golden_candidate())
    assert ledger.register(env) == "REGISTERED"
    assert ledger.register(env) == "DUPLICATE"
    assert ledger.size() == 1


def test_identity_ledger_rejects_conflicting_payload_hash_for_same_id():
    ledger = IdentityLedger()
    env = candidate_identity(golden_candidate())
    ledger.register(env)
    conflict = IdentityEnvelope(env.identity_domain, env.object_type, env.schema_version, env.semantic_hash, env.compact_id, "f" * 64)
    with pytest.raises(FPI02Error) as exc:
        ledger.register(conflict)
    assert exc.value.code == "FP_RC_IDENTITY_CONFLICT"
