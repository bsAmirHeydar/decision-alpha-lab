from tools.repository_paths import find_repository_root
from pathlib import Path
import ast

ROOT = find_repository_root(__file__)
PACKAGE = ROOT / "src/engine/packages/saed_v4_semantic_hypergraph"
FORBIDDEN_IMPORT_PREFIXES = (
    "strategy_factory_execution",
    "strategy_factory_live",
    "strategy_factory_portfolio",
    "MetaTrader5",
    "requests",
    "httpx",
    "socket",
)
FORBIDDEN_CALLS = {
    "order_send",
    "OrderSend",
    "activate_runtime",
    "allocate_risk",
    "select_treatment",
    "train",
    "fit",
}
violations = []
for path in sorted(PACKAGE.glob("*.py")):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES):
                    violations.append(f"{path.name}: forbidden import {alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                violations.append(f"{path.name}: forbidden import {node.module}")
        elif isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in FORBIDDEN_CALLS:
                violations.append(f"{path.name}: forbidden call {name}")
if violations:
    raise SystemExit("; ".join(violations))
print(f"boundary scan passed for {len(list(PACKAGE.glob('*.py')))} Python modules")
