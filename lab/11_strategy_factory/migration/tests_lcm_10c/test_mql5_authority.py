from pathlib import Path
def test_mql5_reference_has_no_broker_calls():
 roots=[Path('mql5/Include/StrategyFactory/LCM/V10C'),Path('mql5/Experts/StrategyFactory/LCM/V10C')];tokens=['OrderSend(','PositionOpen(','Buy(','Sell(']
 for root in roots:
  for p in root.rglob('*'):
   if p.is_file():
    text=p.read_text(errors='ignore');assert not any(t in text for t in tokens)
