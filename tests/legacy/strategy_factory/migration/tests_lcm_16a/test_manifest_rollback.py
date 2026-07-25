from tools.strategy_factory.lcm.lcm_16a.io import file_digest


def test_output_manifest_matches_package(load, audit_root):
    manifest = load("output_manifest.json")
    assert manifest["self_excluded_to_prevent_recursive_hash"] is True
    assert manifest["file_count"] == len(manifest["files"]) == 17
    for item in manifest["files"]:
        assert file_digest(audit_root / item["path"]) == item["sha256"]


def test_rollback_is_bounded(load):
    rollback = load("rollback_manifest.json")
    assert rollback["validation_status"] == "PASS"
    assert "BROAD_WILDCARD_DELETE" in rollback["forbidden_rollback_actions"]
    assert rollback["deletion_authority_created"] is False
