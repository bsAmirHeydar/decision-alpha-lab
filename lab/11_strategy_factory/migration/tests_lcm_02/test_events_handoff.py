import json,pytest
from tools.strategy_factory.lcm.lcm_02.event_ledger import verify
from tools.strategy_factory.lcm.lcm_02.canonical import digest_object

def test_event_chain(classification_root): verify(json.loads((classification_root/'events/classification_event_ledger.json').read_text()))
def test_event_tamper_detected(classification_root):
 x=json.loads((classification_root/'events/classification_event_ledger.json').read_text()); x['events'][1]['payload']={'tampered':True}
 with pytest.raises(Exception): verify(x)
def test_handoff_forbids_move(classification_root):
 x=json.loads((classification_root/'handoff/lcm02_to_lcm03_handoff.json').read_text()); assert 'MOVE_SOURCE_FILE' in x['forbidden_actions']; assert x['handoff_digest']==digest_object(x,'handoff_digest')
