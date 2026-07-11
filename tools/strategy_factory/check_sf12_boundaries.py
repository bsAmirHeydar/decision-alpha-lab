from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
paths=list((root/'mql5'/'Include'/'AlphaLab'/'StrategyFactory'/'Validation').glob('*.mqh'))
errors=[]
for p in paths:
    text=p.read_text(encoding='utf-8')
    if 'LongToString' in text: errors.append(f'{p}: unsupported LongToString')
    for token in ('Order'+'Send(', 'Order'+'Check(', 'C'+'Trade', 'Position'+'Open('):
        if token in text: errors.append(f'{p}: live authority token {token}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'SF12 boundary guard: PASS ({len(paths)} headers)')
