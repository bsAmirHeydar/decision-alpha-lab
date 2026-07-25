import pytest,math
from saed_v4_sequence_state_space.contracts import CandidateSpec
from saed_v4_sequence_state_space.models import build_model
@pytest.mark.parametrize('architecture',['ema_recurrent','causal_convolution','diagonal_ssm','selective_ssm','local_causal_attention','hybrid_ssm_attention'])
def test_model_deterministic(architecture):
 s=CandidateSpec('x_'+architecture,architecture,7,8,8,True);m1=build_model(s,12);m2=build_model(s,12);x=[[0.01*j for j in range(12)] for _ in range(4)];a,_=m1.batch(x);b,_=m2.batch(x);assert a==b and all(math.isfinite(v) for row in a for v in row)
@pytest.mark.parametrize('architecture',['ema_recurrent','causal_convolution','diagonal_ssm','selective_ssm','local_causal_attention','hybrid_ssm_attention'])
def test_state_width(architecture):
 s=CandidateSpec('y_'+architecture,architecture,9,10,8,True);m=build_model(s,12);o,st=m.batch([[0.0]*12]);assert len(o[0])==10 and st.step_count==1
