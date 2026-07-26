import json
from pathlib import Path
from jsonschema import Draft202012Validator

def test_schema_registry_closed(repo_root):
    files=list((repo_root/"registry/history/acl/acl_05/schemas/v1").glob("*.schema.json")); assert len(files)>=25
    for p in files: s=json.loads(p.read_text()); Draft202012Validator.check_schema(s); assert s.get("additionalProperties") is False

def test_policy_registry_complete(repo_root):
    files=list((repo_root/"registry/history/acl/acl_05/policies/v1").glob("*.json")); assert len(files)>=20

def test_mql_contract_headers_exist(repo_root):
    files=list((repo_root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL05").glob("*.mqh")); assert len(files)>=12

def test_mql_headers_have_no_order_api(repo_root):
    root=repo_root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL05"; text="\n".join(p.read_text() for p in root.glob("*.mqh")); assert "OrderSend(" not in text and "CTrade" not in text

def test_claim_ceiling_policy(repo_root):
    d=json.loads((repo_root/"registry/history/acl/acl_05/policies/v1/claim_ceiling_policy.json").read_text()); assert d["claim_ceiling"]=="RESEARCH_BATCH_FREEZE_REFERENCE_ONLY"

def test_obsidian_phase_delivery_exists(repo_root):
    root=repo_root/"docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_05"; assert (root/"00_MOC.md").is_file() and len(list(root.glob("*.md")))>=40

def test_atomic_concept_library_exists(repo_root):
    root=repo_root/"docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_05"; assert (root/"00_MOC.md").is_file() and len(list(root.glob("*.md")))>=60
