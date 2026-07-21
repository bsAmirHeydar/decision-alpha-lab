from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schemas
from .static_validation import validate_module
from .verify import verify_package

def run_qa(output_root:Path,schema_root:Path,module_root:Path):
    errors=[];errors.extend(verify_package(output_root));errors.extend(validate_schemas(schema_root));errors.extend(validate_module(module_root));return errors
