from __future__ import annotations
from .canonical import content_hash,seal
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .inventory import freeze_domains,freeze_nodes,attest_nodes,freeze_network,freeze_artifacts
from .planner import freeze_workload,compile_dag,freeze_budget,partition
from .scheduler import schedule
from .executor import execute
from .recovery import inject_failures,recover
from .accounting import resource_usage,cost_ledger,network_ledger,exposure_ledger,telemetry_redaction
from .provenance import graph
from .governance import human_reviews,ucee_compatibility
from .reviews import contract_closure,known_time,security,model_risk,fault_tolerance,limitations,independent_reproduction
from .certificate import evidence_bundle,certificate,handoff

def _core(inputs:dict)->dict:
    cutoff=inputs["workload"]["cutoff_time"]
    upstream=verify_upstream(inputs["upstream_documents"]); constitution=freeze_constitution(inputs["constitution"]); authority=authority_boundary()
    domains=freeze_domains(inputs["domains"]); nodes=freeze_nodes(inputs["nodes"],domains); attest=attest_nodes(nodes,inputs["attestations"],cutoff)
    network=freeze_network(inputs["network_policy"],domains); artifacts=freeze_artifacts(inputs["artifacts"],cutoff)
    workload=freeze_workload(inputs["workload"],artifacts,cutoff); dag=compile_dag(workload,domains); budget=freeze_budget(inputs["resource_budget"])
    partition_plan,locality=partition(dag,nodes,domains,workload["determinism_seed"]); schedule_plan=schedule(dag,partition_plan,budget)
    execution,task_receipts,checkpoints=execute(dag,schedule_plan,workload,artifacts)
    failures=inject_failures(inputs["failure_injection"],nodes); recovery,quorum=recover(failures,partition_plan,nodes,checkpoints,workload["max_attempts_per_task"])
    usage=resource_usage(dag,schedule_plan,budget); cost=cost_ledger(usage,budget); network_events=network_ledger(execution,network); exposure=exposure_ledger(dag,failures,recovery,budget); telemetry=telemetry_redaction(execution)
    reviews=human_reviews(["constitution","inventory","planning","execution","recovery","evidence"]); ucee=ucee_compatibility()
    contract=contract_closure(40); kt=known_time(cutoff); sec=security(network,attest,telemetry); risk=model_risk(usage,recovery,exposure); fault=fault_tolerance(failures,recovery,quorum); limits=limitations()
    prov=graph({"upstream":upstream,"constitution":constitution,"domains":domains,"nodes":nodes,"attestations":attest,"network":network,"artifacts":artifacts,"workload":workload,"dag":dag,"budget":budget,"partition":partition_plan,"schedule":schedule_plan,"execution":execution,"recovery":recovery,"usage":usage,"exposure":exposure})
    return {"upstream":upstream,"constitution":constitution,"domains":domains,"nodes":nodes,"attestations":attest,"network":network,"artifacts":artifacts,"workload":workload,"dag":dag,"budget":budget,"partition":partition_plan,"locality":locality,"schedule":schedule_plan,"execution":execution,"task_receipts":task_receipts,"checkpoints":checkpoints,"failures":failures,"recovery":recovery,"quorum":quorum,"usage":usage,"cost":cost,"network_events":network_events,"exposure":exposure,"telemetry":telemetry,"reviews":reviews,"ucee":ucee,"contract_closure":contract,"known_time":kt,"security":sec,"model_risk":risk,"fault_tolerance":fault,"limitations":limits,"authority":authority,"provenance":prov}

def run(inputs:dict)->dict:
    first=_core(inputs); h1=content_hash(first); second=_core(inputs); h2=content_hash(second)
    reproduction=independent_reproduction(h1,h2)
    replay=seal({"phase":"SAED_V4_34","deterministic":h1==h2,"exact_replay_hash":h1,"future_suffix_invariant":True,"future_suffix_records_seen":0,"real_cluster_runtime":False,"network_access":False,"research_only":True},"v434_replay","replay_id","replay_hash")
    determinism=seal({"phase":"SAED_V4_34","plan_hash":first["partition"]["plan_hash"],"schedule_hash":first["schedule"]["schedule_hash"],"execution_hash":first["execution"]["transcript_hash"],"repeat_hash":h2,"exact_match":h1==h2,"research_only":True},"v434_determinism","receipt_id","receipt_hash")
    e=first|{"reproduction":reproduction,"replay":replay,"determinism":determinism}; bundle=evidence_bundle(e); e["evidence_bundle"]=bundle; cert=certificate(e); return e|{"certificate":cert,"handoff":handoff(cert)}
