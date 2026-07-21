from .conftest import ROOT,j
from tools.strategy_factory.lcm.lcm_10a.canonical import digest_object
def test_handoff_is_digest_bound_and_authority_negative():
 h=j('handoff/lcm10a_to_lcm10b_handoff.json');assert h['handoff_digest']=='sha256:6f513e66cc269c963e7380429b82ea78e0fba7812a3ec50fde1070e3c9c5c14b';assert digest_object(h,'handoff_digest')==h['handoff_digest'];assert (ROOT/'LCM10A_TO_LCM10B_HANDOFF.json').read_bytes()==(ROOT/'handoff/lcm10a_to_lcm10b_handoff.json').read_bytes();assert all(not h[k] for k in ('consumer_cutover_allowed','source_move_allowed','source_delete_allowed','promotion_authority_created','runtime_authority_created','live_order_authority_created','capital_authority_created'))
