from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schemas
from .static_validation import static_validate
from .verify import verify_package
def run_qa(repo_root:Path,package_root:Path,schema_root:Path,module_root:Path)->dict:
    result=verify_package(repo_root,package_root)
    return {"validation_status":"PASS","candidate_count":result.candidate_count,"approved_relocation_count":result.approved_relocation_count,"blocked_deletion_count":result.blocked_deletion_count,"schema_count":validate_schemas(schema_root),"module_count":static_validate(module_root)}
