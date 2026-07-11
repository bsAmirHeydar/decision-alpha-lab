from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
errors=[]
headers=list((root/'mql5/Include/AlphaLab/StrategyFactory/Inference').glob('*.mqh'))
experts=list((root/'mql5/Experts/StrategyFactory').glob('SF15_*.mq5'))+list((root/'mql5/Experts/StrategyFactoryTests').glob('SF15_*.mq5'))
for p in headers+experts:
    text=p.read_text(encoding='utf-8')
    if 'LongToString' in text:
        errors.append(f'{p}: unsupported LongToString')
    for token in ('Order'+'Send(','Order'+'Check(','C'+'Trade','Position'+'Open('):
        if token in text:
            errors.append(f'{p}: forbidden Phase 15 capital-authority token {token}')
for p in (root/'lab/11_strategy_factory/python/strategy_factory_inference').glob('*.py'):
    text=p.read_text(encoding='utf-8')
    for token in ('MetaTrader5','live_'+'order','paper_'+'order'):
        if token in text:
            errors.append(f'{p}: forbidden execution token {token}')
if not any('OnnxRun(' in p.read_text(encoding='utf-8') for p in headers):
    errors.append('missing MQL5 OnnxRun integration')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'SF15 boundary guard: PASS ({len(headers)} headers, {len(experts)} experts)')
