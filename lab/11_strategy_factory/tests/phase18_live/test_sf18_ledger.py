from strategy_factory_live import *

def test_live_ledger_is_hash_chained():
    x=AppendOnlyLiveLedger(4)
    x.append(LiveTransactionType.INTENT_RECEIVED,"i",1,"h","received")
    x.append(LiveTransactionType.PREFLIGHT_PASSED,"i",2,"h2","passed")
    assert x.validate_chain() and x.records[1].previous_chain_hash==x.records[0].chain_hash
