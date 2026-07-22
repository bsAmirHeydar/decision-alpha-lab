from pathlib import Path
from .verify import verify_package
from .schema_validation import validate_schema_directory
from .static_validation import static_validate
def run_qa(root:Path,schema_root:Path,module_root:Path)->list[str]: return verify_package(root)+validate_schema_directory(schema_root)+static_validate(module_root)
