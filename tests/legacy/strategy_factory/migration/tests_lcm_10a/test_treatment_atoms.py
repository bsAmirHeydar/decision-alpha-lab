from .conftest import j,jl
def test_atoms_are_observed_not_extracted():
 r=j('inventory/treatment_atom_registry.json');rows=jl('inventory/treatment_atom_registry.jsonl');assert r['record_count']==len(rows)==1109;assert all(x['semantic_status']=='OBSERVED_STATIC_NOT_NORMALIZED' and not x['executable_rule_extracted'] for x in rows)
