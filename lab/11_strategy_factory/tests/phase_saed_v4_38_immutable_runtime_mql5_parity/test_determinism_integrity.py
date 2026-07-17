import copy,random,pytest
from saed_v4_immutable_runtime_mql5_parity import run_reference
from saed_v4_immutable_runtime_mql5_parity.canonical import canonical_bytes,content_hash,stable_id,merkle_root
from saed_v4_immutable_runtime_mql5_parity.compiler import verify_immutable
from saed_v4_immutable_runtime_mql5_parity.integrity import verify_file_manifest,verify_synthetic_signature

def test_canonical_order():assert canonical_bytes({"b":2,"a":1})==canonical_bytes({"a":1,"b":2})
def test_hash_repeat():assert content_hash({"x":[1,2]})==content_hash({"x":[1,2]})
def test_stable_id():assert stable_id("x",{"a":1}).startswith("x_")
def test_merkle_order_independent():assert merkle_root(["a"*64,"b"*64])==merkle_root(["b"*64,"a"*64])
def test_verify_bundle(output):assert verify_immutable(output["runtime_bundle"])
def test_verify_manifest(output):assert verify_file_manifest(output["file_manifest"])
def test_verify_signature(output):assert verify_synthetic_signature(output["synthetic_signature"])
def test_tamper_bundle(output):
 x=copy.deepcopy(output["runtime_bundle"]); x["components"]["model"]="0"*64; assert verify_immutable(x) is False
def test_tamper_manifest(output):
 x=copy.deepcopy(output["file_manifest"]); x["files"][0]["content_hash"]="0"*64; assert verify_file_manifest(x) is False
def test_tamper_signature(output):
 x=copy.deepcopy(output["synthetic_signature"]); x["signature"]="0"*64; assert verify_synthetic_signature(x) is False
@pytest.mark.parametrize("i",range(30))
def test_repeat_replay(fixture,output,i):assert run_reference(copy.deepcopy(fixture))==output
@pytest.mark.parametrize("seed",range(20))
def test_reorder_closed_sets(fixture,seed):
 a=copy.deepcopy(fixture); b=copy.deepcopy(fixture); r=random.Random(seed)
 r.shuffle(a["upstream"]); r.shuffle(a["external_evidence"]); r.shuffle(a["reviews"])
 assert run_reference(a)==run_reference(b)
