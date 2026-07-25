import pytest
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.hypotheses import HypothesisLedger
from saed_v4_context_twin.models import HypothesisAssessment
from saed_v4_context_twin.enums import HypothesisStatus
from saed_v4_context_twin.errors import ContractError
H='a'*64

def a(twin,score,weight=1):return HypothesisAssessment(twin,'h_continuation',H,'2026-07-13T10:00:00Z',score,weight,'reviewer','r')
def test_declared(context_spec,seed):
 m=compile_twin(context_spec,seed);assert HypothesisLedger(m.hypotheses).state('h_continuation').status==HypothesisStatus.DECLARED
def test_supported(context_spec,seed):
 m=compile_twin(context_spec,seed);l=HypothesisLedger(m.hypotheses);l.append(a(m.twin_id,1));assert l.state('h_continuation').status==HypothesisStatus.SUPPORTED
def test_rejected(context_spec,seed):
 m=compile_twin(context_spec,seed);l=HypothesisLedger(m.hypotheses);l.append(a(m.twin_id,-1));assert l.state('h_continuation').status==HypothesisStatus.REJECTED
def test_bad_weight(context_spec,seed):
 m=compile_twin(context_spec,seed);l=HypothesisLedger(m.hypotheses)
 with pytest.raises(ContractError):l.append(a(m.twin_id,.5,0))
def test_no_canonical_mutation(context_spec,seed):
 m=compile_twin(context_spec,seed);l=HypothesisLedger(m.hypotheses);l.append(a(m.twin_id,1));assert m.context_ref.context_id=='EXP0017_F2_BULLISH'
