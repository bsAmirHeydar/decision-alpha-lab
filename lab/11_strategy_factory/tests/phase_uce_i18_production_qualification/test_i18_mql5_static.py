from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
INC = ROOT / "mql5/Include/AlphaLab/StrategyFactory/Qualification"
EXP = ROOT / "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics"


def test_mql5_qualification_contract_inventory():
    assert len(list(INC.glob("*.mqh"))) >= 13
    assert len(list(EXP.glob("EXP_UCE_I18_*.mq5"))) >= 3


def test_qualification_catalog_denies_implicit_authority():
    text = (INC / "QualificationCatalog.mqh").read_text()
    assert "#define AL_QUALIFICATION_ORDER_AUTHORITY false" in text
    assert "#define AL_QUALIFICATION_BROKER_AUTHORITY false" in text
    assert "#define AL_QUALIFICATION_NETWORK_AUTHORITY false" in text


def test_reconciliation_guard_is_fail_closed():
    text = (INC / "QualificationReconciliationGuard.mqh").read_text()
    assert "return false" in text and "reserved_hash!=observed_hash" in text


def test_diagnostics_do_not_place_orders():
    for path in EXP.glob("EXP_UCE_I18_*.mq5"):
        text = path.read_text()
        assert "OrderSend(" not in text and "CTrade" not in text
