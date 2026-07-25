from pathlib import Path

import yaml

from tools.consolidation.uc02.contracts import load_contracts, validate_contracts


def test_all_machine_contracts_validate(repo_root: Path) -> None:
    result = validate_contracts(repo_root)
    assert result["status"] == "PASS", result
    assert result["contract_count"] == 12


def test_product_is_not_nested(repo_root: Path) -> None:
    constitution = yaml.safe_load((repo_root / "policies/platform/architecture_constitution.yaml").read_text(encoding="utf-8"))
    assert constitution["product_name"] == "Alpha Lab"
    assert constitution["canonical_production_root"] == "src/engine"
    assert constitution["nested_product_root_forbidden"] is True


def test_every_contract_disables_authority(repo_root: Path) -> None:
    for relative, contract in load_contracts(repo_root).items():
        for flag in ("destructive_authority", "runtime_authority", "order_authority", "broker_authority", "capital_authority"):
            assert contract[flag] is False, (relative, flag)


def test_system_disposition_is_complete(repo_root: Path) -> None:
    contract = yaml.safe_load((repo_root / "contracts/platform/system_disposition.yaml").read_text(encoding="utf-8"))
    assert set(contract["systems"]) == {"STRATEGY_FACTORY", "ACL_OS", "UCEE", "SAED_V3", "SAED_V4", "AIEOS", "LCM", "RTHP", "NDS", "EXPERIMENTS"}


def test_dependency_kernel_has_no_upstream_dependency(repo_root: Path) -> None:
    contract = yaml.safe_load((repo_root / "policies/platform/dependency_rules.yaml").read_text(encoding="utf-8"))
    assert contract["allowed_dependencies"]["kernel"] == []
    assert "research -> broker/order API" in contract["forbidden_edges"]
