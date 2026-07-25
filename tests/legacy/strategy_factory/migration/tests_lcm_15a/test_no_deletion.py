def test_no_deletion(loadl):
 assert all(not x["future_deletion_approved"] and not x["deletion_performed"] for x in loadl("records/deletion_candidate_records.jsonl"))
