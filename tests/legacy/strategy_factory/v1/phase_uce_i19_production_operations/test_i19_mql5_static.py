from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Operations'
EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'


def test_mql5_operations_surface_exists():
    assert len(list(INC.glob('*.mqh')))>=15
    assert len(list(EXP.glob('EXP_UCE_I19_*.mq5')))>=4


def test_mql5_reference_has_no_order_authority():
    catalog=(INC/'OperationsCatalog.mqh').read_text()
    assert 'AL_OPERATIONS_ORDER_AUTHORITY false' in catalog
    assert 'AL_OPERATIONS_BROKER_AUTHORITY false' in catalog
    assert 'AL_OPERATIONS_NETWORK_AUTHORITY false' in catalog


def test_diagnostics_do_not_call_order_apis():
    forbidden=('OrderSend(','CTrade','trade.Buy','trade.Sell','WebRequest(')
    for path in EXP.glob('EXP_UCE_I19_*.mq5'):
        text=path.read_text()
        assert not any(token in text for token in forbidden)
