from src.engine.tooling.strategy_factory.lcm.lcm_07.canonical import content_id,digest_object

def test_content_id_deterministic():assert content_id("X",{"b":2,"a":1})==content_id("X",{"a":1,"b":2})
def test_digest_omit_field():
 o={"a":1,"digest":None};o["digest"]=digest_object(o,"digest");assert digest_object(o,"digest")==o["digest"]
