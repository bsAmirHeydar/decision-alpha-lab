from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__)
MQL=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Context'
def test_mql5_inventory():
    required=['SF07_ContextEngine.mqh','SF07_FeatureRegistry.mqh','SF07_ContextState.mqh','SF07_FeatureVector.mqh','SF07_ContextFrame.mqh','SF07_AllContext.mqh']
    for name in required:assert (MQL/name).exists()
def test_no_live_authority_or_legacy_coupling():
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in MQL.rglob('*.mqh'))
    for token in ['OrderSend(','OrderCheck(','CTrade','EXP0017','Daye']:assert token not in text
def test_no_unsupported_long_to_string():
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in list(MQL.rglob('*.mqh'))+list((ROOT/'mql5/Experts/StrategyFactory').glob('SF07_*.mq5'))+list((ROOT/'mql5/Tests/Experts/StrategyFactory').glob('SF07_*.mq5')))
    assert 'LongToString(' not in text
def test_docs_and_status_exist():
    assert (ROOT/'docs/strategy_factory_implementation/phase07/00_PHASE_07_MOC.md').exists()
    assert (ROOT/'releases/history/strategy_factory/program/implementation/phase_status/PHASE_07.json').exists()
