from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
headers=list((root/'mql5/Include/AlphaLab/StrategyFactory/Governance').glob('*.mqh'))
for p in headers:
    text=p.read_text(encoding='utf-8')
    if 'LongToString' in text:errors.append(f'{p}: unsupported LongToString')
    for token in ('Order'+'Send(','Order'+'Check(','C'+'Trade','Position'+'Open(','Onnx'+'Run('):
        if token in text:errors.append(f'{p}: forbidden Phase 14 authority token {token}')
for p in (root/'lab/11_strategy_factory/python/strategy_factory_governance').glob('*.py'):
    text=p.read_text(encoding='utf-8')
    for token in ('MetaTrader5','live_'+'order','paper_'+'order','onnxruntime'):
        if token in text:errors.append(f'{p}: forbidden Phase 14 runtime token {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'SF14 boundary guard: PASS ({len(headers)} headers)')
