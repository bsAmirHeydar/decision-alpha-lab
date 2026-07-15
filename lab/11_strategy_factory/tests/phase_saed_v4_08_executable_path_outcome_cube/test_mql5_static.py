from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_mql5_mirror_is_diagnostic_only():
 files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4OutcomeCube').glob('*.mqh'));assert len(files)>=12
 text='\n'.join(p.read_text() for p in files);assert 'OrderSend' not in text;assert 'WebRequest' not in text;assert 'PRODUCTION_AUTHORIZATION false' in text
