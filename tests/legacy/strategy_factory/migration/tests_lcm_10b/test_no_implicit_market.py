from tools.strategy_factory.lcm.lcm_10b.execution_intent import build_execution_intent
def test_missing_entry_kind_blocks(sample_package):
 i=build_execution_intent(sample_package,{"decision_id":"D2","side":"BUY","symbol":"EURUSD","entry":{}});assert i["validation_status"]=="BLOCKED";assert "ENTRY_KIND_REQUIRED" in i["rejection_reasons"]
