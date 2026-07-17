import pytest
from tools.strategy_factory.acl_os.acl_02.scaffold import scaffold
from tools.strategy_factory.acl_os.acl_02.policies import load_policy

def test_scaffold(tmp_path):
 p=scaffold("CTX_NEW_TEST",tmp_path/"CTX_NEW_TEST");assert (p/"context_manifest.yaml").is_file();assert "CTX_NEW_TEST" in (p/"context_manifest.yaml").read_text()
@pytest.mark.parametrize("bad",["BAD","CTX_x","CTX_","CTX_HAS-DASH"])
def test_bad_context_id_rejected(tmp_path,bad):
 with pytest.raises(ValueError):scaffold(bad,tmp_path/bad)
def test_claim_ceiling_forbids_profit():assert "PROFITABLE" in load_policy("claim_ceiling")["forbidden"]
def test_extensions_forbid_orders():assert "runtime_order_send" in load_policy("extension_policy")["forbidden"]
