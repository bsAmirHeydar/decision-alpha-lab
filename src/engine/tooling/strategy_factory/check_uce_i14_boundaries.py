#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);PKG=ROOT/'src/engine/packages/strategy_factory_runtime_v3';errors=[]
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
for p in sorted(PKG.glob('*.py')):
 text=p.read_text(encoding='utf-8')
 for token in FORBIDDEN:
  if token in text:errors.append(f'{p.relative_to(ROOT)} forbidden authority/dynamic token {token!r}')
checks={
 'bundle.py':('partial_bundle','feature_order_mismatch','model_input_order_mismatch','artifact_hash_mismatch'),
 'export.py':('onnx_unavailable','approved_native_v1','unsupported_export_format'),
 'parity.py':('decision_mismatch','numerical_tolerance_exceeded','predict_mirror'),
 'generation.py':('GenerationState.VALIDATED','idempotency_key','rollback','QUARANTINED'),
 'host.py':('live_adapter_not_authorized','RuntimeDecision','stale_context'),
 'journal.py':('duplicate_request_conflict','duplicate_occurrence_conflict'),
 'policy_bridge.py':('i13_dependency_hash_mismatch','execute_policy')}
for name,tokens in checks.items():
 text=(PKG/name).read_text(encoding='utf-8')
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I14 boundary guard: PASS')
