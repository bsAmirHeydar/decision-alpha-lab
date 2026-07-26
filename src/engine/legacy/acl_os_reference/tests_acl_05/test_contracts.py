import copy, json
import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_05.canonical import digest_object
from src.engine.tooling.strategy_factory.acl_os.acl_05.contracts import compile_dataset_snapshot, validate_label_contract, validate_split_contract, validate_environment_lock, validate_compute_budget

def redigest(doc,field): doc[field]=digest_object({k:v for k,v in doc.items() if k!=field}); return doc

def test_dataset_compiles(inputs,fixture_root):
    s,p=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); assert s["known_time_verified"] and len(p)==s["size_bytes"]

def test_dataset_row_count_mismatch_denied(inputs,fixture_root):
    d=copy.deepcopy(inputs["dataset_documents"][0]); d["row_count"]+=1; redigest(d,"snapshot_digest")
    with pytest.raises(Exception): compile_dataset_snapshot(d,fixture_root)

def test_dataset_available_after_cut_denied(inputs,fixture_root):
    d=copy.deepcopy(inputs["dataset_documents"][0]); d["available_through"]="2025-01-01T00:00:00Z"; redigest(d,"snapshot_digest")
    with pytest.raises(Exception): compile_dataset_snapshot(d,fixture_root)

def test_path_escape_denied(inputs,fixture_root):
    d=copy.deepcopy(inputs["dataset_documents"][0]); d["source_path"]="../secret"; redigest(d,"snapshot_digest")
    with pytest.raises(Exception): compile_dataset_snapshot(d,fixture_root)

def test_primary_label_valid(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); assert validate_label_contract(inputs["label_documents"][0],snap)["role"]=="PRIMARY"

def test_primary_future_path_denied(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); d=copy.deepcopy(inputs["label_documents"][0]); d["uses_future_path_diagnostics"]=True; redigest(d,"label_contract_digest")
    with pytest.raises(Exception): validate_label_contract(d,snap)

def test_unmatured_label_denied(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); d=copy.deepcopy(inputs["label_documents"][0]); d["maturity"]["available_after_seconds"]=1; redigest(d,"label_contract_digest")
    with pytest.raises(Exception): validate_label_contract(d,snap)

def test_diagnostic_must_be_segregated(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); d=copy.deepcopy(inputs["label_documents"][1]); d["segregated_from_selection"]=False; redigest(d,"label_contract_digest")
    with pytest.raises(Exception): validate_label_contract(d,snap)

def test_split_valid(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); assert validate_split_contract(inputs["split_contract"],snap)["method"]=="PURGED_WALK_FORWARD"

def test_split_overlap_denied(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); d=copy.deepcopy(inputs["split_contract"]); d["validation"]["start"]="2024-02-01T00:00:00Z"; redigest(d,"split_digest")
    with pytest.raises(Exception): validate_split_contract(d,snap)

def test_non_train_fit_denied(inputs,fixture_root):
    snap,_=compile_dataset_snapshot(inputs["dataset_documents"][0],fixture_root); d=copy.deepcopy(inputs["split_contract"]); d["transform_fit_scope"]="ALL_DATA"; redigest(d,"split_digest")
    with pytest.raises(Exception): validate_split_contract(d,snap)

def test_environment_network_denied(inputs):
    d=copy.deepcopy(inputs["environment_lock"]); d["network_access_allowed"]=True; redigest(d,"environment_digest")
    with pytest.raises(Exception): validate_environment_lock(d)

def test_budget_zero_denied(inputs):
    d=copy.deepcopy(inputs["compute_budget"]); d["max_tasks"]=0; redigest(d,"budget_digest")
    with pytest.raises(Exception): validate_compute_budget(d)
