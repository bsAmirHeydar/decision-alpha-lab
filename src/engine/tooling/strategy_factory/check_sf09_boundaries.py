from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=list((root/'mql5/Include/AlphaLab/StrategyFactory/Outcome').rglob('*.mqh'))+list((root/'mql5/Experts/StrategyFactory').glob('SF09_*.mq5'))+list((root/'mql5/Tests/Experts/StrategyFactory').glob('SF09_*.mq5'))
text='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in owned)
errors=[]
for token in ('OrderSend(','OrderCheck(','CTrade','PositionOpen(','CopyRates(','LongToString('):
    if token in text:errors.append('forbidden Phase 09 token: '+token)
if 'strategy_factory/outcome_record@1.0.0' not in text:errors.append('outcome schema missing')
print(f'SF09 boundary guard: errors={len(errors)} files={len(owned)}')
for e in errors:print('ERROR',e)
raise SystemExit(1 if errors else 0)
