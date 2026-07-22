import json
def test_blocked_records(package_root):rows=[json.loads(x) for x in (package_root/'records/blocked_deletion_records.jsonl').read_text().splitlines() if x];assert len(rows)==2168 and all(not r['deletion_approved'] for r in rows)
