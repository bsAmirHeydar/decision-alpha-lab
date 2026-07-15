import pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.validation import validate_candidates
from saed_v4_sequence_state_space.trainer import fit_candidate
from saed_v4_sequence_state_space.errors import BudgetError

def seqs(upstream):return compile_sequences(compile_points(upstream[0],FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])),16)
@pytest.mark.parametrize('idx',range(6))
def test_fit_candidates(upstream,config,idx):
 c=validate_candidates(config[1])[idx];m,w,ck,r=fit_candidate(c,12,seqs(upstream),128);assert ck['core_trainable'] is False and ck['readout_trainable'] is True and r['pair_count']>0 and len(w)==11
def test_budget_fails(upstream,config):
 c=validate_candidates(config[1])[0]
 with pytest.raises(BudgetError):fit_candidate(c,12,seqs(upstream),1)
