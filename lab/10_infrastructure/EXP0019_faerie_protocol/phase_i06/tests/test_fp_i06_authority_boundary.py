from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
def test_python_has_no_drawing_trading_network_authority():
    text='\n'.join(p.read_text() for p in (ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i06/python/fp_i06_relations').glob('*.py'))
    for token in ('OrderSend(','CTrade','PositionOpen','ObjectCreate(','ChartCreate','WebRequest(','requests.','socket.'):
        assert token not in text
def test_i06_does_not_own_upstream_phase_files():
    index=ROOT/'EXP0019_FP_I06_FILE_INDEX.txt'
    if index.exists():
        assert not any(f'/phase_i0{i}/' in x for x in index.read_text().splitlines() for i in range(6))
