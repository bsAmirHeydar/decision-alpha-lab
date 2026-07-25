import pytest
from strategy_factory_runtime_v3.golden import *
from strategy_factory_runtime_v3.generation import GenerationManager
from strategy_factory_runtime_v3.parity import certify_parity
from strategy_factory_runtime_v3.enums import *
from strategy_factory_runtime_v3.errors import ActivationError

def setup_validated():
    m,p,model,e,data=golden_bundle();c=certify_parity(m,p,model,data,golden_vectors(),created_at_ms=0);g=GenerationManager();g.build(m);g.warm(m.bundle_hash);g.validate(m.bundle_hash,c);return m,c,g

def test_state_machine_build_warm_validate_activate():
    m,c,g=setup_validated();r=g.activate(m.bundle_hash,'key',100);assert r.state is GenerationState.ACTIVE;assert g.active_hash==m.bundle_hash
def test_activation_is_idempotent():
    m,c,g=setup_validated();a=g.activate(m.bundle_hash,'same',100);b=g.activate(m.bundle_hash,'same',200);assert a==b
def test_cannot_activate_before_validation():
    m,*_=golden_bundle();g=GenerationManager();g.build(m)
    with pytest.raises(ActivationError):g.activate(m.bundle_hash,'x')
def test_failed_parity_cannot_validate():
    m,p,model,e,data=golden_bundle();bad=certify_parity(m,p,model,data,(ParityVector('x','golden',{'score':.8,'direction':'long','liquidity':.8,'blocked':False},'no_action'),),created_at_ms=0);g=GenerationManager();g.build(m);g.warm(m.bundle_hash)
    with pytest.raises(ActivationError):g.validate(m.bundle_hash,bad)
def test_activation_retires_previous_generation_and_rollback_restores():
    m,c,g=setup_validated();g.activate(m.bundle_hash,'a',100)
    import dataclasses
    m2=dataclasses.replace(m,bundle_id='runtime.breakout2',generation=15,signature='');from strategy_factory_runtime_v3.signing import sign_manifest;m2=sign_manifest(m2,b'uce-i14-test-secret')
    c2=dataclasses.replace(c,certificate_id='cert2',bundle_hash=m2.bundle_hash);g.build(m2);g.warm(m2.bundle_hash);g.validate(m2.bundle_hash,c2);g.activate(m2.bundle_hash,'b',200);assert g.record(m.bundle_hash).state is GenerationState.RETIRED
    rr=g.rollback(m.bundle_hash,'rollback',300);assert rr.bundle_hash==m.bundle_hash;assert g.active_hash==m.bundle_hash
def test_quarantine_active_reverts_pointer():
    m,c,g=setup_validated();g.activate(m.bundle_hash,'a',100);rec=g.quarantine(m.bundle_hash,'corrupt');assert rec.state is GenerationState.QUARANTINED;assert g.active_hash=='0'*64
@pytest.mark.parametrize('method,args',[('warm',('0'*64,)),('rollback',('0'*64,'x'))])
def test_unknown_generation_rejected(method,args):
    g=GenerationManager()
    with pytest.raises(ActivationError):getattr(g,method)(*args)
