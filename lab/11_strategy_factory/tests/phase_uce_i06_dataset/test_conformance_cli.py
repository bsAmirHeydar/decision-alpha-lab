from strategy_factory_dataset_v3.conformance import run_conformance
from strategy_factory_dataset_v3.cli import main

def test_conformance_passes():
 r=run_conformance(); assert r['accepted']; assert r['cell_count']==24

def test_cli(capsys):
 assert main(['conformance'])==0; assert 'cube_set_hash' in capsys.readouterr().out
