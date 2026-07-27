from .helpers import cube
from saed_v4_outcome_cube.handoff import build_v4_09_handoff
def test_handoff_preserves_no_authority():
 h=build_v4_09_handoff(cube());assert h['next_phase']=='SAED_V4_09';assert not h['authority']['send_order'];assert not h['authority']['rank_treatments']
