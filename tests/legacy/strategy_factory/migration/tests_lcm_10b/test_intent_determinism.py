from src.engine.tooling.strategy_factory.lcm.lcm_10b.execution_intent import build_execution_intent
def test_intent_is_deterministic(sample_package):
 r={"decision_id":"D4","side":"SELL","symbol":"XAUUSD","entry":{"kind":"MARKET"}};assert build_execution_intent(sample_package,r)==build_execution_intent(sample_package,r)
