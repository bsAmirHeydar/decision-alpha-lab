import json
def test_external_unknown(qroot):
 rows=[json.loads(x) for x in (qroot/"records/retirement_eligibility_records.jsonl").read_text().splitlines()]
 assert len(rows)==136
 assert all(r["external_consumer_evidence_state"]=="UNKNOWN_BLOCKING_DELETION_APPROVAL" for r in rows)
 assert all(r["deletion_approved"] is False for r in rows)
