import copy,pytest
from saed_v4_independent_multi_lab_replication.service import run
from saed_v4_independent_multi_lab_replication.upstream import verify_upstream
from saed_v4_independent_multi_lab_replication.errors import IntegrityError

def invoke(i): return run(i["config"],i["upstream"],i["protocol"],i["package"],i["labs"],i["environments"],i["payload"])
def test_exact_replay(inputs): assert invoke(copy.deepcopy(inputs))==invoke(copy.deepcopy(inputs))
@pytest.mark.parametrize("field",["certificate_hash","certificate_id","phase","version","claim_class"])
def test_upstream_certificate_mutation_fails(inputs,field):
 v=copy.deepcopy(inputs["upstream"]); v["certificate"][field]="mutated"
 with pytest.raises(IntegrityError): verify_upstream(v)
@pytest.mark.parametrize("field",["handoff_hash","handoff_id","next_phase","phase"])
def test_upstream_handoff_mutation_fails(inputs,field):
 v=copy.deepcopy(inputs["upstream"]); v["handoff"][field]="mutated"
 with pytest.raises(IntegrityError): verify_upstream(v)
@pytest.mark.parametrize("suffix",[[{"ignored":True,"value":0}],[{"ignored":True,"value":1}],[{"ignored":True,"value":999999}],[],[{"ignored":False,"value":-1}]])
def test_future_suffix_invariance(inputs,suffix):
 base=invoke(copy.deepcopy(inputs)); v=copy.deepcopy(inputs); v["payload"]["future_suffix"]=suffix; changed=invoke(v)
 assert base["results"]==changed["results"] and base["certificate"]==changed["certificate"]
@pytest.mark.parametrize("index",[0,1,2,3,4,5,6,7,8,9])
def test_payload_prefix_mutation_detected(inputs,index):
 v=copy.deepcopy(inputs); v["payload"]["aggregate_reference_rows"][index]["probability"]+=0.01
 # package commitment is deliberately frozen, so semantic outcome changes and exact equality is lost
 changed=invoke(v)
 assert changed["results"]!=invoke(copy.deepcopy(inputs))["results"]
