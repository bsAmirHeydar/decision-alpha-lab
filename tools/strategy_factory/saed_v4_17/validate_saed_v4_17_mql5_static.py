from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];base=ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_17';files=list(base.glob('*.mqh'));expert=ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_17/SAEDV417StaticConformanceExpert.mq5';assert len(files)>=16 and expert.is_file()
for p in files+[expert]:
 t=p.read_text(encoding='utf-8');assert 'OrderSend' not in t and 'trade.Buy' not in t and 'trade.Sell' not in t and 'WebRequest' not in t
assert 'return false' in (base/'SAEDV417AuthorityBoundary.mqh').read_text()
assert 'return false' in (base/'SAEDV417IdentificationGuard.mqh').read_text()
print(f'SAED V4-17 MQL5 static validation passed: {len(files)+1} files; MetaEditor compile remains external')
