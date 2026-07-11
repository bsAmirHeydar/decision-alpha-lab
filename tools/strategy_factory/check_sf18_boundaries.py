#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
live=root/'mql5/Include/AlphaLab/StrategyFactory/Live'
errors=[]; send=[]; check=[]
for p in live.rglob('*'):
    if not p.is_file(): continue
    text=p.read_text(encoding='utf-8',errors='ignore')
    if 'OrderSend(' in text: send.append(p.name)
    if 'OrderCheck(' in text: check.append(p.name)
    if 'OrderSendAsync(' in text: errors.append(f'async send forbidden: {p}')
    if 'CTrade' in text: errors.append(f'CTrade wrapper forbidden: {p}')
if send!=['SF18_Mql5BrokerAdapter.mqh']: errors.append(f'OrderSend authority files: {send}')
if check!=['SF18_Mql5BrokerAdapter.mqh']: errors.append(f'OrderCheck authority files: {check}')
host=(root/'mql5/Experts/StrategyFactory/SF18_MicroLiveHost.mq5').read_text(encoding='utf-8')
for required in ('InpEnableMicroLive=false','InpStartWithKillSwitchEngaged=true'):
    if required not in host: errors.append(f'host missing locked default: {required}')
print(f'SF18 boundary guard: errors={len(errors)} send_files={send} check_files={check}')
for e in errors: print('ERROR:',e)
raise SystemExit(1 if errors else 0)
