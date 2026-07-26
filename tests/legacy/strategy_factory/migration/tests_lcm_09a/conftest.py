from tools.repository_paths import find_repository_root
from pathlib import Path
import json
REPO=find_repository_root(__file__)
ROOT=REPO/"registry/history/lcm/setup_contract_freezes/SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891"
def j(rel):return json.loads((ROOT/rel).read_text())
def jl(rel):return [json.loads(x) for x in (ROOT/rel).read_text().splitlines() if x.strip()]
