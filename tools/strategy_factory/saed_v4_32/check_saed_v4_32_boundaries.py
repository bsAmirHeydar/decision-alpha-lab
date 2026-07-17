from __future__ import annotations
import ast
from _common import ROOT
pkg = ROOT / "lab/11_strategy_factory/python/saed_v4_multi_agent_research_constitution"
forbidden_imports = {"requests", "urllib", "httpx", "socket", "subprocess", "asyncio.subprocess", "MetaTrader5"}
for path in pkg.glob("*.py"):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name not in forbidden_imports, (path, alias.name)
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module not in forbidden_imports, (path, node.module)
text = "\n".join(p.read_text(encoding="utf-8") for p in pkg.glob("*.py"))
for forbidden in ["order_send(", "OrderSend(", "trade.Buy(", "trade.Sell(", "login(", "password=", "secret_key"]:
    assert forbidden not in text
print("V4-32 authority and network boundary passed")
