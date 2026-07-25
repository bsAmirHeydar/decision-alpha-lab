def test_mql5_mirror_has_no_trade_calls(root):
 d=root/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_10';text='\n'.join(p.read_text(errors='ignore') for p in d.glob('*.mqh'));forbidden=['OrderSend(','CTrade','PositionOpen(','Buy(','Sell('];assert not any(x in text for x in forbidden);assert 'SAEDV410' in text
