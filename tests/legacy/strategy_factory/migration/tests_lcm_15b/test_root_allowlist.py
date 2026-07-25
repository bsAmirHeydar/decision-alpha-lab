def test_root_allowlist(load,loadl):
 r=load("root_allowlist.json");rows=loadl(r["records_path"]);assert len(rows)==r["root_file_count"] and r["root_allowlist_violation_count"]==sum(not x["allowed"] for x in rows)
