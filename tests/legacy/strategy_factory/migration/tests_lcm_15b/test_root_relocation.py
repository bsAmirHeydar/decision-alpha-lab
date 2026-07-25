def test_root_relocation(load,loadl):
 r=load("root_relocation_manifest.json");rows=loadl(r["records_path"]);assert len(rows)==6 and all(x["source_retained"] and not x["source_deleted"] for x in rows)
