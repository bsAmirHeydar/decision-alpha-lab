from pathlib import Path
from .verify import verify_package
from .boundary import scan_canonical_boundary
from .schema_validation import validate_schema_directory
from .static_validation import scan_module
def run_qa(repo_root:Path,package_root:Path,schema_root:Path,module_root:Path)->dict:
 checks={"package":verify_package(package_root),"boundary":scan_canonical_boundary(repo_root),"schemas":validate_schema_directory(schema_root),"static":scan_module(module_root)}
 return {"passed":all(x.get("passed") for x in checks.values()),"checks":checks}
