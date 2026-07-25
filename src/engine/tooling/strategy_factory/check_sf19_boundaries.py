#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=root/'mql5/Include/AlphaLab/StrategyFactory/Monitoring'
errors=[]
for p in owned.rglob('*'):
    if not p.is_file():continue
    text=p.read_text(encoding='utf-8',errors='ignore')
    for token in ('OrderSend(','OrderCheck(','OrderSendAsync(','CTrade','PositionClose(','WebRequest(','FileOpen('):
        if token in text:errors.append(f'forbidden authority or fast-path token {token}: {p}')
    if 'automatic_mutation_allowed=true' in text or 'automatic_mutation_allowed = true' in text:
        errors.append(f'automatic mutation enabled: {p}')
for p in (root/'src/engine/packages/strategy_factory_monitoring').rglob('*.py'):
    text=p.read_text(encoding='utf-8',errors='ignore')
    for token in ('MetaTrader5','requests.','urllib.request','subprocess.Popen'):
        if token in text:errors.append(f'forbidden online authority {token}: {p}')
required={
 root/'mql5/Include/AlphaLab/StrategyFactory/Monitoring/SF19_TelemetryRing.mqh':'SF19_MAX_TELEMETRY_RECORDS',
 root/'mql5/Include/AlphaLab/StrategyFactory/Monitoring/SF19_LifecycleGovernor.mqh':'automatic_mutation_allowed=false',
 root/'src/engine/packages/strategy_factory_monitoring/models.py':'automatic_mutation_allowed: bool=False'}
for p,token in required.items():
    if not p.is_file() or token not in p.read_text(encoding='utf-8',errors='ignore'):errors.append(f'missing invariant {token}: {p}')
print(f'SF19 boundary guard: errors={len(errors)}')
for e in errors:print('ERROR:',e)
raise SystemExit(1 if errors else 0)
