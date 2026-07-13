from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'python'/'strategy_factory_promotion_v3'
FORBIDDEN=('OrderSend(', 'CTrade', 'trade.Buy(', 'trade.Sell(', 'PositionOpen(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'WebRequest(')
def test_no_execution_or_network_authority():
    violations=[]
    for path in PACKAGE.glob('*.py'):
        text=path.read_text()
        for token in FORBIDDEN:
            if token in text: violations.append((path.name,token))
    assert not violations
def test_no_final_test_data_access_primitive():
    for name in ('uncertainty.py','multiplicity.py','winner_overfit.py','nulls.py','stress.py','calibration.py','gate.py'):
        text=(PACKAGE/name).read_text(); assert 'load_final_test' not in text and 'read_hidden_test' not in text
def test_gate_is_non_compensatory():
    text=(PACKAGE/'gate.py').read_text(); assert 'scorecard.critical_blockers' in text and 'GateOutcome.REJECT if blockers' in text
def test_complete_universe_is_enforced_by_contract(): assert 'trial_universe_count_mismatch' in (PACKAGE/'contracts.py').read_text()
