from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_mql5_headers_exist():
    base=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Anatomy'
    required=['SF06_AnatomyObservation.mqh','SF06_EventLifecycle.mqh','SF06_EventBuilder.mqh','SF06_GoldenLedger.mqh','Reference/SF06_ReferenceSweepPlugin.mqh']
    assert all((base/x).exists() for x in required)
def test_no_live_authority():
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'mql5').rglob('*') if p.suffix.lower() in {'.mqh','.mq5'})
    for token in ('OrderSend(','OrderCheck(','CTrade '):assert token not in text
def test_no_legacy_in_reference_plugin():
    text=(ROOT/'mql5/Include/AlphaLab/StrategyFactory/Anatomy/Reference/SF06_ReferenceSweepPlugin.mqh').read_text()
    for token in ('NDS','EXP0017','Daye','ICT','Astro'):assert token not in text
def test_pyproject_includes_package():
    assert 'strategy_factory_anatomy*' in (ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text()
