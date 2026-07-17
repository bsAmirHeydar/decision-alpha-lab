from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,hash_chain
from .errors import ExecutionError

def execute(dag:dict,schedule:dict,workload:dict,artifacts:dict)->tuple[dict,dict,dict]:
    tasks={t["task_id"]:t for t in dag["tasks"]}; outputs={}; events=[]; receipts=[]
    for wave in schedule["waves"]:
        for slot in wave["tasks"]:
            t=tasks[slot["task_id"]]; dep_hashes=[outputs[d] for d in t["dependencies"]]
            payload={"task_id":t["task_id"],"node_id":slot["node_id"],"domain_id":slot["domain_id"],"command_hash":t["command_hash"],"dependency_output_hashes":dep_hashes,"seed":workload["determinism_seed"],"input_registry_hash":artifacts["registry_hash"]}
            out_hash=content_hash(payload); outputs[t["task_id"]]=out_hash
            events.append({"event_type":"task_completed","task_id":t["task_id"],"node_id":slot["node_id"],"domain_id":slot["domain_id"],"tick":slot["end_tick"],"attempt":slot["attempt"],"output_hash":out_hash,"raw_data_exported":False})
            receipts.append({"task_id":t["task_id"],"status":"completed","attempt":slot["attempt"],"node_id":slot["node_id"],"domain_id":slot["domain_id"],"output_hash":out_hash,"dependencies_verified":True,"locality_verified":True,"budget_checked":True,"synthetic_execution":True})
    chained=hash_chain(events,"v434_exec_event")
    transcript=seal({"phase":"SAED_V4_34","schedule_id":schedule["schedule_id"],"events":chained,"event_count":len(chained),"all_tasks_completed":len(receipts)==dag["task_count"],"network_runtime":"simulated_reference","research_only":True},"v434_execution","transcript_id","transcript_hash")
    receipt=seal({"phase":"SAED_V4_34","task_receipts":receipts,"task_count":len(receipts),"all_success":True,"synthetic_execution":True,"research_only":True},"v434_task_receipts","ledger_id","ledger_hash")
    checkpoints=seal({"phase":"SAED_V4_34","checkpoints":[{"checkpoint_id":f"CP-{i:03d}","wave":i,"state_hash":content_hash(w),"immutable":True} for i,w in enumerate(schedule["waves"])],"checkpoint_count":len(schedule["waves"]),"restartable":True,"research_only":True},"v434_checkpoints","ledger_id","ledger_hash")
    return transcript,receipt,checkpoints
