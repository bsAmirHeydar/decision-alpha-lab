#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
base = root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I08'
files = sorted(base.glob('*.mqh'))
errors: list[str] = []
expected = {
    'FP_I08_ActiveStack.mqh', 'FP_I08_All.mqh', 'FP_I08_Checkpoint.mqh',
    'FP_I08_Contracts.mqh', 'FP_I08_DirectionGate.mqh', 'FP_I08_Enums.mqh',
    'FP_I08_Neutralization.mqh', 'FP_I08_Registry.mqh', 'FP_I08_Revision.mqh',
    'FP_I08_Store.mqh', 'FP_I08_WWCompiler.mqh', 'FP_I08_WWConfirmation.mqh',
}
if {p.name for p in files} != expected:
    errors.append(f'MQL include set mismatch: {[p.name for p in files]}')
text = '\n'.join(p.read_text(encoding='utf-8') for p in files)
for token in (
    'FP_I08_ResolveActiveStack', 'FP_I08_EvaluateDirectionGate',
    'FP_I08_ShouldNeutralize', 'NEWEST_ACTIVE_CONFIRMED_WW_WINS'
):
    if token not in text:
        errors.append('missing MQL token ' + token)
for token in (
    'OrderSend(', 'CTrade', 'PositionOpen(', 'ObjectCreate(',
    'ChartCreate(', 'WebRequest(', 'SocketCreate'
):
    if token in text:
        errors.append('forbidden MQL authority ' + token)
for rel in (
    'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I08_WeeklyDiagnostic.mq5',
    'mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I08_WeeklySelfTest.mq5',
):
    path = root / rel
    if not path.is_file():
        errors.append('missing ' + rel)
    elif 'FP_I08_All.mqh' not in path.read_text(encoding='utf-8'):
        errors.append('aggregate include missing ' + rel)
for path in files:
    source = path.read_text(encoding='utf-8')
    if source.count('{') != source.count('}'):
        errors.append('brace mismatch ' + path.name)

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I08 MQL5 static PASS: 12 includes, 2 entrypoints, WW stack/gate/neutralization symbols present, no forbidden authority.')
