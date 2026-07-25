from helpers import load
def test_phase_status():
 s=load('releases/history/strategy_factory/program/status/SAED_V4_08.json');assert s['implementation_status']=='reference_implementation_complete';assert s['next_phase']=='SAED_V4_09';assert not s['production_authorization']
def test_handoff_status():
 s=load('releases/history/strategy_factory/program/status/SAED_V4_08_HANDOFF_TO_V4_09.json');assert s['handoff_status']=='ready_reference_only'
