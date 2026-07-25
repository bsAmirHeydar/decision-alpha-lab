#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);PKG=ROOT/'src/engine/packages/strategy_factory_tournament_v3';errors=[]
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
for p in sorted(PKG.glob('*.py')):
 text=p.read_text(encoding='utf-8')
 for token in FORBIDDEN:
  if token in text:errors.append(f'{p.relative_to(ROOT)} forbidden token {token!r}')
checks={
 'inventory.py':('fixture_not_real_data','future_suffix_invariant','causal_cut'),
 'contexts.py':('exploitation_leakage_feature','adapt_exp0017','adapt_hook_zone','causal_replay'),
 'treatments.py':('tight_convex','partial_plus_runner','capital_policy'),
 'algorithms.py':('manual','treatment_choice','deep_multiview'),
 'tournament.py':('declared_trial_count','trial_completed','budget_exhausted'),
 'prospective.py':('duplicate_decision_hash','not_prospective_paper_data','prospective_window_incomplete'),
 'decision.py':('tournament_not_reference_only','paper_mode_prospective','promotion_bundle_missing')}
for name,tokens in checks.items():
 text=(PKG/name).read_text(encoding='utf-8')
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I15 boundary guard: PASS')
