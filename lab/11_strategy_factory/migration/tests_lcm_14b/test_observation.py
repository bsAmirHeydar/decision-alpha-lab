import json
def test_two_cycles(qroot):
 rows=[json.loads(x) for x in (qroot/"records/observation_cycle_records.jsonl").read_text().splitlines()]
 by={}
 for r in rows: by.setdefault(r["consumer_id"],set()).add(r["cycle_ordinal"]); assert r["meaningful_active_reference_count"]==0
 assert len(by)==136 and all(v=={1,2} for v in by.values())
