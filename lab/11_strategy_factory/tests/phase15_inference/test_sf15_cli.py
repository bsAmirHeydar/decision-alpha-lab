from strategy_factory_inference.cli import main

def test_cli_export_and_inspect(tmp_path,capsys):
 p=tmp_path/"m.onnx";assert main(["export-linear","--weights","1,2","--bias","0.5","--out",str(p)])==0
 assert p.exists();assert main(["inspect",str(p)])==0
 assert "MatMul" in capsys.readouterr().out
