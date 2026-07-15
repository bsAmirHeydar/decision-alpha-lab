import pytest
from saed_v4_sequence_state_space.distillation import distill_state,project
from saed_v4_sequence_state_space.errors import DistillationError

def test_distillation():
 d=distill_state('x',10,5);assert len(project(d,(0.1,)*10))==5 and not d['runtime_authority']
@pytest.mark.parametrize('n',[0,1,11])
def test_bad_runtime_dim(n):
 with pytest.raises(DistillationError):distill_state('x',10,n)
