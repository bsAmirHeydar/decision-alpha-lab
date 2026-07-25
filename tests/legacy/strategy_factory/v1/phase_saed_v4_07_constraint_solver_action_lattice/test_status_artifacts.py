from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
def test_phase_status():
 s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_07.json').read_text());assert s['implementation_status']=='reference_implementation_complete';assert s['next_phase']=='SAED_V4_08';assert not s['production_authorization']
def test_handoff_status():
 s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_07_HANDOFF_TO_V4_08.json').read_text());assert s['handoff_status']=='ready_reference_only';assert s['authority_preserved']
