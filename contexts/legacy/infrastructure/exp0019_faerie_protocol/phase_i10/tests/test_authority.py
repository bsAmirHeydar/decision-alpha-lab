from pathlib import Path
from fp_i10_indicator.authority import scan_mql5_authority

def test_no_forbidden_mql5_authority():
 root=Path(__file__).resolve().parents[4]
 paths=list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I10').glob('*.mqh'))+list((root/'mql5/Indicators/EXP0019').rglob('*.mq5'))
 assert scan_mql5_authority(paths)==()
