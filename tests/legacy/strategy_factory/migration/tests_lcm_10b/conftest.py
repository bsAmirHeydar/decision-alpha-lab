from tools.repository_paths import find_repository_root
from pathlib import Path
import json,pytest
REPO=find_repository_root(__file__)
ROOT=REPO/'registry/history/lcm/treatment_package_migrations/TREATMIG_DCC2F1F7B74985D72A783020843C6B51'
SCHEMAS=REPO/'registry/history/lcm/lcm_10b/schemas/v1'
MODULE=REPO/'src/engine/tooling/strategy_factory/lcm/lcm_10b'
def j(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def jl(rel):return [json.loads(x) for x in (ROOT/rel).read_text(encoding="utf-8").splitlines() if x.strip()]
@pytest.fixture(scope="session")
def sample_package(jl=jl):
 r=jl("registries/treatment_package_registry.jsonl")[0];return json.loads((ROOT/r["package_path"]).read_text(encoding="utf-8"))
