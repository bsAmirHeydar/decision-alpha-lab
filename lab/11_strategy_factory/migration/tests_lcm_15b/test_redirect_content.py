def test_redirect_content(repo_root,load,loadl):
 r=load("documentation_relocation_receipts.json")
 for x in loadl(r["records_path"]):
  text=(repo_root/x["legacy_path"]).read_text(encoding="utf-8");assert "compatibility-redirect" in text and x["canonical_target_path"] in text
