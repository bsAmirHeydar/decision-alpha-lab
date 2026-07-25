def test_revalidation(load,loadl):
 r=load("revalidated_deletion_ledger.json");rows=loadl(r["records_path"]);assert len(rows)==2168 and r["relocated_documentation_count"]==934 and r["canonical_root_copy_count"]==6
