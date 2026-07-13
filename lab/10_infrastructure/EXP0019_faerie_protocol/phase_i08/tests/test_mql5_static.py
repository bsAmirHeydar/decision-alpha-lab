from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
def test_i08_mql5_files_present_and_no_execution_authority():
 inc=ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I08';files=list(inc.glob('*.mqh'));assert len(files)>=10
 text='\n'.join(p.read_text(errors='ignore') for p in files)
 for token in ('OrderSend(','CTrade','PositionOpen(','WebRequest(','ObjectCreate('): assert token not in text
 assert 'FP_I08_ResolveActiveStack' in text and 'FP_I08_EvaluateDirectionGate' in text
