from fp_i12_operator import *
def test_no_authority_in_package():
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]/'python/fp_i12_operator';bad=[]
 for p in root.glob('*.py'):
  if p.name in ('constants.py','authority.py'):continue
  found=scan_text(p.read_text());bad.extend(found)
 assert not bad
def test_forbidden_registry_present():assert 'OrderSend' in FORBIDDEN_AUTHORITIES
