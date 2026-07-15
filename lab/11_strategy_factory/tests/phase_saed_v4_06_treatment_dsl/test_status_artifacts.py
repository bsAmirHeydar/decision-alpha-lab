import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_phase_status_is_reference_only():
 s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_06.json').read_text());assert s['implementation_status']=='reference_implementation_complete';assert not s['production_authorization'];assert s['next_phase']=='SAED_V4_07'
def test_handoff_status_ready():
 s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_06_HANDOFF_TO_V4_07.json').read_text());assert s['handoff_status']=='ready_reference_only';assert s['authority_preserved']
