from __future__ import annotations
from tools.strategy_factory.lcm.lcm_13b.schema_validation import validate_schema_directory
from tools.strategy_factory.lcm.lcm_13b.static_validation import static_validate

def test_schemas(repo_root):
    assert validate_schema_directory(repo_root / "registry/legacy_context_migration/lcm_13b/schemas/v1") == []

def test_static_boundary(repo_root):
    assert static_validate(repo_root / "tools/strategy_factory/lcm/lcm_13b") == []
