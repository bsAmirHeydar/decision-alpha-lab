from pathlib import Path
import sys

repo = Path(__file__).resolve().parents[2]
py = repo / "lab/11_strategy_factory/python"
sys.path.insert(0, str(py))
from strategy_factory_runtime.dependency_guard import scan_mql5_boundaries

rules = repo / "lab/11_strategy_factory/phase02_runtime/config/dependency_rules.json"
violations = scan_mql5_boundaries(repo, rules)
for item in violations:
    print(f"{item.file}: {item.reason}: {item.include}")
raise SystemExit(1 if violations else 0)
