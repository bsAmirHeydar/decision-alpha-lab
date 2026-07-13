#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
base=root/'mql5/Include/FaerieProtocol/EXP0019/Core'
errors=[]
expected={
 'FP_I02_Enums.mqh','FP_I02_ReasonCodes.mqh','FP_I02_Relations.mqh','FP_I02_Hash.mqh','FP_I02_Types.mqh',
 'FP_I02_Config.mqh','FP_I02_Identity.mqh','FP_I02_StateMachines.mqh','FP_I02_Validation.mqh','FP_I02_SelfTest.mqh','FP_I02_All.mqh'
}
actual={p.name for p in base.glob('*.mqh')}
if actual!=expected: errors.append(f'MQL include set mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}')
for path in base.glob('*.mqh'):
    text=path.read_text(encoding='utf-8')
    if '#ifndef ' not in text or '#define ' not in text or '#endif' not in text:
        errors.append(f'include guard missing: {path.relative_to(root)}')
    for token in ('OrderSend','CTrade','PositionOpen','ObjectCreate','WebRequest'):
        if token in text: errors.append(f'forbidden token {token} in {path.relative_to(root)}')
reasons=(base/'FP_I02_ReasonCodes.mqh').read_text(encoding='utf-8')
relations=(base/'FP_I02_Relations.mqh').read_text(encoding='utf-8')
if reasons.count('#define FP_RC_')!=35: errors.append('MQL reason-code count is not 35')
if 'return 35;' not in reasons: errors.append('MQL reason count function mismatch')
if relations.count('case FP_REL_')!=7 or 'return 7;' not in relations: errors.append('MQL relation registry count mismatch')
all_text=(base/'FP_I02_All.mqh').read_text(encoding='utf-8')
for name in expected-{'FP_I02_All.mqh'}:
    if f'#include "{name}"' not in all_text: errors.append(f'All header missing include {name}')
selftest=(base/'FP_I02_SelfTest.mqh').read_text(encoding='utf-8')
for token in ('Q12_BLOCKS_CONSUMPTION','PAIR_ID_ORDER_INVARIANT','PROJECTION_ID_CHANGES','WW_NEUTRALIZATION'):
    if token not in selftest: errors.append(f'self-test missing {token}')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I02 MQL5 static validation PASS: 11 includes, 35 reasons, 7 relations, state/identity tests, no forbidden authority.')
