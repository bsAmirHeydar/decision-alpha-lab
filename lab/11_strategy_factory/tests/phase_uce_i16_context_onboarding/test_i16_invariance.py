from pathlib import Path
import pytest
from strategy_factory_onboarding_v3.invariance import snapshot,compare
from strategy_factory_onboarding_v3.enums import InvarianceStatus
from strategy_factory_onboarding_v3.canonical import canonical_sha256
from strategy_factory_onboarding_v3.contracts import CoreSnapshot

def test_snapshot_repeats():
 a=snapshot(Path('.'));b=snapshot(Path('.'));assert a.snapshot_hash==b.snapshot_hash

def test_equal_snapshots_pass():
 a=snapshot(Path('.'));r=compare(a,a);assert r.status is InvarianceStatus.PASS and not r.changed_core_paths

@pytest.mark.parametrize('path',['lab/11_strategy_factory/python/strategy_factory_contracts_v3/x.py','lab/11_strategy_factory/python/strategy_factory_economics_v3/x.py','lab/11_strategy_factory/python/strategy_factory_runtime_v3/x.py'])
def test_core_change_requires_adr(path):
 h=canonical_sha256('x');a=CoreSnapshot('a','1.0.0',canonical_sha256({}),{},0);b=CoreSnapshot('b','1.0.0',canonical_sha256({path:h}),{path:h},0)
 with pytest.raises(Exception):compare(a,b)

def test_core_change_with_adr_is_reported():
 path='lab/11_strategy_factory/python/strategy_factory_contracts_v3/x.py';h=canonical_sha256('x');a=CoreSnapshot('a','1.0.0',canonical_sha256({}),{},0);b=CoreSnapshot('b','1.0.0',canonical_sha256({path:h}),{path:h},0)
 r=compare(a,b,(), 'ADR-016',canonical_sha256('review'));assert r.status is InvarianceStatus.ADR_REQUIRED and path in r.changed_core_paths
