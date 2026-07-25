import pytest
from saed_v4_data_foundation.integrity import build_integrity_receipt,verify_integrity_receipt
from saed_v4_data_foundation.bundle import build_bundle
from saed_v4_data_foundation.handoff import build_twin_seed
from saed_v4_data_foundation.models import DatasetSnapshot
from saed_v4_data_foundation.enums import DataRole
from saed_v4_data_foundation.errors import IntegrityViolation
H='a'*64
def snap():return DatasetSnapshot('s',('a',),('r',),'2026-01-01T00:00:00Z',None,DataRole.DEVELOPMENT,H,H,1,{})
def test_integrity_receipt(): assert verify_integrity_receipt(build_integrity_receipt(H,{'a':'b'*64}))
def test_tampered_receipt():
 r=build_integrity_receipt(H,{'a':'b'*64}); bad=type(r)(r.receipt_id,r.object_hash,'0'*64,r.status,r.details);assert not verify_integrity_receipt(bad)
def test_bundle_deterministic(): assert build_bundle({'b':H,'a':'b'*64},H,H).bundle_hash==build_bundle({'a':'b'*64,'b':H},H,H).bundle_hash
def test_twin_seed_deterministic(): assert build_twin_seed('ctx',[snap()],{'x':'1'},H,'2026-01-01T00:00:00Z',H).package_hash==build_twin_seed('ctx',[snap()],{'x':'1'},H,'2026-01-01T00:00:00Z',H).package_hash
def test_twin_seed_requires_context():
 with pytest.raises(IntegrityViolation): build_twin_seed('',[snap()],{'x':'1'},H,'2026-01-01T00:00:00Z',H)
def test_twin_seed_requires_snapshot():
 with pytest.raises(IntegrityViolation): build_twin_seed('ctx',[],{'x':'1'},H,'2026-01-01T00:00:00Z',H)
