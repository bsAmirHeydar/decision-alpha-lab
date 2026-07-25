def test_ledger(load,loadl):
 r=load("deletion_candidate_ledger.json");rows=loadl(r["records_path"]);assert r["record_count"]==2168==len(rows);assert len({x["candidate_path"] for x in rows})==2168
