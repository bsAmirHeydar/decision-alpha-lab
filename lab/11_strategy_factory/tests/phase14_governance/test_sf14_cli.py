import json
from strategy_factory_governance.cli import main

def test_cli_emits_reference_bundle(tmp_path,capsys):
    assert main(["emit-reference",str(tmp_path)])==0
    assert (tmp_path/"registry_snapshot.json").is_file()
    assert (tmp_path/"governance_decisions.jsonl").is_file()
    output=json.loads(capsys.readouterr().out)
    assert output["snapshot_hash"].startswith("rsnap_")
