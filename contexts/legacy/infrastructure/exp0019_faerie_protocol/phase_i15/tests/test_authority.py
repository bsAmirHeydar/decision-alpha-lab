from pathlib import Path
from fp_i15_paper import *
def test_no_live_mql_authority():
 root=Path(__file__).resolve().parents[4]/'mql5';paths=list((root/'Include/AlphaLab/EXP0019/FaerieProtocol/I15').glob('*.mqh'))+list((root/'Experts/EXP0019/FaerieProtocol').glob('*Paper*.mq5'));assert scan_mql5_authority(paths)==()
def test_live_disabled_constants(): assert LIVE_EXECUTION_ENABLED is False and PAPER_RUNTIME_AUTHORITY=='SYNTHETIC_EXECUTION_ONLY'
