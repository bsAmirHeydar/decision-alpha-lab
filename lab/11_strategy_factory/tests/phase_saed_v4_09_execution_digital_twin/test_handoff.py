from helpers import built
from saed_v4_execution_twin.handoff import build_v4_10_handoff

def test_handoff_preserves_no_authority():
    *_,twin=built();h=build_v4_10_handoff(twin);assert h['phase']=='SAED_V4_09' and h['next_phase']=='SAED_V4_10';assert not h['authority']['send_order'];assert not h['authority']['replace_shadow_or_prospective']
