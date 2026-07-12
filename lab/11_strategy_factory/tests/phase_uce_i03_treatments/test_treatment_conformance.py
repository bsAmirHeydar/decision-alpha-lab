from pathlib import Path
from strategy_factory_treatments_v3 import *
def test_catalog_conformance():
 r=run_catalog_conformance(); assert r.total_atoms==50; assert r.successful_invocations>=80; assert r.deterministic and r.long_short_covered and r.no_authority
def test_no_broker_authority_in_python_package():
 root=Path(__file__).resolve().parents[2]/'python'/'strategy_factory_treatments_v3'; text='\n'.join(p.read_text(encoding='utf-8') for p in root.glob('*.py'))
 for token in ('Order'+'Send(', 'Order'+'Check(', 'C'+'Trade', 'Position'+'Open('): assert token not in text
def test_all_atoms_have_identity_affecting_behavior_parameters():
 c=build_default_catalog()
 for r in c.registries():
  for a in r.all(): assert all(s.identity_affecting for s in a.descriptor.parameter_schema.specs)
