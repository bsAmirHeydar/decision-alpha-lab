from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_surface_is_complete_and_authority_free():
    base=ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I06'
    files=sorted(base.glob('*.mqh'))
    assert len(files)==12
    text='\n'.join(p.read_text() for p in files)
    for token in ('FP_I06_RelationRegistry','FP_I06_HuntAdapter','FP_I06_FirstSweepClassifier','FP_I06_CandidateEngine','SameMinuteHasNoOrder','ContractCount'):
        assert token in text
    for token in ('OrderSend(','CTrade','PositionOpen','ObjectCreate(','ChartCreate','WebRequest('):
        assert token not in text
def test_mql5_entrypoints_include_aggregate_header():
    for rel in ('mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationDiagnostic.mq5','mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationSelfTest.mq5'):
        text=(ROOT/rel).read_text();assert 'FP_I06_All.mqh' in text
