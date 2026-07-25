from tools.strategy_factory.acl_os.acl_08.delivery_validator import validate_delivery
from tools.strategy_factory.acl_os.acl_08.static_validator import validate_registry_files


def test_registry_files_valid():
    result = validate_registry_files()
    assert result["passed"]
    assert result["schema_count"] >= 20
    assert result["policy_count"] >= 20


def test_delivery(repo_root):
    assert validate_delivery(repo_root)["passed"]


def test_mql_guards_present(repo_root):
    root = repo_root / "mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL08"
    text = "\n".join(path.read_text() for path in root.glob("*.mqh"))
    assert "ACL08_LIVE_ORDER_SUBMISSION_ALLOWED false" in text
    assert "ACL08_CAPITAL_ACTIVATION_ALLOWED false" in text
    assert "ACL08_PROMOTION_ALLOWED false" in text


def test_docs_are_present(repo_root):
    root = repo_root / "docs/alpha_lab_master_architecture/context_lifecycle_os"
    assert (root / "12_PHASE_DELIVERIES/ACL_08/00_MOC.md").exists()
    assert (root / "13_ATOMIC_CONCEPTS/ACL_08/000_MOC.md").exists()
