from fp_i11_visual import *

def test_conformance_all_green(): assert all(run().values())
def test_registry_object_kinds(): assert len(manifest()['object_kinds'])==13
def test_reason_registry_closed(): assert len(manifest()['reason_codes'])>=20
