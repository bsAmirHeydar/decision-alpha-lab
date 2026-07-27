import json
from .conftest import CLOSURE
def test_all_replays_zero_authority():
 for line in (CLOSURE/'dry_run/dry_run_replay_results.jsonl').read_text().splitlines():
  r=json.loads(line);assert r['submission_attempt_count']==r['live_order_count']==r['paper_order_count']==r['capital_activation_count']==0
def test_handoff_zero_authority():
 h=json.loads((CLOSURE/'handoff/lcm10c_to_lcm11a_handoff.json').read_text());assert not h['runtime_authority_created'];assert not h['live_order_authority_created'];assert not h['capital_authority_created']
