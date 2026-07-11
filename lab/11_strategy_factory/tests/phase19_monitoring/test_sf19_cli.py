import json
from strategy_factory_monitoring.cli import main

def test_cli_compact(capsys):
    assert main(["--compact"] )==0;data=json.loads(capsys.readouterr().out);assert data["telemetry_count"]==5
