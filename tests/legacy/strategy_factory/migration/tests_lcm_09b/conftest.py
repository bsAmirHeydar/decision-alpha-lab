from tools.repository_paths import find_repository_root
from pathlib import Path
import json
REPO=find_repository_root(__file__)
ROOT=REPO/"registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9"
SCHEMAS=REPO/"registry/legacy_context_migration/lcm_09b/schemas/v1"
def j(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def jl(rel):return [json.loads(x) for x in (ROOT/rel).read_text(encoding="utf-8").splitlines() if x.strip()]
