from strategy_factory_execution.cli import main

def test_cli_no_args(monkeypatch):
    monkeypatch.setattr("sys.argv",["sf17"]); assert main()==0
