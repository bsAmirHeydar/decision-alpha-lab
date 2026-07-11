from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_mql5_headers_exist():
    base=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Anatomy'
    required=['SF06_AnatomyObservation.mqh','SF06_EventLifecycle.mqh','SF06_EventBuilder.mqh','SF06_GoldenLedger.mqh','Reference/SF06_ReferenceSweepPlugin.mqh']
    assert all((base/x).exists() for x in required)
def test_no_live_authority():
    owned_roots = [
        ROOT/'mql5/Include/AlphaLab/StrategyFactory/Anatomy',
        ROOT/'mql5/Experts/StrategyFactory/SF06_StrategyHost.mq5',
        ROOT/'mql5/Experts/StrategyFactory/SF06_ReferenceAnatomyDiagnostic.mq5',
        ROOT/'mql5/Experts/StrategyFactoryTests/SF06_ReferenceAnatomySelfTest.mq5',
    ]
    files = []
    for root in owned_roots:
        if root.is_dir():
            files.extend(p for p in root.rglob('*') if p.suffix.lower() in {'.mqh','.mq5'})
        elif root.exists():
            files.append(root)
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in files)
    for token in ('OrderSend(','OrderCheck(','CTrade '):
        assert token not in text
def test_no_legacy_in_reference_plugin():
    text=(ROOT/'mql5/Include/AlphaLab/StrategyFactory/Anatomy/Reference/SF06_ReferenceSweepPlugin.mqh').read_text()
    for token in ('NDS','EXP0017','Daye','ICT','Astro'):assert token not in text
def test_pyproject_includes_package():
    assert 'strategy_factory_anatomy*' in (ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text()
