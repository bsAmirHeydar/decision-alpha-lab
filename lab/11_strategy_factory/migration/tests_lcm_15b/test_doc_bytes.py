def test_doc_bytes(load,loadl):
 r=load("documentation_relocation_receipts.json");assert all(x["original_source_sha256"]==x["canonical_target_sha256"] for x in loadl(r["records_path"]))
