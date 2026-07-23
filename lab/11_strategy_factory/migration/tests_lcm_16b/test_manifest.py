from tools.strategy_factory.lcm.lcm_16b.io import file_digest, load_json


def test_output_manifest_hashes(package_root):
    manifest = load_json(package_root / "output_manifest.json")
    assert manifest["self_excluded_to_prevent_recursive_hash"] is True
    for item in manifest["files"]:
        assert file_digest(package_root / item["path"]) == item["sha256"]


def test_rollback_is_bounded(package_root):
    rollback = load_json(package_root / "rollback_manifest.json")
    assert rollback["rollback_scope"] == "LCM16B_OWNED_ARTIFACTS_AND_BOUNDED_ROADMAP_EDITS_ONLY"
    assert "LEGACY_SOURCE" in rollback["forbidden_rollback_scope"]


def test_hostile_review_has_core_cases(package_root):
    report = load_json(package_root / "reports/hostile_review_report.json")
    assert report["fail_closed"] is True
    assert "CERTIFICATE_ISSUED_WHILE_BLOCKED" in report["cases"]
