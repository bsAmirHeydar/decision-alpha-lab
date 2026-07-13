import dataclasses,pytest
from strategy_factory_runtime_v3.contracts import *
from strategy_factory_runtime_v3.enums import *
from strategy_factory_runtime_v3.errors import RuntimeContractError
from strategy_factory_runtime_v3.golden import *

def test_golden_contract_hashes_are_stable():
    m,p,model,e,data=golden_bundle();assert len(m.bundle_hash)==64;assert p.preprocessing_hash==p.preprocessing_hash;assert model.model_hash==e.model_hash
@pytest.mark.parametrize('bad',[-1,float('nan'),float('inf')])
def test_feature_rule_rejects_invalid_scale_or_finite(bad):
    with pytest.raises((RuntimeContractError,ValueError)):FeatureRule('x',FeatureKind.NUMERIC,scale=bad)
def test_feature_rule_rejects_zero_scale():
    with pytest.raises(RuntimeContractError):FeatureRule('x',FeatureKind.NUMERIC,scale=0)
def test_categorical_requires_categories():
    with pytest.raises(RuntimeContractError):FeatureRule('x',FeatureKind.CATEGORICAL)
def test_categorical_rejects_duplicate_categories():
    with pytest.raises(RuntimeContractError):FeatureRule('x',FeatureKind.CATEGORICAL,categories=('a','a'))
def test_preprocessing_order_must_match_rules():
    r=(FeatureRule('x',FeatureKind.NUMERIC),)
    with pytest.raises(RuntimeContractError):PreprocessingContract('p','1.0.0',('y',),r)
def test_model_shape_validation():
    with pytest.raises(RuntimeContractError):NativeModelArtifact('m','1.0.0',ModelKind.LINEAR_SOFTMAX,('x',),('a','b'),((1.0,),),(0.0,0.0))
def test_scalar_model_requires_one_output():
    with pytest.raises(RuntimeContractError):NativeModelArtifact('m','1.0.0',ModelKind.LINEAR_SCALAR,('x',),('a','b'),((1.0,),(2.0,)),(0.0,0.0))
def test_bundle_generation_must_be_positive():
    m,*_=golden_bundle()
    with pytest.raises(RuntimeContractError):dataclasses.replace(m,generation=0)
def test_bundle_component_roles_unique():
    m,*_=golden_bundle();dupe=m.components+(m.components[0],)
    with pytest.raises(RuntimeContractError):dataclasses.replace(m,components=dupe)
def test_runtime_request_known_time_is_causal():
    with pytest.raises(RuntimeContractError):RuntimeRequest('r','o','EURUSD',2,1,{},RuntimeMode.SHADOW)
def test_runtime_decision_forbids_order_authority():
    with pytest.raises(RuntimeContractError):RuntimeDecision('d','r','o','a'*64,1,RuntimeDisposition.DECIDED,'x',{},0,0,0,(),True,'b'*64)
def test_operational_latency_not_in_decision_identity():
    d=RuntimeDecision('d','r','o','a'*64,1,RuntimeDisposition.DECIDED,'x',{'x':1},0,1,2,(),False,'b'*64)
    assert d.decision_hash==dataclasses.replace(d,completed_at_ms=99,latency_us=999).decision_hash
@pytest.mark.parametrize('severity',['x','fatal',''])
def test_failure_finding_severity_closed(severity):
    with pytest.raises(RuntimeContractError):FailureFinding(FailureCode.KILL_SWITCH,severity,True,'reject')
def test_pass_report_cannot_hide_critical_failure():
    f=FailureFinding(FailureCode.KILL_SWITCH,'critical',True,'reject')
    with pytest.raises(RuntimeContractError):RuntimeFailureReport('r','a'*64,(f,),True,0)
