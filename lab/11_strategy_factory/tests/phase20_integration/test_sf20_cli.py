import json
from strategy_factory_integration.cli import main

def test_cli_golden(tmp_path):
    out=tmp_path/"golden.json"; assert main(["golden","--output",str(out)])==0
    data=json.loads(out.read_text()); assert data["differential"]["passed"] is True
