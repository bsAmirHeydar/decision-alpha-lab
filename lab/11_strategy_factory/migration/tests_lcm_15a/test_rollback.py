def test_rollback(load):
 r=load("rollback_manifest.json");assert not r["deletion_reversal_required"] and not r["relocation_reversal_required"]
