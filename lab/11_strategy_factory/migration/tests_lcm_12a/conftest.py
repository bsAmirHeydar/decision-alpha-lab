from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
MAPPING_ROOT=ROOT/'registry/legacy_context_migration/documentation_authority_mappings/DOCMAP_2AB7C99DBD273C8F29BCD6D455431658'
@pytest.fixture(scope="session")
def mapping_root():return MAPPING_ROOT
@pytest.fixture(scope="session")
def load():return lambda rel:json.loads((MAPPING_ROOT/rel).read_text(encoding="utf-8"))
