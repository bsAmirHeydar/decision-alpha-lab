from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
FORBIDDEN=('OrderSend','CTrade','PositionOpen','PositionClose','WebRequest','ObjectCreate(','ChartCreate','FileOpen(')
def test_python_has_no_forbidden_authority():
    for p in (ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i07/python').rglob('*.py'):
        text=p.read_text();assert not any(t in text for t in FORBIDDEN),p
def test_mql5_has_no_order_drawing_network_authority():
    paths=list((ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07').glob('*.mqh'))+list((ROOT/'mql5/Experts/EXP0019').rglob('*I07*.mq5'))
    for p in paths:
        text=p.read_text();assert not any(t in text for t in FORBIDDEN),p
