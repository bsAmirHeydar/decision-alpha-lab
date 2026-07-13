#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
base=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I05';files=sorted(base.glob('*.mqh'))
expected={'FP_I05_All.mqh','FP_I05_CalendarDaySelector.mqh','FP_I05_Checkpoint.mqh','FP_I05_Contracts.mqh','FP_I05_Enums.mqh','FP_I05_ReferenceEngine.mqh','FP_I05_Registry.mqh','FP_I05_RevisionInvalidation.mqh','FP_I05_WindowStore.mqh'}
if {p.name for p in files}!=expected:errors.append(f'MQL include mismatch: {[p.name for p in files]}')
text='\n'.join(p.read_text(encoding='utf-8') for p in files)
for token in ('FP_I05_WindowDescriptor','FP_I05_PairWindowAggregate','FP_I05_ReferenceLevel','ApplyHunterTouch','ApplyProtectedTouch','ContractCount'):
    if token not in text:errors.append('missing MQL token '+token)
for token in ('OrderSend(','CTrade','PositionOpen','ObjectCreate(','ChartCreate','WebRequest(','SocketCreate'):
    if token in text:errors.append('forbidden MQL authority '+token)
for rel in ('mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I05_ReferenceDiagnostic.mq5','mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I05_ReferenceSelfTest.mq5'):
    path=root/rel
    if not path.is_file():errors.append('missing entrypoint '+rel)
    elif 'FP_I05_All.mqh' not in path.read_text(encoding='utf-8'):errors.append('entrypoint missing aggregate include '+rel)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I05 MQL5 static validation PASS: 9 includes, 2 entrypoints, lifecycle/store symbols present, no drawing/trading/network authority.')
