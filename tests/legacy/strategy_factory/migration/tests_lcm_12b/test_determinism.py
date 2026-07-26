from src.engine.tooling.strategy_factory.lcm.lcm_12b.canonical import stable_id,digest_object
def test_deterministic_helpers():
    assert stable_id("X","a",1)==stable_id("X","a",1)
    assert digest_object({"b":2,"a":1})==digest_object({"a":1,"b":2})
