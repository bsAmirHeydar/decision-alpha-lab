import json
def test_restoration(qroot):
 rows=[json.loads(x) for x in (qroot/"records/restoration_drill_records.jsonl").read_text().splitlines()]
 assert len(rows)==136 and all(r["result"]=="PASS" and r["payload_hash_match"] and r["redirect_continuity_pass"] for r in rows)
