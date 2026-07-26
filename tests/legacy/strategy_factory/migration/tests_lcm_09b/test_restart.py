import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_09b.restart import checkpoint,restore
from src.engine.tooling.strategy_factory.lcm.lcm_09b.errors import ReplayError
def test_checkpoint_round_trip_is_digest_bound():
 s={"setup_id":"SETUP_TEST","occurrence_id":"OCC_TEST","last_sequence":3,"decision_state":"TRIGGERED","last_decision_digest":"sha256:"+"1"*64,"reason_codes":[]};c=checkpoint(s);assert restore(c)["last_sequence"]==3
def test_checkpoint_tamper_fails():
 s={"setup_id":"SETUP_TEST","occurrence_id":"OCC_TEST","last_sequence":3,"decision_state":"TRIGGERED","last_decision_digest":"sha256:"+"1"*64,"reason_codes":[]};c=checkpoint(s);c["last_sequence"]=4
 with pytest.raises(ReplayError):restore(c)
