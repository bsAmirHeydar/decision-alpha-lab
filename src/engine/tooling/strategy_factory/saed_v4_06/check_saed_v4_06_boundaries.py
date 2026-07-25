from tools.repository_paths import find_repository_root
from pathlib import Path
import ast

ROOT = find_repository_root(__file__)
PACKAGE = ROOT / "src/engine/packages/saed_v4_treatment_dsl"
FORBIDDEN_IMPORT_PREFIXES = (
    "strategy_factory_execution", "strategy_factory_live", "strategy_factory_portfolio",
    "MetaTrader5", "requests", "httpx", "urllib", "socket", "aiohttp",
    "sklearn", "torch", "tensorflow", "xgboost", "lightgbm", "catboost",
)
FORBIDDEN_CALLS = {
    "order_send", "OrderSend", "send_order", "activate_runtime", "allocate_risk",
    "select_treatment", "solve_action_lattice", "fit", "fit_transform", "predict",
    "predict_proba", "train", "partial_fit", "compile_runtime", "WebRequest",
}
violations=[]
paths=sorted(PACKAGE.glob('*.py'))
if len(paths)<20:
    raise SystemExit('V4-06 Python package is incomplete')
for path in paths:
    text=path.read_text(encoding='utf-8')
    tree=ast.parse(text,filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES): violations.append(f'{path.name}: forbidden import {alias.name}')
        elif isinstance(node,ast.ImportFrom) and node.module:
            if node.module.startswith(FORBIDDEN_IMPORT_PREFIXES): violations.append(f'{path.name}: forbidden import {node.module}')
        elif isinstance(node,ast.Call):
            name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else None
            if name in FORBIDDEN_CALLS: violations.append(f'{path.name}: forbidden call {name}')
if violations:
    raise SystemExit('; '.join(violations))
print(f'boundary scan passed for {len(paths)} Python modules')
