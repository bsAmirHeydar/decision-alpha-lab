def test_approvals(load,loadl):
 r=load("deletion_approval_registry.json");rows=loadl(r["records_path"]);assert r["future_deletion_approved_count"]==0 and all(x["role_separation_pass"] for x in rows)
