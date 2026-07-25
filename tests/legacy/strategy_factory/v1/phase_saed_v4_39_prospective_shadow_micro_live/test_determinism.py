import copy,random,pytest
from saed_v4_prospective_shadow_micro_live import run_reference
from saed_v4_prospective_shadow_micro_live.canonical import canonical_bytes,content_hash,stable_id,merkle_root

def test_canonical_order():assert canonical_bytes({"b":2,"a":1})==canonical_bytes({"a":1,"b":2})
def test_hash_repeat():assert content_hash({"x":[1,2]})==content_hash({"x":[1,2]})
def test_stable_id():assert stable_id("x",{"a":1}).startswith("x_")
def test_merkle_order_independent():assert merkle_root(["a"*64,"b"*64])==merkle_root(["b"*64,"a"*64])
@pytest.mark.parametrize("i",range(30))
def test_repeat(fixture,output,i):assert run_reference(copy.deepcopy(fixture))==output
@pytest.mark.parametrize("seed",range(20))
def test_reorder_closed_sets(fixture,seed):
 a=copy.deepcopy(fixture);b=copy.deepcopy(fixture);r=random.Random(seed);r.shuffle(a["external_evidence"]);r.shuffle(a["reviews"]);assert run_reference(a)==run_reference(b)
