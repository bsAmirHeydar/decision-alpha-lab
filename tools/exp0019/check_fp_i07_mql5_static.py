#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
base = root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07'
files = sorted(base.glob('*.mqh'))
expected = {
    'FP_I07_All.mqh', 'FP_I07_Checkpoint.mqh', 'FP_I07_ConfirmationPredicate.mqh',
    'FP_I07_ConfirmationStore.mqh', 'FP_I07_Contracts.mqh', 'FP_I07_Engine.mqh',
    'FP_I07_Enums.mqh', 'FP_I07_HostCloseClock.mqh', 'FP_I07_LifecycleEngine.mqh',
    'FP_I07_ProjectionEngine.mqh', 'FP_I07_Registry.mqh', 'FP_I07_RevisionInvalidation.mqh',
    'FP_I07_SignalIdentity.mqh', 'FP_I07_TimeframeResolver.mqh',
}
if {p.name for p in files} != expected:
    errors.append(f'MQL include mismatch: {[p.name for p in files]}')
text = '\n'.join(p.read_text(encoding='utf-8') for p in files)
for token in ('FP_I07_ResolveHostTimeframe', 'FP_I07_EvaluateOutcome', 'FP_I07_StateForOutcome', 'FP_I07_ConfirmedEvidenceIsImmutable', 'STRICT_SAME_SESSION_FIRST_ELIGIBLE_CLOSE'):
    if token not in text:
        errors.append('missing MQL token ' + token)
for token in ('OrderSend(', 'CTrade', 'PositionOpen', 'ObjectCreate(', 'ChartCreate', 'WebRequest(', 'SocketCreate'):
    if token in text:
        errors.append('forbidden MQL authority ' + token)
for rel in (
    'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I07_ConfirmationDiagnostic.mq5',
    'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I07_ConfirmationSelfTest.mq5',
):
    path = root / rel
    if not path.is_file():
        errors.append('missing ' + rel)
    elif 'FP_I07_All.mqh' not in path.read_text(encoding='utf-8'):
        errors.append('aggregate include missing ' + rel)
for path in files:
    text = path.read_text(encoding='utf-8')
    if text.count('{') != text.count('}'):
        errors.append('brace mismatch ' + path.name)
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I07 MQL5 static PASS: 14 includes, 2 entrypoints, strict close/deadline/lifecycle symbols present, no forbidden authority.')
