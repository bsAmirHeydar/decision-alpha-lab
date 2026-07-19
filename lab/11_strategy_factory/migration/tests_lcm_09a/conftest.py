from pathlib import Path
import json
REPO=Path(__file__).resolve().parents[4]
ROOT=REPO/"registry/legacy_context_migration/setup_contract_freezes/SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891"
def j(rel):return json.loads((ROOT/rel).read_text())
def jl(rel):return [json.loads(x) for x in (ROOT/rel).read_text().splitlines() if x.strip()]
