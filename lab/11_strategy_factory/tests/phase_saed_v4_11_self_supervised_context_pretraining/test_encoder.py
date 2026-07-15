import copy,pytest
from saed_v4_self_supervised_pretraining.encoder import ReferenceEmbeddingEncoder,checkpoint_payload,encoder_from_checkpoint,cosine
from saed_v4_self_supervised_pretraining.errors import CheckpointError

def test_initialization_deterministic():
 a=ReferenceEmbeddingEncoder(['a','b'],8,1);b=ReferenceEmbeddingEncoder(['a','b'],8,1);assert a.state_hash()==b.state_hash()
def test_encode_unit_norm():
 e=ReferenceEmbeddingEncoder(['a','b'],8,1);v=e.encode(['a','b']);assert abs(sum(x*x for x in v)-1)<1e-9
def test_training_changes_state():
 e=ReferenceEmbeddingEncoder(['a','b','c'],8,1);h=e.state_hash();e.train_pair('a','b',['c'],.1,1);assert e.state_hash()!=h
def test_positive_similarity_moves_up():
 e=ReferenceEmbeddingEncoder(['a','b','c'],8,1);before=cosine(e.embeddings['a'],e.embeddings['b']);[e.train_pair('a','b',['c'],.1,1) for _ in range(5)];assert cosine(e.embeddings['a'],e.embeddings['b'])>before
def test_checkpoint_roundtrip():
 e=ReferenceEmbeddingEncoder(['a','b'],8,1);c=checkpoint_payload(e,{'x':1});assert encoder_from_checkpoint(c).state_hash()==e.state_hash()
def test_checkpoint_tamper_rejected():
 e=ReferenceEmbeddingEncoder(['a','b'],8,1);c=checkpoint_payload(e,{});c=copy.deepcopy(c);c['dimension']=9
 with pytest.raises(CheckpointError):encoder_from_checkpoint(c)
