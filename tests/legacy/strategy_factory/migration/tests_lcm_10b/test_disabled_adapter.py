import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_10b.adapters import DisabledExecutionAdapter
from src.engine.tooling.strategy_factory.lcm.lcm_10b.errors import CapabilityDeniedError
from src.engine.tooling.strategy_factory.lcm.lcm_10b.execution_intent import build_execution_intent
from .conftest import ROOT,j,jl
def test_adapter_records_dry_and_never_submits(sample_package):
 r=jl("execution_adapter_contracts/execution_adapter_contract_registry.jsonl")[0];c=j(f"execution_adapter_contracts/{r['adapter_id']}.json");a=DisabledExecutionAdapter(c,j("guards/capability_guard_policy.json"));i=build_execution_intent(sample_package,{"decision_id":"D7","side":"BUY","symbol":"EURUSD","entry":{"kind":"MARKET"}});o=a.dry_run(i);assert not o["accepted_for_submission"] and not o["broker_api_invoked"]
 with pytest.raises(CapabilityDeniedError):a.submit(i)
