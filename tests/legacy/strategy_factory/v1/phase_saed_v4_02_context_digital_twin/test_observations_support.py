import pytest
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.observations import ObservationLedger
from saed_v4_context_twin.models import Observation
from saed_v4_context_twin.enums import ObservationKind,SupportStatus
from saed_v4_context_twin.support import evaluate_support
from saed_v4_context_twin.errors import ContractError,IdentityError
H='a'*64

def obs(twin,oid,value,seq,known='2026-07-13T10:00:00Z',event='2026-07-13T09:59:00Z'):
 return Observation(twin,oid,value,event,known,'art',H,ObservationKind.CANONICAL_FACT,1.0,seq)
def test_append_and_latest(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables);l.append(obs(m.twin_id,'context_fresh',True,1));assert l.latest_by_observable(m.twin_id,'2026-07-13T10:00:01Z')['context_fresh'].value is True
def test_sequence_gap(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
 with pytest.raises(IdentityError):l.append(obs(m.twin_id,'context_fresh',True,2))
def test_value_validation(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
 with pytest.raises(ContractError):l.append(obs(m.twin_id,'volatility_z',9.0,1))
def test_known_before_event(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
 with pytest.raises(ContractError):l.append(obs(m.twin_id,'context_fresh',True,1,'2026-07-13T09:00:00Z','2026-07-13T10:00:00Z'))
def test_supported(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables);l.append(obs(m.twin_id,'context_fresh',True,1));l.append(obs(m.twin_id,'htf_alignment','aligned',2));l.append(obs(m.twin_id,'volatility_z',0.2,3));e=evaluate_support(m.twin_id,m.support_geometry,l.latest_by_observable(m.twin_id,'2026-07-13T10:00:01Z'),'2026-07-13T10:00:01Z');assert e.status==SupportStatus.SUPPORTED and e.coverage==1.0
def test_unknown_required(context_spec,seed):
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables);e=evaluate_support(m.twin_id,m.support_geometry,{},'2026-07-13T10:00:01Z');assert e.status==SupportStatus.UNKNOWN
