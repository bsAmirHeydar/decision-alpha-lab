import json,subprocess,sys
import pytest
from strategy_factory_policy_v3.migration import migrate_graph_document
from strategy_factory_policy_v3.errors import PolicyError

def test_current_version_identity(): assert migrate_graph_document({'version':'1.0.0','x':1})['x']==1
def test_legacy_graph_migrates(): assert migrate_graph_document({'version':'0.9.0','policy_id':'g'})['graph_id']=='g'
def test_unknown_version_rejected():
    with pytest.raises(PolicyError):migrate_graph_document({'version':'7.0.0'})
def test_cli_registry():
    p=subprocess.run([sys.executable,'-m','strategy_factory_policy_v3.cli','registry'],capture_output=True,text=True,check=True); assert json.loads(p.stdout)['count']==14
