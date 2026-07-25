from __future__ import annotations
import copy,pytest
from saed_v4_sovereign_distributed_compute import run
from saed_v4_sovereign_distributed_compute.errors import SAEDV434Error

MUTATIONS=[
 ("constitution","raw_data_export_allowed",True),("constitution","public_network_egress_allowed",True),("constitution","central_engine_mutation_allowed",True),("constitution","execution_authority_allowed",True),
 ("resource_budget","max_cpu_core_seconds",0),("resource_budget","max_gpu_seconds",0),("resource_budget","max_memory_gb_seconds",0),("resource_budget","max_scratch_gb_seconds",0),("resource_budget","max_network_bytes",0),("resource_budget","max_cost_units",0),("resource_budget","max_task_attempts",0),("resource_budget","max_wall_clock_ticks",0),("resource_budget","max_exposures",0),
]
@pytest.mark.parametrize("section,key,value",MUTATIONS)
def test_policy_mutations_fail(inputs,section,key,value):
    x=copy.deepcopy(inputs); x[section][key]=value
    with pytest.raises(SAEDV434Error): run(x)

@pytest.mark.parametrize("section",["constitution","network_policy","resource_budget","workload"])
def test_unknown_field_fails(inputs,section):
    x=copy.deepcopy(inputs); x[section]["unknown_field"]=1
    with pytest.raises(SAEDV434Error): run(x)

@pytest.mark.parametrize("field",["phase","document_id","document_hash","next_phase","research_only"])
def test_upstream_missing_fails(inputs,field):
    x=copy.deepcopy(inputs); x["upstream_documents"][0].pop(field)
    with pytest.raises(SAEDV434Error): run(x)

@pytest.mark.parametrize("idx",range(6))
def test_node_attestation_mutations_fail(inputs,idx):
    x=copy.deepcopy(inputs); x["attestations"][idx]["attestation_fingerprint"]="0"*64
    with pytest.raises(SAEDV434Error): run(x)

@pytest.mark.parametrize("idx",range(5))
def test_artifact_future_or_mutable_fails(inputs,idx):
    x=copy.deepcopy(inputs); x["artifacts"][idx]["immutable"]=False
    with pytest.raises(SAEDV434Error): run(x)

@pytest.mark.parametrize("idx",range(6))
def test_route_raw_data_fails(inputs,idx):
    x=copy.deepcopy(inputs); x["network_policy"]["allowed_routes"][idx]["raw_data_allowed"]=True
    with pytest.raises(SAEDV434Error): run(x)
