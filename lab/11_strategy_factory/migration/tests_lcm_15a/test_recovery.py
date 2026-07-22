def test_recovery(load):
 r=load("recovery_proof.json");assert r["record_count"]==2168 and r["active_path_write_count"]==0
