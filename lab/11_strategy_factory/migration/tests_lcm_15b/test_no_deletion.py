def test_no_deletion(load,loadl):
 r=load("revalidated_deletion_ledger.json");rows=loadl(r["records_path"]);assert r["future_deletion_approved_count"]==0 and all(not x["future_deletion_approved"] and not x["deletion_performed"] for x in rows)
