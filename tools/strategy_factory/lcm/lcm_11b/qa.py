from __future__ import annotations
from pathlib import Path
from .schema_validation import validate_schema_catalog
from .static_validation import validate_python
from .verify import VisualizerMigrationVerifier
def run_qa(repo_root:Path,migration_root:Path,schema_root:Path,module_root:Path)->dict:
    checks=[VisualizerMigrationVerifier().verify(migration_root),validate_schema_catalog(schema_root),validate_python(module_root)]
    return {"result":"PASS" if all(x.get("result")=="PASS" for x in checks) else "FAIL","checks":checks}
