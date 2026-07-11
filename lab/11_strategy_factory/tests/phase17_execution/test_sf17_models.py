from strategy_factory_execution import *

def test_policy_hash_and_validation():
    p=PaperExecutionPolicy("p","1",ExecutionMode.PAPER,0.01,1.0,2.0,0.5,1000,False,True,True,17)
    p.validate(); assert p.derived_hash().startswith("xpol_")

def test_quote_rejects_crossed_market():
    q=QuoteObservation("X",101,100,1,1)
    try: q.validate()
    except ValueError: pass
    else: raise AssertionError("crossed quote accepted")
