from .conftest import REPO

def test_mql_reference_boundary_defaults_false_and_has_no_broker_calls():
    root = REPO / "mql5/Include/StrategyFactory/LCM/V10B"
    text = chr(10).join(p.read_text() for p in root.glob("*.mqh"))
    assert "LCM10B_SUBMISSION_DEFAULT false" in text
    assert "Order" + "Send(" not in text
    assert "Position" + "Open(" not in text
