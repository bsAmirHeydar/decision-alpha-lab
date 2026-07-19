from __future__ import annotations
import ast
from pathlib import Path
from .errors import VerificationError
from .schema_validation import validate_schema_directory
from .verify import verify_package

FORBIDDEN = (
    "OrderSend", "CTrade", ".Buy(", ".Sell(", "PositionOpen",
    "PositionModify", "PositionClose", "ObjectCreate", "ObjectSet",
    "ChartRedraw",
)


def run(repo_root: Path, closure_root: Path) -> dict:
    result = verify_package(closure_root)
    module_root = repo_root / "tools/strategy_factory/lcm/lcm_08c"
    py_files = sorted(module_root.glob("*.py"))
    for path in py_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    scan_files = [path for path in py_files if path.name != "qa.py"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in scan_files)
    hits = [token for token in FORBIDDEN if token in text]
    if hits:
        raise VerificationError(f"forbidden authority API hits: {hits}")
    phase_doc = repo_root / (
        "docs/alpha_lab_master_architecture/context_lifecycle_os/"
        "17_LEGACY_MIGRATION_PROGRAM/05_PHASES/"
        "LCM_08C_CONTEXT_WAVE_MIGRATION_AND_CONTEXT_PORTFOLIO_CLOSURE.md"
    )
    if "status: accepted-reference" not in phase_doc.read_text(encoding="utf-8"):
        raise VerificationError("phase status not accepted-reference")
    schema = validate_schema_directory(
        repo_root / "registry/legacy_context_migration/lcm_08c/schemas/v1"
    )
    return {
        **result,
        "python_file_count": len(py_files),
        "schema_count": schema["schema_count"],
        "forbidden_authority_api_hits": 0,
        "qa_passed": True,
    }
