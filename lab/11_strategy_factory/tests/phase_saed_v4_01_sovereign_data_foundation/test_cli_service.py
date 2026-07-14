import json
from pathlib import Path
from saed_v4_data_foundation.cli import main
from saed_v4_data_foundation.service import SovereignDataFoundation
ROOT=Path(__file__).resolve().parents[4]
def test_service_wires(tmp_path):
 s=SovereignDataFoundation(tmp_path);assert s.content.root==tmp_path
def test_cli_validate(capsys):
 e=ROOT/'lab/11_strategy_factory/examples/saed_v4_01/source_descriptor.json';s=ROOT/'lab/11_strategy_factory/schemas/saed_v4_01/source_descriptor.schema.json';assert main(['validate','--document',str(e),'--schema',str(s)])==0;assert json.loads(capsys.readouterr().out)['status']=='pass'
def test_cli_hash(capsys):
 e=ROOT/'lab/11_strategy_factory/examples/saed_v4_01/source_descriptor.json';assert main(['hash','--document',str(e)])==0;assert len(capsys.readouterr().out.strip())==64
