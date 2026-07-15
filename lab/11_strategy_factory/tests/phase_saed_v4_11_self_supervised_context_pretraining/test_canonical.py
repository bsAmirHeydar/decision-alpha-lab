import pytest
from saed_v4_self_supervised_pretraining.canonical import canonical_json,content_hash,stable_id,merkle_root,hash_unit

def test_canonical_order_independent():assert canonical_json({'b':2,'a':1})==canonical_json({'a':1,'b':2})
def test_hash_stable():assert content_hash({'a':[1,2]})==content_hash({'a':[1,2]})
def test_stable_id_prefix():assert stable_id('x',{'a':1}).startswith('x_')
def test_empty_merkle_is_sha256():assert len(merkle_root([]))==64
def test_hash_unit_range():assert 0<=hash_unit('seed')<=1
@pytest.mark.parametrize('v',[float('inf'),float('-inf'),float('nan')])
def test_nonfinite_rejected(v):
 with pytest.raises(ValueError):canonical_json({'x':v})
