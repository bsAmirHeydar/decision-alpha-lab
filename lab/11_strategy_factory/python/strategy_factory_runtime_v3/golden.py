from __future__ import annotations
from .contracts import *
from .enums import *
from .export import export_approved_native
from .bundle import compile_bundle,REQUIRED_ROLES
from .signing import sign_manifest
import hashlib
H=lambda c:c*64
def golden_preprocessing():
    rules=(FeatureRule('score',FeatureKind.NUMERIC,MissingPolicy.ERROR,scaling=ScalingKind.ZSCORE,mean=.5,scale=.25,clip_min=0,clip_max=1),FeatureRule('direction',FeatureKind.CATEGORICAL,categories=('long','short')),FeatureRule('liquidity',FeatureKind.NUMERIC,MissingPolicy.CONSTANT,.5,ScalingKind.MINMAX,minimum=0,maximum=1,clip_min=0,clip_max=1),FeatureRule('blocked',FeatureKind.BOOLEAN,MissingPolicy.ZERO))
    return PreprocessingContract('preprocess.breakout','1.0.0',tuple(r.name for r in rules),rules)
def golden_model(pre=None):
    pre=pre or golden_preprocessing();return NativeModelArtifact('model-alpha','1.2.0',ModelKind.LINEAR_SOFTMAX,pre.output_names,('enter_long','no_action'),((1.0,1.0,-2.0,.2,-5.0),(-1.0,-1.0,2.0,-.2,5.0)),(0.0,0.0))
def golden_components():return tuple(ArtifactRef(f'artifact:{r}','1.0.0',hashlib.sha256(r.encode()).hexdigest(),f'application/{r}',100+i,r) for i,r in enumerate(REQUIRED_ROLES))
def golden_bundle(secret=b'uce-i14-test-secret'):
    pre=golden_preprocessing();model=golden_model(pre);export,data=export_approved_native(model)
    m=compile_bundle(bundle_id='runtime.breakout',version='1.0.0',generation=14,created_at_ms=1000,components=golden_components(),preprocessing=pre,model=model,export=export,policy_graph_hash=H('d'),manual_policy_hash=H('e'),fallback_policy_hash=H('f'),authority_matrix_hash=H('1'),monitoring_policy_hash=H('2'),rollback_bundle_hash=H('3'),allowed_modes=(RuntimeMode.TESTER,RuntimeMode.SHADOW,RuntimeMode.PAPER),signature_key_id='test-key',limitations=('synthetic fixtures do not prove market edge',))
    return sign_manifest(m,secret),pre,model,export,data
def golden_vectors():return (ParityVector('golden:base','golden',{'score':.8,'direction':'long','liquidity':.8,'blocked':False},'enter_long'),ParityVector('edge:blocked','edge',{'score':.9,'direction':'long','liquidity':.9,'blocked':True},'no_action'),ParityVector('edge:short','edge',{'score':.7,'direction':'short','liquidity':.5,'blocked':False},'no_action'),ParityVector('missing:liquidity','missing',{'score':.75,'direction':'long','blocked':False}),ParityVector('extreme:clip','extreme',{'score':99,'direction':'long','liquidity':-3,'blocked':False},'enter_long'))
def golden_request(i=1,mode=RuntimeMode.SHADOW):return RuntimeRequest(f'req:{i}',f'occ:{i}','EURUSD',5000+i,5000+i,{'score':.8,'direction':'long','liquidity':.8,'blocked':False},mode)
