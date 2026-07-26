from src.engine.tooling.strategy_factory.lcm.lcm_12a.canonical import digest_object,stable_id
def test_stable_identity():
    assert stable_id("DOC","a","b")==stable_id("DOC","a","b")
    assert digest_object({"b":2,"a":1})==digest_object({"a":1,"b":2})
