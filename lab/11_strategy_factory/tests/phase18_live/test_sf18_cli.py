from strategy_factory_live.cli import main

def test_cli_reference(monkeypatch,capsys):
    monkeypatch.setattr("sys.argv",["sf18","--reference-preflight"])
    assert main()==0
    assert '"ledger_valid": true' in capsys.readouterr().out
