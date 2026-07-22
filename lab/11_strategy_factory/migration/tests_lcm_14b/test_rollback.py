def test_rollback(load):
 r=load("rollback_manifest.json")
 assert r["active_legacy_redirect_restore_required"] is False and r["deletion_reversal_required"] is False
