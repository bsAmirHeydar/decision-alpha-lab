#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
base=root/'mql5/Include/FaerieProtocol/EXP0019/Time'
expected={
 'FP_I03_Enums.mqh','FP_I03_Types.mqh','FP_I03_Config.mqh','FP_I03_TimeMath.mqh','FP_I03_SessionRegistry.mqh','FP_I03_SessionCalendar.mqh',
 'FP_I03_WeekCalendar.mqh','FP_I03_Identity.mqh','FP_I03_Calendar.mqh','FP_I03_Diagnostics.mqh','FP_I03_SelfTest.mqh','FP_I03_All.mqh'}
actual={p.name for p in base.glob('*.mqh')}
if actual!=expected: errors.append(f'include mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}')
alltext='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in base.glob('*.mqh'))
for token in ('#define FP_I03_A_START 64800','#define FP_I03_A_END 14400','#define FP_I03_L_END 34200','#define FP_I03_N_END 61200','FP-NY-US-DST-2007PLUS@1.0.0','FP-CALENDAR-ALN-WEEK@1.0.0'):
    if token not in alltext: errors.append('missing canonical token '+token)
for token in ('OrderSend','CTrade','PositionOpen','WebRequest','ObjectCreate('):
    if token.lower() in alltext.lower(): errors.append('forbidden MQL authority '+token)
entries=[root/'mql5/Experts/FaerieProtocolTests/EXP0019_FP_I03_TimeCalendarSelfTest.mq5',root/'mql5/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarDiagnostic.mq5']
for path in entries:
    if not path.is_file(): errors.append('missing '+str(path.relative_to(root)))
    elif '<FaerieProtocol/EXP0019/Time/FP_I03_All.mqh>' not in path.read_text(encoding='utf-8'): errors.append('missing composition include '+str(path.relative_to(root)))
if errors: print('\n'.join(errors));raise SystemExit(1)
print('FP-I03 MQL5 static PASS: 12 includes, canonical session/DST/week constants, two entry points, no order/chart/network authority.')
