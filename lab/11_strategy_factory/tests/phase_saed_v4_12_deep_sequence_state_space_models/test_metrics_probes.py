import pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.validation import validate_candidates
from saed_v4_sequence_state_space.trainer import fit_candidate
from saed_v4_sequence_state_space.metrics import evaluate_candidate,truncation_sensitivity
from saed_v4_sequence_state_space.probes import state_probe,stability_probe

def build(upstream,config,idx):
 s=compile_sequences(compile_points(upstream[0],FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])),16);c=validate_candidates(config[1])[idx];m,w,_,_=fit_candidate(c,12,s,128);return s,m,w
@pytest.mark.parametrize('idx',range(6))
def test_metrics(upstream,config,idx):
 s,m,w=build(upstream,config,idx);r=evaluate_candidate(m,w,s);assert r['summary']['validation']['count']>0 and r['summary']['test']['count']>0
@pytest.mark.parametrize('idx',range(6))
def test_probes(upstream,config,idx):
 s,m,w=build(upstream,config,idx);p=state_probe(m,s);q=stability_probe(m,s[0]);t=truncation_sensitivity(m,w,s);assert not p['collapsed'] and q['finite_and_bounded'] and 'report_hash' in t
