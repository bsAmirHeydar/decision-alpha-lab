from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
def test_required_mql5_files_exist_and_braces_balance():
    files=list((ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07').glob('*.mqh'))+list((ROOT/'mql5/Experts/EXP0019').rglob('*I07*.mq5'))
    assert len(files)>=12
    for p in files:
        t=p.read_text();assert t.count('{')==t.count('}'),p
def test_all_header_composition_exists(): assert (ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07/FP_I07_All.mqh').exists()
