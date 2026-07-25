import json
from pathlib import Path
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.state import build_snapshot
from saed_v4_context_twin.integrity import build_receipt
from saed_v4_context_twin.handoff import build_v4_03_handoff
from saed_v4_context_twin.conformance import run_vectors

def test_handoff(context_spec,seed):
 m=compile_twin(context_spec,seed);s=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);h=build_v4_03_handoff(m,s,build_receipt(m,s),['no event stream yet']);assert h['phase']=='SAED_V4_02' and h['next_phase']=='SAED_V4_03' and not h['authority']['send_order']
def test_vectors(root):
 v=json.loads((root/'tests/fixtures/legacy/strategy_factory/saed_v4_02/SAED_V4_02_CONFORMANCE_VECTORS.json').read_text());r=run_vectors(v);assert all(x['passed'] for x in r)
