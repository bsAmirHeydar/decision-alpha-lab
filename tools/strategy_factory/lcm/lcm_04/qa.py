from pathlib import Path
from .delivery_validation import validate as delivery
from .schema_validation import validate as schemas
from .static_validation import validate as static
from .verify import verify_package

def run_qa(repo_root: Path,characterization_root: Path):
    pkg=verify_package(characterization_root);s=static(repo_root);sch=schemas(repo_root);d=delivery(repo_root)
    return {'passed':pkg['passed'] and s['passed'] and sch['passed'] and d['passed'],'package':pkg,'static':s,'schemas':sch,'delivery':d}
