import copy,pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.contracts import CandidateSpec
from saed_v4_sequence_state_space.models import build_model
from saed_v4_sequence_state_space.snapshot import restart_parity,create_snapshot,restore_snapshot
from saed_v4_sequence_state_space.errors import IntegrityError

def test_restart(upstream):
 seq=compile_sequences(compile_points(upstream[0],FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])),16)[0];m=build_model(CandidateSpec('restart','selective_ssm',17,10,16,True),12);assert restart_parity(m,seq,1)['passed']
def test_snapshot_tamper():
 m=build_model(CandidateSpec('snap','ema_recurrent',17,10,16,True),12);_,st=m.batch([[0.1]*12]);s=create_snapshot(m.candidate_id,st,'seq','point');bad=copy.deepcopy(s);bad['hidden'][0]+=1
 with pytest.raises(IntegrityError):restore_snapshot(bad)
