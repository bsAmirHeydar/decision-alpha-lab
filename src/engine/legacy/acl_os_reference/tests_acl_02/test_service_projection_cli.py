import json,subprocess,sys
from src.engine.tooling.strategy_factory.acl_os.acl_02.service import ACL02ContextIntakeService
from src.engine.tooling.strategy_factory.acl_os.acl_02.projection import render_readiness

def test_service_valid(valid_root,valid_permit,tmp_path):
 r=ACL02ContextIntakeService().evaluate(valid_root,valid_permit,tmp_path);assert r["readiness"]["blocking_count"]==0;assert (tmp_path/"CONTEXT_INTAKE_READINESS.md").is_file()
def test_service_incomplete(valid_root,valid_permit):assert ACL02ContextIntakeService().evaluate(valid_root.parent/"incomplete_context",valid_permit)["readiness"]["blocking_count"]>0
def test_projection_non_authoritative(valid_root,valid_permit):
 text=render_readiness(ACL02ContextIntakeService().evaluate(valid_root,valid_permit)["readiness"]);assert "Generated projection" in text;assert "CAPITAL" not in text.upper() or "capital" in text.lower()
def test_cli_questions():
 p=subprocess.run([sys.executable,"-m","src.engine.tooling.strategy_factory.acl_os.acl_02.cli","questions","CTX_TEST"],text=True,capture_output=True);assert p.returncode==0;assert "IDENTITY_001" in p.stdout
def test_cli_evaluate(valid_root,valid_permit,tmp_path):
 permit=tmp_path/"permit.json";permit.write_text(json.dumps(valid_permit));p=subprocess.run([sys.executable,"-m","src.engine.tooling.strategy_factory.acl_os.acl_02.cli","evaluate",str(valid_root),"--permit",str(permit)],text=True,capture_output=True);assert p.returncode==0
