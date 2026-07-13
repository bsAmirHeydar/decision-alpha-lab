import pytest

from fp_i02_kernel.enums import CandidateState, RelationCode, WindowKind
from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.reason_codes import DEFAULT_REASON_REGISTRY
from fp_i02_kernel.registry import ContractDescriptor, DEFAULT_CONTRACT_REGISTRY
from fp_i02_kernel.relations import DEFAULT_RELATION_REGISTRY, RelationDescriptor
from fp_i02_kernel.enums import WindowScope


def test_closed_relation_enum_contains_seven_codes():
    assert tuple(code.value for code in RelationCode) == ("AL", "AN", "LN", "NA", "NL", "NN", "WW")


def test_relation_registry_has_reference_then_check_semantics():
    assert len(DEFAULT_RELATION_REGISTRY.all()) == 7
    for descriptor in DEFAULT_RELATION_REGISTRY.all():
        assert descriptor.code.value[0] == descriptor.reference_kind.value
        assert descriptor.code.value[1] == descriptor.check_kind.value


def test_ww_relation_is_directional_gate_and_not_ww_gated():
    ww = DEFAULT_RELATION_REGISTRY.resolve("WW")
    assert ww.directional_gate is True
    assert ww.ww_gated is False
    assert ww.tradeable is True


def test_unknown_relation_fails_closed():
    with pytest.raises(FPI02Error) as exc:
        DEFAULT_RELATION_REGISTRY.resolve("AX")
    assert exc.value.code == "FP_RC_UNKNOWN_ENUM"


def test_invalid_relation_descriptor_is_rejected():
    with pytest.raises(FPI02Error):
        RelationDescriptor(RelationCode.AL, WindowKind.N, WindowScope.SAME_TRADING_DAY, WindowKind.L, WindowScope.SAME_TRADING_DAY, "L", True, True)


def test_reason_registry_is_closed_and_resolvable():
    assert len(DEFAULT_REASON_REGISTRY.all()) == 35
    assert DEFAULT_REASON_REGISTRY.resolve("FP_RC_QUOTA_POLICY_UNSET").execution_blocking is True
    with pytest.raises(FPI02Error):
        DEFAULT_REASON_REGISTRY.resolve("FREE_TEXT")


def test_contract_registry_is_exact_version_and_frozen():
    assert len(DEFAULT_CONTRACT_REGISTRY.all()) == 16
    assert DEFAULT_CONTRACT_REGISTRY.resolve("FP.ConfirmedSignal@1.0.0").identity_domain == "SEMANTIC"
    with pytest.raises(FPI02Error):
        DEFAULT_CONTRACT_REGISTRY.resolve("FP.ConfirmedSignal@2.0.0")
    with pytest.raises(FPI02Error):
        DEFAULT_CONTRACT_REGISTRY.register(ContractDescriptor("X", "1.0.0", "SEMANTIC", "NONE", "FP-I02", "NONE"))
