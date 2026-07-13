#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];PKG=ROOT/'lab/11_strategy_factory/python/strategy_factory_onboarding_v3';errors=[]
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
for p in sorted(PKG.glob('*.py')):
 text=p.read_text(encoding='utf-8')
 for token in FORBIDDEN:
  if token in text:errors.append(f'{p.relative_to(ROOT)} forbidden token {token!r}')
checks={
 'generator.py':('validate_capabilities','render_files','core_snapshot'),
 'adapters.py':('copy.deepcopy','measure_parity','output_mismatch'),
 'migration.py':('parity_passed','stop_after_unit','unaffected'),
 'tournament_template.py':('prospective_paper','promotion_handoff','final_test_sealed'),
 'invariance.py':('CORE_PREFIXES','ADR_REQUIRED','changed'),
 'capabilities.py':('shared_treatment','shared_economics','order_send','future_data')}
for name,tokens in checks.items():
 text=(PKG/name).read_text(encoding='utf-8')
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I16 boundary guard: PASS')
