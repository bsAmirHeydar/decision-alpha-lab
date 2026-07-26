from src.engine.tooling.strategy_factory.lcm.lcm_06.schema_validation import validate as schemas
from src.engine.tooling.strategy_factory.lcm.lcm_06.static_validation import validate as static
from src.engine.tooling.strategy_factory.lcm.lcm_06.delivery_validation import validate as delivery
def test_schemas(repo_root): r=schemas(repo_root);assert r["passed"] and r["schema_count"]>=25
def test_static(repo_root): r=static(repo_root);assert r["passed"] and r["policy_count"]>=20
def test_delivery(repo_root): assert delivery(repo_root)["passed"]
def test_mql_static_contracts(repo_root):
    root=repo_root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ContextOS/Migration/LCM06";files=list(root.glob("*"));assert len(files)>=12
    text="\n".join(x.read_text(errors="ignore") for x in files if x.is_file());assert "OrderSend(" not in text and "CTrade" not in text and "WebRequest(" not in text
