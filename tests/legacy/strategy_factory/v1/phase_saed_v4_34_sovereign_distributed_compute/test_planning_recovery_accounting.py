from __future__ import annotations
import copy,pytest
from saed_v4_sovereign_distributed_compute import run
from saed_v4_sovereign_distributed_compute.errors import SAEDV434Error

def test_dag_is_acyclic(inputs): assert run(inputs)["dag"]["acyclic"]
def test_all_tasks_scheduled(inputs):
    r=run(inputs); assert r["schedule"]["scheduled_task_count"]==r["dag"]["task_count"]
def test_all_tasks_receipted(inputs):
    r=run(inputs); assert r["task_receipts"]["task_count"]==r["dag"]["task_count"]
def test_checkpoints_restartable(inputs): assert run(inputs)["checkpoints"]["restartable"]
def test_faults_are_synthetic(inputs): assert run(inputs)["failures"]["synthetic_faults"]
def test_recovery_stays_sovereign(inputs): assert run(inputs)["recovery"]["cross_domain_migration"] is False
def test_resource_checks_complete(inputs): assert all(run(inputs)["usage"]["checks"].values())
def test_cost_reference_only(inputs): assert run(inputs)["cost"]["financial_charge"]=="not_claimed"
def test_telemetry_redaction(inputs): assert run(inputs)["telemetry"]["redaction_passed"]
def test_provenance_complete(inputs): assert run(inputs)["provenance"]["complete"]
def test_ucee_unchanged(inputs): assert run(inputs)["ucee"]["central_engine_mutations"]==0

def test_cycle_fails(inputs):
    x=copy.deepcopy(inputs); x["workload"]["task_templates"][0]["dependencies"]=["T40-CERTIFY"]
    with pytest.raises(SAEDV434Error): run(x)
def test_no_eligible_node_fails(inputs):
    x=copy.deepcopy(inputs); x["workload"]["task_templates"][1]["gpu_units"]=99
    with pytest.raises(SAEDV434Error): run(x)
def test_unknown_failure_node_fails(inputs):
    x=copy.deepcopy(inputs); x["failure_injection"]["failures"][0]["node_id"]="MISSING"
    with pytest.raises(SAEDV434Error): run(x)
def test_raw_artifact_fails(inputs):
    x=copy.deepcopy(inputs); x["artifacts"][0]["contains_raw_rows"]=True
    with pytest.raises(SAEDV434Error): run(x)
