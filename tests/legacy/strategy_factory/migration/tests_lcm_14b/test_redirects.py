import json
def test_redirects_retained(qroot):
 rows=[json.loads(x) for x in (qroot/"records/quarantine_package_records.jsonl").read_text().splitlines()]
 assert all(r["legacy_redirect_retained"] and r["canonical_source_retained"] for r in rows)
