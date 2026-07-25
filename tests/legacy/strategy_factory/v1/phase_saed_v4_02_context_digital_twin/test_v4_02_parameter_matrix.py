import copy,pytest,hashlib
from saed_v4_context_twin.compiler import compile_twin
@pytest.mark.parametrize('i',range(80))
def test_identity_matrix(context_spec,seed,i):
 c=copy.deepcopy(context_spec);c['context_id']=f'C{i}';c['artifact_id']=f'A{i}';c['specification_hash']=hashlib.sha256(f'c{i}'.encode()).hexdigest();s=copy.deepcopy(seed);s['context_specification_artifact_id']=c['artifact_id'];s['package_id']=f'S{i}';s['package_hash']=hashlib.sha256(f's{i}'.encode()).hexdigest();a=compile_twin(c,s);b=compile_twin(copy.deepcopy(c),copy.deepcopy(s));assert a.semantic_hash==b.semantic_hash
@pytest.mark.parametrize('value,ok',[(True,True),(False,True),(1,False),('true',False)])
def test_boolean_observable_matrix(context_spec,seed,value,ok):
 from saed_v4_context_twin.observations import ObservationLedger
 from saed_v4_context_twin.models import Observation
 from saed_v4_context_twin.enums import ObservationKind
 m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables);o=Observation(m.twin_id,'context_fresh',value,'2026-01-01T00:00:00Z','2026-01-01T00:00:01Z','a','a'*64,ObservationKind.CANONICAL_FACT,1,1)
 if ok:l.append(o)
 else:
  with pytest.raises(Exception):l.append(o)
