from .conftest import j,ROOT
from tools.strategy_factory.lcm.lcm_10b.canonical import digest_object
def test_handoff_is_digest_bound_and_bounded():
 h=j("handoff/lcm10b_to_lcm10c_handoff.json");assert h["handoff_digest"]==digest_object(h,"handoff_digest");assert h["handoff_type"]=="LCM10B_TO_LCM10C";assert (ROOT/"LCM10B_TO_LCM10C_HANDOFF.json").read_bytes()==(ROOT/"handoff/lcm10b_to_lcm10c_handoff.json").read_bytes();assert not h["consumer_cutover_allowed"] and not h["source_move_allowed"] and not h["source_delete_allowed"]
