from pathlib import Path

def test_mql5_inventory():
    root=Path(__file__).resolve().parents[4]
    p=root/'mql5'/'Include'/'AlphaLab'/'StrategyFactory'/'Statistics'
    required=['SF11_AllStatistics.mqh','SF11_StatisticalSample.mqh','SF11_GroupAccumulator.mqh','SF11_MatchedNullEngine.mqh','SF11_StatisticsHarness.mqh']
    assert all((p/x).exists() for x in required)

def test_no_forbidden_long_to_string():
    root=Path(__file__).resolve().parents[4]
    text='\n'.join(p.read_text(encoding='utf-8') for p in (root/'mql5').rglob('*.mq*'))
    assert 'LongToString' not in text

def test_no_live_authority_in_phase11():
    root=Path(__file__).resolve().parents[4]
    text='\n'.join(p.read_text(encoding='utf-8') for p in (root/'mql5'/'Include'/'AlphaLab'/'StrategyFactory'/'Statistics').glob('*.mqh'))
    forbidden=['Order'+'Send(', 'Order'+'Check(', 'C'+'Trade']
    assert not any(x in text for x in forbidden)
