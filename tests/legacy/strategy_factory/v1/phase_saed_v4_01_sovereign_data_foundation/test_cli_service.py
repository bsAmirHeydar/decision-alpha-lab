from tools.repository_paths import find_repository_root
import json
from pathlib import Path
from saed_v4_data_foundation.cli import main
from saed_v4_data_foundation.service import SovereignDataFoundation
ROOT=find_repository_root(__file__)
def test_service_wires(tmp_path):
 s=SovereignDataFoundation(tmp_path);assert s.content.root==tmp_path
def test_cli_validate(capsys):
 e=ROOT/'examples/legacy/strategy_factory/saed_v4_01/source_descriptor.json';s=ROOT/'schemas/legacy/strategy_factory/saed_v4_01/source_descriptor.schema.json';assert main(['validate','--document',str(e),'--schema',str(s)])==0;assert json.loads(capsys.readouterr().out)['status']=='pass'
def test_cli_hash(capsys):
 e=ROOT/'examples/legacy/strategy_factory/saed_v4_01/source_descriptor.json';assert main(['hash','--document',str(e)])==0;assert len(capsys.readouterr().out.strip())==64
