import json
import pytest
from strategy_factory_operations_v3.contracts import EvidenceRef, GateResult
from strategy_factory_operations_v3.enums import DeploymentStage, EvidenceState, GateName
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.evidence import build_operations_evidence_bundle
from strategy_factory_operations_v3.golden import H1, H2, H3, H4, NOW
from strategy_factory_operations_v3.parsing import load_json_object, require_closed_keys


def gate(name=GateName.HEALTH, status=EvidenceState.PASS, reasons=()): return GateResult(name, status, NOW, reasons, (H1,))


def bundle(gates): return build_operations_evidence_bundle("b", "abc", H1, H2, H3, H4, NOW, gates, (EvidenceRef("e", H1, "1.0.0", "evidence/e.json", NOW),), DeploymentStage.MICRO_LIVE, .25, ("external evidence required",))


def test_all_pass_bundle_can_authorize_bounded_stage():
    result = bundle((gate(), gate(GateName.RECONCILIATION)))
    assert result.activation_allowed and result.maximum_risk_units == .25


@pytest.mark.parametrize("state", [EvidenceState.FAIL, EvidenceState.PENDING, EvidenceState.DEGRADED])
def test_non_pass_bundle_does_not_activate(state):
    result = bundle((gate(status=state, reasons=("x",)),))
    assert not result.activation_allowed and result.maximum_risk_units == 0


def test_gate_order_and_evidence_order_are_deterministic():
    a = build_operations_evidence_bundle("b", "abc", H1, H2, H3, H4, NOW, (gate(GateName.RECONCILIATION), gate(GateName.HEALTH)), (EvidenceRef("z", H1, "1", "z", NOW), EvidenceRef("a", H2, "1", "a", NOW)), DeploymentStage.SHADOW, 0)
    assert [x.gate for x in a.gates] == sorted([x.gate for x in a.gates], key=lambda x:x.value)
    assert [x.evidence_id for x in a.evidence_refs] == ["a","z"]


def test_evidence_path_rejects_parent_traversal():
    with pytest.raises(OperationsError): EvidenceRef("e", H1, "1", "../secret", NOW)


def test_load_json_object(tmp_path):
    path=tmp_path/"x.json"; path.write_text('{"a":1}')
    assert load_json_object(path)=={"a":1}


def test_load_json_rejects_array(tmp_path):
    path=tmp_path/"x.json"; path.write_text('[]')
    with pytest.raises(OperationsError, match="json_shape"): load_json_object(path)


def test_load_json_rejects_invalid(tmp_path):
    path=tmp_path/"x.json"; path.write_text('{')
    with pytest.raises(OperationsError, match="json_read"): load_json_object(path)


def test_closed_keys_accepts_exact():
    require_closed_keys({"a":1,"b":2},{"a"},{"b"})


def test_closed_keys_rejects_missing():
    with pytest.raises(OperationsError, match="missing_keys"): require_closed_keys({}, {"a"})


def test_closed_keys_rejects_unknown():
    with pytest.raises(OperationsError, match="unknown_keys"): require_closed_keys({"a":1,"x":2}, {"a"})
