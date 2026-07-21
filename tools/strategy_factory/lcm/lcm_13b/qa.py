from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schema_directory
from .static_validation import static_validate
from .verify import verify_package

def run_qa(cutover_root: Path, schema_root: Path, module_root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(verify_package(cutover_root))
    errors.extend(validate_schema_directory(schema_root))
    errors.extend(static_validate(module_root))
    return errors
