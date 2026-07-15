from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_11').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_11').glob('*.mq5'))
assert len(files)>=9
for p in files:
 text=p.read_text(encoding='utf-8')
 assert 'OrderSend(' not in text and 'CTrade' not in text and 'PositionOpen(' not in text
 if p.suffix=='.mqh':assert '#ifndef' in text and '#define' in text and '#endif' in text
assert 'send_order=false' in (ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_11/SAEDV411Authority.mqh').read_text().replace(' ','')
print(f'V4-11 MQL5 static validation passed: {len(files)} files; MetaEditor compile pending_local_windows')
