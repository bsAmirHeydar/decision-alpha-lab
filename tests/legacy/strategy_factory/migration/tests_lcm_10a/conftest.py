from tools.repository_paths import find_repository_root
from pathlib import Path
import json
REPO=find_repository_root(__file__)
ROOT=REPO/'registry/legacy_context_migration/treatment_execution_inventories/TREATINV_98D30D63F6B6CA7BEA4ABAC517956B02'
SCHEMAS=REPO/'registry/legacy_context_migration/lcm_10a/schemas/v1'
def j(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def jl(rel): return [json.loads(x) for x in (ROOT/rel).read_text(encoding='utf-8').splitlines() if x.strip()]
