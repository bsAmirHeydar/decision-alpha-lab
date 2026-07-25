from tools.consolidation.uc02.classification import classify_artifact, classify_symbol


def row(path: str, *, production: bool = False, category: str = "source_code") -> dict:
    return {"path": path, "sha256": "0" * 64, "category": category, "owner_domain": "legacy", "production_source_candidate": production}


def test_root_release_artifact_is_externalized() -> None:
    result = classify_artifact(row("releases/history/lcm/readmes/README_ALPHA_LAB_LCM_16B.md", category="documentation"))
    assert result["canonical_owner"] == "release_history"
    assert result["planning_disposition"] == "EXTERNALIZE"
    assert result["destructive_authority"] is False


def test_rthp_is_a_context_not_a_platform() -> None:
    result = classify_artifact(row("lab/11_strategy_factory/python/strategy_factory_rthp_context_v1/compiler.py", production=True))
    assert result["system_id"] == "RTHP"
    assert result["canonical_owner"] == "context"
    assert result["canonical_target"] == "contexts/rthp"


def test_saed_becomes_extension() -> None:
    result = classify_artifact(row("lab/11_strategy_factory/python/saed_v4_multimodal_views/service.py", production=True))
    assert result["system_id"] == "SAED_V4"
    assert result["canonical_target"] == "src/engine/extensions/saed"
    assert result["migration_action"] == "CONVERT_TO_EXTENSION"


def test_lcm_tooling_becomes_maintenance() -> None:
    result = classify_artifact(row("tools/strategy_factory/lcm/lcm_16b/verify.py", production=True))
    assert result["system_id"] == "LCM"
    assert result["canonical_target"] == "tools/maintenance"


def test_production_under_lab_must_leave_lab() -> None:
    result = classify_artifact(row("lab/example_engine/runtime.py", production=True))
    assert result["planning_disposition"] in {"MOVE", "MERGE"}
    assert not result["canonical_target"].startswith("lab/")


def test_symbol_inherits_one_owner() -> None:
    result = classify_symbol("lab/11_strategy_factory/python/strategy_factory_market/bars.py", "BarClock", "class", "python")
    assert result["canonical_owner"] == "market"
    assert result["destructive_authority"] is False
