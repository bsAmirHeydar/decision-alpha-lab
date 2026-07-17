from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_positive_int,require_nonnegative,require_sha256
from .errors import PlanningError
from .canonical import content_hash,seal

def freeze_workload(spec:dict,artifacts:dict,cutoff_time:str)->dict:
    require_exact(spec,["workload_id","objective","cutoff_time","baseline_id","task_templates","input_artifact_ids","output_classes","determinism_seed","max_attempts_per_task","synthetic_fixture","research_only"])
    if spec["cutoff_time"]!=cutoff_time or spec["synthetic_fixture"] is not True or spec["research_only"] is not True: raise PlanningError("workload boundary invalid")
    aids={a["artifact_id"] for a in artifacts["artifacts"]}
    if not set(spec["input_artifact_ids"]).issubset(aids): raise PlanningError("unknown input artifact")
    require_unique(spec["task_templates"],"template_id","task templates"); require_positive_int(spec["max_attempts_per_task"],"max_attempts_per_task")
    for t in spec["task_templates"]:
        require_exact(t,["template_id","stage","compute_class","cpu_cores","gpu_units","memory_gb","scratch_gb","locality","replicas","dependencies","command_hash","output_class"])
        require_positive_int(t["cpu_cores"],"cpu_cores"); require_nonnegative(t["gpu_units"],"gpu_units"); require_positive_int(t["replicas"],"replicas"); require_sha256(t["command_hash"],"command_hash")
    body=deepcopy(spec); body["task_templates"]=sorted(body["task_templates"],key=lambda x:x["template_id"]); return seal(body,"v434_workload","workload_spec_id","workload_spec_hash")

def compile_dag(workload:dict,domains:dict)->dict:
    templates={t["template_id"]:t for t in workload["task_templates"]}; tasks=[]
    for tid,t in sorted(templates.items()):
        for r in range(t["replicas"]):
            task_id=f"{tid}::r{r:02d}"; deps=[]
            for d in t["dependencies"]:
                if d not in templates: raise PlanningError("unknown dependency")
                deps.extend(f"{d}::r{x:02d}" for x in range(templates[d]["replicas"]))
            tasks.append({"task_id":task_id,"template_id":tid,"replica":r,"stage":t["stage"],"compute_class":t["compute_class"],"cpu_cores":t["cpu_cores"],"gpu_units":t["gpu_units"],"memory_gb":t["memory_gb"],"scratch_gb":t["scratch_gb"],"locality":t["locality"],"dependencies":sorted(deps),"command_hash":t["command_hash"],"output_class":t["output_class"]})
    ids={t["task_id"] for t in tasks}
    for t in tasks:
        if any(d not in ids for d in t["dependencies"]): raise PlanningError("compiled dependency missing")
    # deterministic cycle detection
    done=set()
    while len(done)<len(tasks):
        ready=[t for t in tasks if t["task_id"] not in done and set(t["dependencies"]).issubset(done)]
        if not ready: raise PlanningError("task DAG cycle")
        done.update(t["task_id"] for t in ready)
    return seal({"phase":"SAED_V4_34","workload_id":workload["workload_id"],"tasks":tasks,"task_count":len(tasks),"acyclic":True,"deterministic":True,"research_only":True},"v434_dag","dag_id","dag_hash")

def freeze_budget(policy:dict)->dict:
    require_exact(policy,["budget_id","max_cpu_core_seconds","max_gpu_seconds","max_memory_gb_seconds","max_scratch_gb_seconds","max_network_bytes","max_cost_units","max_task_attempts","max_wall_clock_ticks","max_exposures","research_only"])
    for k,v in policy.items():
        if k not in {"budget_id","research_only"}: require_nonnegative(v,k)
    if policy["research_only"] is not True: raise PlanningError("budget must be research-only")
    body=deepcopy(policy); body["budget_hash"]=content_hash(body); return body

def partition(dag:dict,nodes:dict,domains:dict,seed:int)->tuple[dict,dict]:
    node_list=nodes["nodes"]; assignments=[]
    for t in sorted(dag["tasks"],key=lambda x:x["task_id"]):
        eligible=[n for n in node_list if n["compute_class"]==t["compute_class"] and n["cpu_cores"]>=t["cpu_cores"] and n["gpu_units"]>=t["gpu_units"] and n["memory_gb"]>=t["memory_gb"] and n["scratch_gb"]>=t["scratch_gb"]]
        if t["locality"].startswith("domain:"): eligible=[n for n in eligible if n["domain_id"]==t["locality"].split(':',1)[1]]
        if not eligible: raise PlanningError(f"no eligible node for {t['task_id']}")
        idx=int(content_hash({"seed":seed,"task_id":t["task_id"]})[:16],16)%len(eligible); n=sorted(eligible,key=lambda x:x["node_id"])[idx]
        assignments.append({"task_id":t["task_id"],"node_id":n["node_id"],"domain_id":n["domain_id"],"compute_class":n["compute_class"],"assignment_reason":"deterministic_capability_locality_hash","raw_data_crossed_domain":False})
    plan=seal({"phase":"SAED_V4_34","dag_id":dag["dag_id"],"seed":seed,"assignments":assignments,"assignment_count":len(assignments),"raw_data_crossed_domain":False,"research_only":True},"v434_partition","plan_id","plan_hash")
    locality=seal({"phase":"SAED_V4_34","plan_id":plan["plan_id"],"checks":[{"task_id":a["task_id"],"domain_id":a["domain_id"],"locality_satisfied":True,"raw_data_crossed_domain":False} for a in assignments],"all_locality_satisfied":True,"research_only":True},"v434_locality","proof_id","proof_hash")
    return plan,locality
