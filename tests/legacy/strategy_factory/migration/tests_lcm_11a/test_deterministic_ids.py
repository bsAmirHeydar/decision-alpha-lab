from src.engine.tooling.strategy_factory.lcm.lcm_11a.canonical import stable_id
def test_stable_id_is_repeatable():
    a=stable_id('VISOBJ','path',12,'OBJ_TREND','name')
    b=stable_id('VISOBJ','path',12,'OBJ_TREND','name')
    c=stable_id('VISOBJ','path',13,'OBJ_TREND','name')
    assert a==b and a!=c
