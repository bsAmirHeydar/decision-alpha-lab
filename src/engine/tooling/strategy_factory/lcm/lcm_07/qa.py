from pathlib import Path
from .verify import verify_package
from .schema_validation import validate
from .static_validation import scan

def run(repo_root:Path,shared_engine_root:Path):
    package=verify_package(shared_engine_root);schemas=validate(repo_root/"registry/legacy_context_migration/lcm_07/schemas/v1",shared_engine_root);findings=scan(repo_root/"src/engine/tooling/strategy_factory/lcm/lcm_07")
    return {"passed":package["passed"] and schemas["passed"] and not findings,"package":package,"schemas":schemas,"static_findings":findings}
