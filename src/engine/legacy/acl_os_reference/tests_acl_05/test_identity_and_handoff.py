import copy
from src.engine.tooling.strategy_factory.acl_os.acl_05.canonical import digest_object

def redigest(doc,field): doc[field]=digest_object({k:v for k,v in doc.items() if k!=field}); return doc

def test_material_request_change_changes_batch_id(build,inputs):
    a=build("a"); d=copy.deepcopy(inputs["batch_request"]); d["purpose"] += " Materially revised purpose."; redigest(d,"request_digest"); b=build("b",batch_request=d); assert a["batch_id"]!=b["batch_id"]

def test_environment_change_changes_batch_id(build,inputs):
    a=build("a"); d=copy.deepcopy(inputs["environment_lock"]); d["platform"]="OTHER_REFERENCE_PLATFORM"; redigest(d,"environment_digest"); b=build("b",environment_lock=d); assert a["batch_id"]!=b["batch_id"]

def test_budget_change_changes_batch_id(build,inputs):
    a=build("a"); d=copy.deepcopy(inputs["compute_budget"]); d["max_tasks"]+=1; redigest(d,"budget_digest"); b=build("b",compute_budget=d); assert a["batch_id"]!=b["batch_id"]

def test_handoff_binds_all_materials(build):
    r=build(); h=r["handoff"]; fields=["candidate_freeze_digest","search_space_freeze_digest","dataset_snapshot_set_digest","label_contract_set_digest","split_digest","environment_digest","budget_digest","object_index_digest","event_ledger_digest","provenance_graph_digest"]; assert all(str(h[x]).startswith("sha256:") for x in fields)

def test_handoff_required_actions_exact(build):
    r=build(); assert r["handoff"]["required_acl06_actions"]==["PLAN_RESEARCH_DAG","REGISTER_TASK_CONTRACTS","EXECUTE_BOUNDED_RESEARCH"]

def test_handoff_forbids_alpha_inference(build):
    r=build(); assert "INFER_ALPHA_FROM_FREEZE" in r["handoff"]["forbidden_acl06_actions"]

def test_provenance_reaches_acl03(build):
    r=build(); assert r["provenance"]["reaches_acl03"] and any(n["node_id"]=="ACL03_HANDOFF" for n in r["provenance"]["nodes"])

def test_search_space_is_closed(build):
    r=build(); assert r["search_freeze"]["frozen"] and not r["search_freeze"]["new_candidate_generation_allowed"]
