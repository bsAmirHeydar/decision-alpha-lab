import dataclasses,json,pytest
from strategy_factory_runtime_v3.golden import *
from strategy_factory_runtime_v3.export import *
from strategy_factory_runtime_v3.parity import certify_parity
from strategy_factory_runtime_v3.contracts import *
from strategy_factory_runtime_v3.enums import *
from strategy_factory_runtime_v3.errors import *
from strategy_factory_runtime_v3.native_model import predict,decision
from strategy_factory_runtime_v3.preprocessing import transform

def test_approved_native_export_roundtrip():
    m,p,model,e,data=golden_bundle();loaded=load_approved_native(data);assert loaded.model_hash==model.model_hash;assert e.artifact_hash

def test_corrupt_export_rejected():
    with pytest.raises(RuntimeContractError):load_approved_native(b'{bad')
def test_wrong_export_format_rejected():
    with pytest.raises(RuntimeContractError):load_approved_native(json.dumps({'format':'pickle','schema_version':'1.0.0','model':{}}).encode())
def test_onnx_probe_is_explicit():
    probe=onnx_availability();assert set(probe)=={'onnx','onnxruntime','available'};assert probe['available']==(probe['onnx'] and probe['onnxruntime'])
def test_onnx_export_fails_closed_when_unavailable_or_unregistered():
    model=golden_model()
    with pytest.raises(ExportUnavailableError):export_onnx(model)
def test_parity_certificate_passes_all_required_families():
    m,p,model,e,data=golden_bundle();c=certify_parity(m,p,model,data,golden_vectors(),created_at_ms=0);assert c.status is ParityStatus.PASS;assert {o.vector_id.split(':')[0] for o in c.observations}>={'golden','edge','missing','extreme'}
def test_parity_certificate_is_deterministic_when_time_pinned():
    m,p,model,e,data=golden_bundle();a=certify_parity(m,p,model,data,golden_vectors(),created_at_ms=0);b=certify_parity(m,p,model,data,golden_vectors(),created_at_ms=0);assert a.certificate_hash==b.certificate_hash

def test_expected_decision_mismatch_fails_certificate():
    m,p,model,e,data=golden_bundle();v=(ParityVector('x','golden',{'score':.8,'direction':'long','liquidity':.8,'blocked':False},'no_action'),);c=certify_parity(m,p,model,data,v,created_at_ms=0);assert c.status is ParityStatus.FAIL;assert 'expected_decision_mismatch' in c.observations[0].reasons

def test_tampered_model_export_changes_identity():
    model=golden_model();r1,d1=export_approved_native(model);tampered=dataclasses.replace(model,bias=(1.0,0.0));r2,d2=export_approved_native(tampered);assert r1.artifact_hash!=r2.artifact_hash;assert d1!=d2
@pytest.mark.parametrize('features,expected',[({'score':.8,'direction':'long','liquidity':.8,'blocked':False},'enter_long'),({'score':.8,'direction':'short','liquidity':.8,'blocked':False},'no_action'),({'score':.8,'direction':'long','liquidity':.8,'blocked':True},'no_action')])
def test_native_decision_semantics(features,expected):
    p=golden_preprocessing();m=golden_model(p);assert decision(m,predict(m,transform(p,features)))==expected
