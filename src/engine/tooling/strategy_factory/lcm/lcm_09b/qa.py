from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schema_directory
from .static_validation import scan_module
from .verify import verify_package

def run(repo_root:Path,package_root:Path)->dict:
    package=verify_package(package_root)
    schemas=validate_schema_directory(repo_root/"registry/history/lcm/lcm_09b/schemas/v1")
    static=scan_module(repo_root/"src/engine/tooling/strategy_factory/lcm/lcm_09b")
    return {**package,"schema_validation_passed":schemas["passed"],"schema_count":schemas["schema_count"],"static_authority_scan_passed":static["passed"],"python_file_count":static["python_file_count"],"qa_passed":package["passed"] and schemas["passed"] and static["passed"],"metaeditor_compile_claimed":False,"mql5_parity_claimed":False}
