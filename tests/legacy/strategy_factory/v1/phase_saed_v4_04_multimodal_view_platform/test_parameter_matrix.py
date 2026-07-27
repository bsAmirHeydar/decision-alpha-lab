import pytest
from .helpers import service_and_specs,request
from saed_v4_multimodal_views.transforms import apply_transform
from saed_v4_multimodal_views.enums import TransformKind
@pytest.mark.parametrize('index',range(30))
def test_spec_hash_repeatability_matrix(index):
 _,specs=service_and_specs();s=specs[index%len(specs)];assert s.semantic_hash==s.semantic_hash and len(s.semantic_hash)==64
@pytest.mark.parametrize('index',range(20))
def test_build_repeatability_matrix(index):
 service,specs=service_and_specs();s=specs[index%len(specs)];a=service.build_view(s,request(rid=str(index)));b=service.build_view(s,request(rid='different'));assert a.view_hash==b.view_hash
@pytest.mark.parametrize('a,b',[(1,2),(2,4),(3,6),(5,10),(10,20),(7,14),(11,22),(13,26),(17,34),(19,38)])
def test_ratio_matrix(a,b):assert apply_transform(TransformKind.RATIO,[b,a])==2
