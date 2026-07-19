import json
from tools.strategy_factory.lcm.lcm_06.quarantine_validator import validate as qv
from tools.strategy_factory.lcm.lcm_06.deletion_validator import validate as dv
def test_quarantine_ready(repo_root):
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/quarantine/reference_quarantine_records.json").read_text())["records"];assert qv(r[0])["eligible"]
def test_quarantine_blocked(repo_root):
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/quarantine/reference_quarantine_records.json").read_text())["records"];assert not qv(r[1])["eligible"]
def test_deletion_all_gates_still_manual(repo_root):
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/deletion/reference_deletion_records.json").read_text())["records"];o=dv(r[0]);assert o["eligible"] and not o["automatic_delete_allowed"] and not o["delete_performed"]
def test_deletion_missing_gates_blocks(repo_root):
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/deletion/reference_deletion_records.json").read_text())["records"];o=dv(r[1]);assert not o["eligible"] and len(o["missing_gates"])>0

def test_quarantine_never_automatic(repo_root):
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/quarantine/reference_quarantine_records.json").read_text())["records"];o=qv(r[0]);assert o["eligible"] and not o["automatic_quarantine_allowed"]

def test_missing_deletion_id_blocks(repo_root):
    import copy
    r=json.loads((repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/deletion/reference_deletion_records.json").read_text())["records"];item=copy.deepcopy(r[0]);item["deletion_record_id"]="";assert not dv(item)["eligible"]
