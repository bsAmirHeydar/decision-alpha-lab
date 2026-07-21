from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schema_directory
from .static_validation import scan_module
from .verify import verify_package

def run(repo_root: Path, inventory_root: Path) -> dict:
    package=verify_package(inventory_root)
    schemas=validate_schema_directory(repo_root/'registry/legacy_context_migration/lcm_10a/schemas/v1')
    static=scan_module(repo_root/'tools/strategy_factory/lcm/lcm_10a')
    return {**package,"qa_passed":True,"schema_count":schemas['schema_count'],"static_validation":static,"source_behavior_changed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False}
