from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=list((root/'mql5/Include/AlphaLab/StrategyFactory/Candidate').rglob('*.mqh'))+list((root/'mql5/Experts/StrategyFactory').glob('SF08_*.mq5'))+list((root/'mql5/Tests/Experts/StrategyFactory').glob('SF08_*.mq5'))
text='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in owned)
errors=[]
for token in ('OrderSend(','OrderCheck(','CTrade','PositionOpen('):
    if token in text:errors.append('live authority token: '+token)
if 'LongToString(' in text:errors.append('unsupported LongToString')
for p in owned:
    raw=p.read_text(encoding='utf-8',errors='replace')
    if re.search(r'CopyRates\s*\(',raw):errors.append('direct CopyRates in '+str(p.relative_to(root)))
print(f'SF08 boundary guard: errors={len(errors)} files={len(owned)}')
for e in errors:print('ERROR',e)
raise SystemExit(1 if errors else 0)
