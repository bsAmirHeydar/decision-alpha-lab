from src.engine.tooling.strategy_factory.lcm.lcm_10b.execution_intent import build_execution_intent
def test_wrong_side_stop_blocks(sample_package):
 base={"decision_id":"D3","side":"BUY","symbol":"EURUSD","entry":{"kind":"LIMIT","price":"1.10"},"stop":{"kind":"HARD","price":"1.11"}};i=build_execution_intent(sample_package,base);assert "BUY_STOP_NOT_BELOW_ENTRY" in i["rejection_reasons"]
