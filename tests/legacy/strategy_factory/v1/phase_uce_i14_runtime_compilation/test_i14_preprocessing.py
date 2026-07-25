import math,pytest
from strategy_factory_runtime_v3.golden import golden_preprocessing
from strategy_factory_runtime_v3.preprocessing import transform,f32,preprocessing_trace
from strategy_factory_runtime_v3.contracts import *
from strategy_factory_runtime_v3.enums import *
from strategy_factory_runtime_v3.errors import RuntimeContractError

def test_golden_output_order_and_width():
    p=golden_preprocessing();assert p.output_names==('score','direction==long','direction==short','liquidity','blocked');assert p.output_width==5
def test_numeric_scaling_clipping_and_f32():
    p=golden_preprocessing();x=transform(p,{'score':99,'direction':'long','liquidity':-5,'blocked':False});assert x==(f32(2.0),f32(1),f32(0),f32(0),f32(0))
def test_missing_constant_is_applied():
    p=golden_preprocessing();x=transform(p,{'score':.5,'direction':'long','blocked':False});assert x[3]==f32(.5)
def test_missing_required_rejected():
    p=golden_preprocessing()
    with pytest.raises(RuntimeContractError):transform(p,{'direction':'long','liquidity':.5,'blocked':False})
def test_unknown_feature_rejected():
    p=golden_preprocessing()
    with pytest.raises(RuntimeContractError):transform(p,{'score':.5,'direction':'long','liquidity':.5,'blocked':False,'future':1})
def test_unknown_category_rejected():
    p=golden_preprocessing()
    with pytest.raises(RuntimeContractError):transform(p,{'score':.5,'direction':'flat','liquidity':.5,'blocked':False})
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-float('inf')])
def test_nonfinite_feature_rejected(bad):
    p=golden_preprocessing()
    with pytest.raises(RuntimeContractError):transform(p,{'score':bad,'direction':'long','liquidity':.5,'blocked':False})
@pytest.mark.parametrize('bad',['yes',2,-1,None])
def test_boolean_contract_closed(bad):
    p=golden_preprocessing();features={'score':.5,'direction':'long','liquidity':.5,'blocked':bad}
    if bad is None:assert transform(p,features)[-1]==0.0
    else:
        with pytest.raises(RuntimeContractError):transform(p,features)
def test_identity_contract_hash_changes_on_behavior_change():
    r1=FeatureRule('x',FeatureKind.NUMERIC,scaling=ScalingKind.ZSCORE,mean=0,scale=1)
    r2=FeatureRule('x',FeatureKind.NUMERIC,scaling=ScalingKind.ZSCORE,mean=1,scale=1)
    p1=PreprocessingContract('p','1.0.0',('x',),(r1,));p2=PreprocessingContract('p','1.0.0',('x',),(r2,));assert p1.preprocessing_hash!=p2.preprocessing_hash
def test_trace_binds_hash_order_values_precision():
    p=golden_preprocessing();tr=preprocessing_trace(p,{'score':.5,'direction':'short','liquidity':.5,'blocked':False});assert tr['contract_hash']==p.preprocessing_hash;assert tr['output_order']==list(p.output_names);assert len(tr['values'])==5
