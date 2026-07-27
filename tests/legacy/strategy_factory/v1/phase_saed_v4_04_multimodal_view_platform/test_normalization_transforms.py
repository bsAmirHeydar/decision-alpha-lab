import pytest,hashlib
from dataclasses import replace
from .helpers import service_and_specs,request,golden_sources
from saed_v4_multimodal_views.models import StaticNormalizer
from saed_v4_multimodal_views.enums import NormalizationKind,TransformKind,FeatureType,MissingnessPolicy
from saed_v4_multimodal_views.normalization import normalize
from saed_v4_multimodal_views.transforms import apply_transform
from saed_v4_multimodal_views.errors import NormalizationError,TransformError
H='a'*64
@pytest.mark.parametrize('kind,spec,expected',[('z',StaticNormalizer(NormalizationKind.STATIC_ZSCORE,10,2,None,None,'stats',H),2.0),('r',StaticNormalizer(NormalizationKind.STATIC_ROBUST,10,5,None,None,'stats',H),.8),('m',StaticNormalizer(NormalizationKind.STATIC_MINMAX,None,None,0,20,'stats',H),.7)])
def test_static_normalizers(kind,spec,expected):assert normalize(14,spec)==pytest.approx(expected)
def test_dynamic_or_unbound_normalizer_forbidden():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');f=replace(price.features[0],normalizer=StaticNormalizer(NormalizationKind.STATIC_ZSCORE,0,1,None,None,None,None));bad=replace(price,features=(f,)+price.features[1:])
 with pytest.raises(NormalizationError):service.build_view(bad,request())
@pytest.mark.parametrize('kind,vals,expected',[(TransformKind.MIDPOINT,[2,4],3),(TransformKind.SPREAD,[2,4],2),(TransformKind.DIFFERENCE,[4,2],2),(TransformKind.RATIO,[4,2],2),(TransformKind.BOOLEAN_AND,[True,True],True),(TransformKind.BOOLEAN_OR,[False,True],True),(TransformKind.CONCAT,['a','b'],'a|b'),(TransformKind.VECTOR,[1,2],[1.0,2.0])])
def test_transforms(kind,vals,expected):assert apply_transform(kind,vals)==expected
def test_ratio_zero_rejected():
 with pytest.raises(TransformError):apply_transform(TransformKind.RATIO,[1,0])
def test_log_return_requires_positive():
 with pytest.raises(TransformError):apply_transform(TransformKind.LOG_RETURN,[1,0])
