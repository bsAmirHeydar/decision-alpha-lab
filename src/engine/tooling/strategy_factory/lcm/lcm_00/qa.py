from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .schema_validation import load_schemas
from .static_validation import validate_registry_tree
from .verify import verify_baseline_package


def run_qa(repo_root: Path, baseline_root: Path) -> dict:
    schema_root = repo_root / "registry/history/lcm/lcm_00/schemas/v1"
    schemas = load_schemas(schema_root)
    registry = validate_registry_tree(repo_root / "registry/history/lcm/lcm_00")
    baseline = verify_baseline_package(baseline_root)
    compile_result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", str(repo_root / "src/engine/tooling/strategy_factory/lcm/lcm_00")],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "passed": compile_result.returncode == 0 and registry["passed"] and baseline["passed"],
        "schema_count": len(schemas),
        "registry_json_count": registry["json_count"],
        "registry_yaml_count": registry["yaml_count"],
        "baseline": baseline,
        "compileall_returncode": compile_result.returncode,
        "compileall_stderr": compile_result.stderr,
    }
