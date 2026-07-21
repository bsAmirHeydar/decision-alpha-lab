import json
from .conftest import ROOT,jl
def test_adapter_contract_files_match_registry():
 for r in jl("execution_adapter_contracts/execution_adapter_contract_registry.jsonl"):
  p=ROOT/f"execution_adapter_contracts/{r['adapter_id']}.json";assert p.is_file();assert json.loads(p.read_text())["adapter_digest"]==r["adapter_digest"]
