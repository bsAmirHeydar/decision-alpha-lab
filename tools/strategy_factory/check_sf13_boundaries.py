from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();headers=list((root/'mql5/Include/AlphaLab/StrategyFactory/Training').glob('*.mqh'));errors=[]
for p in headers:
    text=p.read_text(encoding='utf-8')
    if 'LongToString' in text:errors.append(f'{p}: unsupported LongToString')
    for token in ('Order'+'Send(','Order'+'Check(','C'+'Trade','Position'+'Open('):
        if token in text:errors.append(f'{p}: live authority token {token}')
for p in (root/'lab/11_strategy_factory/python/strategy_factory_training').glob('*.py'):
    text=p.read_text(encoding='utf-8')
    for token in ('MetaTrader5','OrderSend','live_order','paper_order'):
        if token in text:errors.append(f'{p}: forbidden authority token {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'SF13 boundary guard: PASS ({len(headers)} headers)')
