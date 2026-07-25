#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
base=root/'mql5/Include/FaerieProtocol/EXP0019/Data';files=sorted(base.glob('*.mqh'))
expected={'FP_I04_All.mqh','FP_I04_Backfill.mqh','FP_I04_BarValidation.mqh','FP_I04_Coverage.mqh','FP_I04_Cursor.mqh','FP_I04_Diagnostics.mqh','FP_I04_DuplicateResolver.mqh','FP_I04_Enums.mqh','FP_I04_Revision.mqh','FP_I04_SelfTest.mqh','FP_I04_SymbolPair.mqh','FP_I04_Synchronizer.mqh','FP_I04_Types.mqh'}
if {p.name for p in files}!=expected:errors.append(f'MQL include mismatch: {[p.name for p in files]}')
text='\n'.join(p.read_text(encoding='utf-8') for p in files)
for token in ('FP_I04_M1Bar','FP_I04_AlignedMinute','FP_I04_DataRevision','FP_I04_IncrementalCursor','FP_I04_SynchronizeRange','FP_I04_RunSelfTest'):
    if token not in text:errors.append('missing MQL token '+token)
for token in ('OrderSend(','CTrade','PositionOpen','ObjectCreate(','ChartCreate','WebRequest(','SocketCreate'):
    if token in text:errors.append('forbidden MQL authority '+token)
for rel in ('mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncSelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncDiagnostic.mq5'):
    path=root/rel
    if not path.is_file():errors.append('missing entrypoint '+rel)
    elif 'FP_I04_All.mqh' not in path.read_text(encoding='utf-8'):errors.append('entrypoint missing aggregate include '+rel)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I04 MQL5 static validation PASS: 13 includes, 2 entrypoints, contract/self-test symbols present, no drawing/trading/network authority.')
