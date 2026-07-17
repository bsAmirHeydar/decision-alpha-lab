from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4];FILES=sorted(list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_41').glob('*'))+list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_41').glob('*')))
FORBIDDEN=['OrderSend(','CTrade','trade.Buy','trade.Sell','PositionOpen(','PositionClose(','WebRequest(','SocketCreate(']
@pytest.mark.parametrize('path',FILES,ids=lambda p:p.name)
def test_no_order_or_network_api(path):
 s=path.read_text(encoding='utf-8');assert 'SAEDV441' in s
 for token in FORBIDDEN:assert token not in s
def test_mql_count():assert len(FILES)>=32
def test_authority_constants():
 s=(ROOT/'mql5/Include/StrategyFactory/SAED/V4_41/SAEDV441Authority.mqh').read_text();assert 'SAEDV441_LIVE_ORDER_SUBMISSION_ALLOWED 0' in s and 'SAEDV441_CAPITAL_ACTIVATION_ALLOWED 0' in s and 'SAEDV441_PRODUCTION_AUTHORIZED 0' in s and 'SAEDV441_REINSTATEMENT_WITHOUT_REQUALIFICATION_ALLOWED 0' in s
