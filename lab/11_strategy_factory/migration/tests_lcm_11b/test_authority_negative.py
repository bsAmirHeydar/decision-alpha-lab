def test_authority_negative(migration_root,load):
 d=load(migration_root/"reports/authority_negative_report.json");assert d["result"]=="PASS";assert d["runtime_authority_count"]==d["order_authority_count"]==d["capital_authority_count"]==0
