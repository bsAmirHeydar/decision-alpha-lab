def test_docs(load,loadl):
 r=load("documentation_relocation_receipts.json");rows=loadl(r["records_path"]);assert len(rows)==934 and all(x["redirect_materialized"] and x["redirect_loop_free"] for x in rows)
