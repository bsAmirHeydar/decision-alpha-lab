from fp_i05_reference.registry import CATALOG,registry_hash
from fp_i05_reference.conformance import run_conformance

def test_registry_is_exact_and_unique():
 assert len(CATALOG)==12 and len({x.name for x in CATALOG})==12

def test_registry_has_no_runtime_authority():
 assert {x.authority for x in CATALOG}=={'NONE'}

def test_registry_hash_is_stable():
 assert registry_hash()==registry_hash() and len(registry_hash())==64

def test_conformance_passes():
 r=run_conformance();assert r['passed'] and all(r['checks'].values())
