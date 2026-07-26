from src.engine.tooling.strategy_factory.lcm.lcm_04.io import read_json,read_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_04.trace import reference_inputs,build_trace,trace_bundle
from src.engine.tooling.strategy_factory.lcm.lcm_04.known_time import audit

def test_reference_replay_deterministic(char_root):
    b=read_json(char_root/'traces/reference_trace_bundle.json');assert b['bundle_digest']==trace_bundle(build_trace(reference_inputs()))['bundle_digest']
def test_known_time_pass(char_root): assert audit(list(read_jsonl(char_root/'traces/reference_normalized_events.jsonl')))['status']=='PASS'
def test_no_broker_submission(char_root): assert not any(x['broker_submission_performed'] for x in read_jsonl(char_root/'traces/reference_normalized_events.jsonl'))
