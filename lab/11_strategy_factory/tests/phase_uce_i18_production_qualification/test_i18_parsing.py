from dataclasses import asdict
import pytest

from strategy_factory_qualification_v3.enums import ReleaseStage
from strategy_factory_qualification_v3.errors import QualificationError
from strategy_factory_qualification_v3.golden import (
    chaos_report,
    compile_evidence,
    differential_report,
    environment,
    policy,
    recovery_report,
    rollback_report,
    security_report,
    soak_report,
    stage_evidence,
)
from strategy_factory_qualification_v3.parsing import (
    parse_chaos,
    parse_compile,
    parse_differential,
    parse_environment,
    parse_policy,
    parse_recovery,
    parse_rollback,
    parse_security,
    parse_soak,
    parse_stage,
)


def test_all_external_contract_parsers_round_trip_golden_objects():
    assert parse_environment(asdict(environment())) == environment()
    assert parse_policy(asdict(policy())) == policy()
    assert parse_compile(asdict(compile_evidence())) == compile_evidence()
    assert parse_differential(asdict(differential_report())) == differential_report()
    assert parse_soak(asdict(soak_report())) == soak_report()
    assert parse_chaos(asdict(chaos_report())) == chaos_report()
    assert parse_recovery(asdict(recovery_report())) == recovery_report()
    assert parse_security(asdict(security_report())) == security_report()
    assert parse_stage(asdict(stage_evidence(ReleaseStage.SHADOW))) == stage_evidence(ReleaseStage.SHADOW)
    assert parse_rollback(asdict(rollback_report())) == rollback_report()


def test_parser_rejects_non_object_payload():
    with pytest.raises(QualificationError):
        parse_environment([])


def test_stage_parser_rejects_unknown_stage():
    payload = asdict(stage_evidence(ReleaseStage.PAPER))
    payload["stage"] = "unknown"
    with pytest.raises(ValueError):
        parse_stage(payload)
