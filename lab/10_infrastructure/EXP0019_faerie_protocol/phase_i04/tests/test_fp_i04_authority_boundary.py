from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]

def test_phase_python_has_no_trading_or_drawing_authority():
    base=ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python/fp_i04_data'
    forbidden=('OrderSend(','CTrade','PositionOpen','ChartCreate','ObjectCreate(','WebRequest(','socket.')
    text='\n'.join(p.read_text() for p in base.glob('*.py'))
    assert all(token not in text for token in forbidden)

def test_phase_does_not_modify_previous_phase_packages():
    index=ROOT/'releases/history/exp0019/indexes/EXP0019_FP_I04_FILE_INDEX.txt'
    if index.exists():
        paths=index.read_text().splitlines()
        assert not any('/phase_i0'+str(i)+'/' in p for p in paths for i in range(4))
