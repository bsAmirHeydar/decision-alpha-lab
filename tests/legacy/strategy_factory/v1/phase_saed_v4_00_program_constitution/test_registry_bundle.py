import pytest
from saed_v4_constitution.registry import ExactVersionRegistry,RegistryRecord
from saed_v4_constitution.errors import IntegrityViolation
from saed_v4_constitution.bundle import build_evidence_bundle,verify_evidence_bundle,REQUIRED_COMPONENTS

def test_registry_idempotent():
 r=ExactVersionRegistry(); x=RegistryRecord('constitution','c','1','a'*64,'2026-07-13T00:00:00Z','active'); r.register(x); r.register(x); assert r.get('constitution','c','1')==x

def test_registry_immutable():
 r=ExactVersionRegistry(); r.register(RegistryRecord('constitution','c','1','a'*64,'2026-07-13T00:00:00Z','active'))
 with pytest.raises(IntegrityViolation): r.register(RegistryRecord('constitution','c','1','b'*64,'2026-07-13T00:00:00Z','active'))

def comps(): return {k:(["lim"] if k=='limitations' else {'x':k}) for k in REQUIRED_COMPONENTS}

def test_bundle_roundtrip():
 c=comps(); b=build_evidence_bundle('b','2026-07-13T00:00:00Z',c); assert verify_evidence_bundle(b,c)

def test_bundle_tamper_detected():
 c=comps(); b=build_evidence_bundle('b','2026-07-13T00:00:00Z',c); c['constitution']={'x':'tampered'}
 with pytest.raises(IntegrityViolation): verify_evidence_bundle(b,c)

def test_bundle_no_production_claim():
 b=build_evidence_bundle('b','2026-07-13T00:00:00Z',comps()); assert b['production_authorized'] is False and b['actual_external_evidence_attached'] is False
