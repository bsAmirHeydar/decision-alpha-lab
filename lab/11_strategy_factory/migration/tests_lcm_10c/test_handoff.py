import json
from conftest import CLOSURE
def test_lcm11a_handoff_is_bounded():
 h=json.loads((CLOSURE/'handoff/lcm10c_to_lcm11a_handoff.json').read_text());assert h['handoff_type']=='LCM10C_TO_LCM11A';assert 'VISUAL_OBJECT_INVENTORY' in h['allowed_next_actions'];assert 'ORDER_SUBMISSION' in h['forbidden_actions']
