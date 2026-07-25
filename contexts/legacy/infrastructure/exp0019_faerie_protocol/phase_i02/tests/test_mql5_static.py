from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT = find_repository_root(__file__)
BASE = ROOT / "mql5/Include/FaerieProtocol/EXP0019/Core"


def test_expected_mql5_contract_files_exist():
    expected = {
        "FP_I02_Enums.mqh", "FP_I02_ReasonCodes.mqh", "FP_I02_Relations.mqh", "FP_I02_Hash.mqh",
        "FP_I02_Types.mqh", "FP_I02_Config.mqh", "FP_I02_Identity.mqh", "FP_I02_StateMachines.mqh",
        "FP_I02_Validation.mqh", "FP_I02_SelfTest.mqh", "FP_I02_All.mqh",
    }
    assert {path.name for path in BASE.glob("*.mqh")} == expected


def test_mql5_registry_counts_match_python_contract():
    reasons = (BASE / "FP_I02_ReasonCodes.mqh").read_text()
    relations = (BASE / "FP_I02_Relations.mqh").read_text()
    assert "return 35;" in reasons
    assert reasons.count("#define FP_RC_") == 35
    assert "return 7;" in relations
    assert relations.count("case FP_REL_") == 7


def test_mql5_phase_has_no_order_broker_chart_or_network_authority():
    forbidden = ("OrderSend", "CTrade", "PositionOpen", "ObjectCreate", "WebRequest", "Socket")
    paths = list(BASE.glob("*.mqh")) + [
        ROOT / "mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I02_ContractKernelSelfTest.mq5",
        ROOT / "mql5/Experts/FaerieProtocol/EXP0019_FP_I02_ContractKernelDiagnostic.mq5",
    ]
    for path in paths:
        text = path.read_text()
        for token in forbidden:
            assert token not in text, (path, token)


def test_selftest_covers_open_quota_decision_and_state_machines():
    text = (BASE / "FP_I02_SelfTest.mqh").read_text()
    for token in (
        "Q12_BLOCKS_CONSUMPTION", "CANDIDATE_TERMINAL", "REFERENCE_LIFECYCLE", "WW_NEUTRALIZATION",
        "PAIR_ID_ORDER_INVARIANT", "PROJECTION_ID_CHANGES",
    ):
        assert token in text
