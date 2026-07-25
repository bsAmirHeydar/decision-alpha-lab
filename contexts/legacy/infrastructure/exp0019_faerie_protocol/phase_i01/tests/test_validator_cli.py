from tools.repository_paths import find_repository_root
from pathlib import Path
from fp_i01_compatibility.validator import validate
from fp_i01_compatibility.cli import main
ROOT=find_repository_root(__file__)

def test_validator_checks_all_surfaces():
    report,checks=validate(ROOT)
    assert report.status.value=='PASS'
    assert len(checks)==19+8*2+2 and all(x['passed'] for x in checks)

def test_cli_json_returns_zero(capsys):
    assert main([str(ROOT),'--json'])==0
    assert '"status": "PASS"' in capsys.readouterr().out
