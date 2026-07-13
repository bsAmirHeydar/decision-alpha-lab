#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
base = root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I06'
files = sorted(base.glob('*.mqh'))
expected = {
    'FP_I06_All.mqh', 'FP_I06_CandidateEngine.mqh', 'FP_I06_Checkpoint.mqh',
    'FP_I06_Contracts.mqh', 'FP_I06_Engine.mqh', 'FP_I06_Enums.mqh',
    'FP_I06_FirstSweepClassifier.mqh', 'FP_I06_HuntAdapter.mqh',
    'FP_I06_Registry.mqh', 'FP_I06_RelationCompiler.mqh',
    'FP_I06_RelationRegistry.mqh', 'FP_I06_RevisionInvalidation.mqh',
}
if {p.name for p in files} != expected:
    errors.append(f'MQL include mismatch: {[p.name for p in files]}')
text = '\n'.join(p.read_text(encoding='utf-8') for p in files)
for token in ('FP_I06_RelationRegistry', 'FP_I06_RelationCompiler', 'FP_I06_HuntAdapter', 'FP_I06_FirstSweepClassifier', 'FP_I06_CandidateEngine', 'SameMinuteHasNoOrder', 'ContractCount'):
    if token not in text:
        errors.append('missing MQL token ' + token)
for token in ('OrderSend(', 'CTrade', 'PositionOpen', 'ObjectCreate(', 'ChartCreate', 'WebRequest(', 'SocketCreate'):
    if token in text:
        errors.append('forbidden MQL authority ' + token)
for rel in (
    'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationDiagnostic.mq5',
    'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I06_RelationSelfTest.mq5',
):
    path = root / rel
    if not path.is_file():
        errors.append('missing entrypoint ' + rel)
    elif 'FP_I06_All.mqh' not in path.read_text(encoding='utf-8'):
        errors.append('entrypoint missing aggregate include ' + rel)
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I06 MQL5 static validation PASS: 12 includes, 2 entrypoints, relation/hunt/candidate symbols present, no drawing/trading/network authority.')
