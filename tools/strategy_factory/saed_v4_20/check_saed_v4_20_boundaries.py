from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
base=ROOT/'lab/11_strategy_factory/python/saed_v4_decision_focused_treatment_selection'
forbidden=[r'OrderSend\s*\(',r'CTrade\s+',r'MetaTrader5',r'mt5\.',r'broker_password',r'private_signing_key\s*=']
findings=[]
for f in sorted(base.glob('*.py')):
 if f.name in {'security.py','authority.py'}: continue
 text=f.read_text(encoding='utf-8')
 for pat in forbidden:
  if re.search(pat,text,re.I):findings.append((str(f.relative_to(ROOT)),pat))
assert not findings,findings
print(f'SAED V4-20 boundary guard passed: {len(list(base.glob("*.py")))} Python modules')
