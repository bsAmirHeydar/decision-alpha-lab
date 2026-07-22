def test_rewrites(load):
 r=load("reference_rewrite_receipt.json");assert r["planned_record_count"]==69 and r["replacement_count"]>=0
