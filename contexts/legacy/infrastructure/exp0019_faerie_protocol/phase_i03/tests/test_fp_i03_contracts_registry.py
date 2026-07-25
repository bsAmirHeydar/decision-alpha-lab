from dataclasses import replace
import pytest
from fp_i03_time.contracts import TimeKernelConfig, canonical_registry_snapshot, canonical_session_definitions
from fp_i03_time.enums import CalendarSegment
from fp_i03_time.errors import FPI03Error
from fp_i03_time.reason_codes import DEFAULT_TIME_REASON_REGISTRY
from fp_i03_time.registry import DEFAULT_TIME_CONTRACT_REGISTRY, TimeContractDescriptor


def test_session_registry_exact_order_and_values():
    sessions=canonical_session_definitions()
    assert [s.code for s in sessions]==[CalendarSegment.A,CalendarSegment.L,CalendarSegment.N]
    assert [(s.start_second,s.end_second,s.wraps_midnight) for s in sessions]==[(64800,14400,True),(14400,34200,False),(34200,61200,False)]


def test_registry_is_frozen_and_hash_stable():
    a=canonical_registry_snapshot();b=canonical_registry_snapshot()
    assert a.registry_hash==b.registry_hash
    assert a.frozen


def test_time_contract_registry_exact_count_and_no_authority():
    items=DEFAULT_TIME_CONTRACT_REGISTRY.all()
    assert len(items)==11
    assert all(item.authority=="NONE" for item in items)


def test_contract_registry_mutation_rejected():
    with pytest.raises(FPI03Error) as exc:
        DEFAULT_TIME_CONTRACT_REGISTRY.register(TimeContractDescriptor("X","1.0.0","S","P","T"))
    assert exc.value.code=="FP_TRC_REGISTRY_FROZEN"


def test_time_reason_registry_exact_count():
    assert len(DEFAULT_TIME_REASON_REGISTRY.all())==15


def test_timezone_change_rejected():
    with pytest.raises(FPI03Error) as exc:
        replace(TimeKernelConfig(),timezone_name="UTC")
    assert exc.value.code=="FP_TRC_TIMEZONE_UNSUPPORTED"
