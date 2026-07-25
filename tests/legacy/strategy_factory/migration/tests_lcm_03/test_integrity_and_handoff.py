import copy,pytest
from tools.strategy_factory.lcm.lcm_03.canonical import digest_object
from tools.strategy_factory.lcm.lcm_03.event_ledger import verify
from tools.strategy_factory.lcm.lcm_03.errors import IntegrityError
from tools.strategy_factory.lcm.lcm_03.io import read_json
from tools.strategy_factory.lcm.lcm_03.verify import verify_package

def test_package(identity_root): assert verify_package(identity_root)['passed']
def test_event_chain(identity_root): assert verify(read_json(identity_root/'events/identity_event_ledger.json'))
def test_event_tamper(identity_root):
    x=read_json(identity_root/'events/identity_event_ledger.json');x['events'][1]['event_type']='TAMPERED'
    with pytest.raises(IntegrityError): verify(x)
def test_handoff_digest(identity_root):
    x=read_json(identity_root/'handoff/lcm03_to_lcm04_handoff.json');assert x['handoff_digest']==digest_object(x,'handoff_digest')
def test_handoff_forbids_mutation(identity_root):
    x=read_json(identity_root/'handoff/lcm03_to_lcm04_handoff.json');forbidden=set(x['forbidden_actions']);assert {'MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','CUTOVER_CONSUMER'}.issubset(forbidden)
def test_characterization_not_executed(identity_root): assert not read_json(identity_root/'handoff/lcm03_to_lcm04_handoff.json')['characterization_execution_allowed']
def test_receipt_no_authority(identity_root):
    x=read_json(identity_root/'identity_receipt.json');assert not any(x[k] for k in ['source_move_performed','source_delete_performed','semantic_refactor_performed','merge_performed','cutover_performed','runtime_authority_created','live_order_authority_created','capital_authority_created'])
