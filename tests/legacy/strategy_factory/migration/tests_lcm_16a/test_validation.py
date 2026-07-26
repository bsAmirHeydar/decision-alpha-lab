from src.engine.tooling.strategy_factory.lcm.lcm_16a.schema_validation import validate_schemas
from src.engine.tooling.strategy_factory.lcm.lcm_16a.static_validation import static_validate


def test_phase_schemas_are_valid(root):
    assert validate_schemas(root / "registry/history/lcm/lcm_16a/schemas/v1") == 16


def test_phase_module_has_no_forbidden_capability(root):
    assert static_validate(root / "src/engine/tooling/strategy_factory/lcm/lcm_16a") >= 15
