import copy,pytest
from .helpers import build,graph,handoff
from saed_v4_treatment_dsl.errors import IntegrityError
from saed_v4_treatment_dsl.graph_binding import validate_handoff
@pytest.mark.parametrize('field',['graph_id','graph_hash','evidence_role','known_as_of'])
def test_handoff_identity_mismatch_rejected(field):
 h=handoff();h[field]='tampered'
 with pytest.raises(IntegrityError):validate_handoff(graph(),h)
@pytest.mark.parametrize('field',['mutate_ucee_truth','mutate_graph','generate_treatment','select_treatment','train_model','allocate_risk','activate_runtime','send_order'])
def test_handoff_forbidden_authority_rejected(field):
 h=handoff();h['authority'][field]=True
 with pytest.raises(IntegrityError):validate_handoff(graph(),h)
