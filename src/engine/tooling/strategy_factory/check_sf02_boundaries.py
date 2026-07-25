from tools.repository_paths import find_repository_root
from pathlib import Path
import sys

repo = find_repository_root(__file__)
py = repo / "src/engine/packages"
sys.path.insert(0, str(py))
from strategy_factory_runtime.dependency_guard import scan_mql5_boundaries

rules = repo / "src/engine/legacy/strategy_factory/runtime/config/dependency_rules.json"
violations = scan_mql5_boundaries(repo, rules)
for item in violations:
    print(f"{item.file}: {item.reason}: {item.include}")
raise SystemExit(1 if violations else 0)
