from tools.repository_paths import find_repository_root
from pathlib import Path
from tools.strategy_factory.contexts.rthp.validation import validate_package
ROOT=find_repository_root(__file__)
PKG=ROOT/'contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1'
def test_package_valid():
 r=validate_package(PKG);assert r["passed"],r
def test_no_trading_authority():
 text="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in PKG.rglob("*") if p.is_file() and p.suffix in {".yaml",".md",".json"})
 assert "live_order_submission_allowed: true" not in text
