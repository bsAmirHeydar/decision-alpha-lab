from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[4]
def test_phase_status():
 s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_07.json').read_text());assert s['implementation_status']=='reference_implementation_complete';assert s['next_phase']=='SAED_V4_08';assert not s['production_authorization']
def test_handoff_status():
 s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_07_HANDOFF_TO_V4_08.json').read_text());assert s['handoff_status']=='ready_reference_only';assert s['authority_preserved']
