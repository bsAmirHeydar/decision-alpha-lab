import json
from pathlib import Path
import jsonschema

from tools.strategy_factory.lcm.lcm_00.schema_validation import load_schemas
from tools.strategy_factory.lcm.lcm_00.static_validation import validate_registry_tree


def test_all_schemas_are_draft_2020_12(repo_root):
    schemas=load_schemas(repo_root/"registry/legacy_context_migration/lcm_00/schemas/v1")
    assert len(schemas) >= 20


def test_registry_tree_parses(repo_root):
    result=validate_registry_tree(repo_root/"registry/legacy_context_migration/lcm_00")
    assert result["passed"]
    assert result["json_count"] >= 50


def test_handoff_is_non_destructive(baseline_root):
    handoff=json.loads((baseline_root/"handoff/lcm00_to_lcm01_handoff.json").read_text(encoding="utf-8"))
    assert "RUN_FORENSIC_REPOSITORY_SURVEY" in handoff["allowed_actions"]
    for action in ["MOVE_SOURCE_FILE","DELETE_SOURCE_FILE","SEMANTIC_REFACTOR","ACTIVATE_CAPITAL"]:
        assert action in handoff["forbidden_actions"]


def test_unknowns_remain_blockers(baseline_root):
    summary=json.loads((baseline_root/"baseline_summary.json").read_text(encoding="utf-8"))
    assert "GIT_METADATA_UNKNOWN" in summary["blockers"]
    assert summary["state"] != "FROZEN_OPERATIONAL_BASELINE"


def test_no_source_move_or_delete_claim(baseline_root):
    receipt=json.loads((baseline_root/"baseline_receipt.json").read_text(encoding="utf-8"))
    assert receipt["source_file_moved"] is False
    assert receipt["source_file_deleted"] is False
    assert receipt["semantic_change_performed"] is False
