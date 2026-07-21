from __future__ import annotations
from pathlib import Path
from .verify import ClosureVerifier
from .schema_validation import validate_schema_catalog
from .static_validation import validate_python

def run_qa(repo_root:Path,closure_root:Path,schema_root:Path,module_root:Path)->dict:
    checks={'closure':ClosureVerifier().verify(closure_root),'schemas':validate_schema_catalog(schema_root),'python':validate_python(module_root)}
    return {'checks':checks,'result':'PASS' if all(x['result']=='PASS' for x in checks.values()) else 'FAIL'}
