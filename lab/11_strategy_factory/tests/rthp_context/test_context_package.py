from pathlib import Path
from tools.strategy_factory.contexts.rthp.validation import validate_package
ROOT=Path(__file__).resolve().parents[4]
PKG=ROOT/'lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1'
def test_package_valid():
 r=validate_package(PKG);assert r["passed"],r
def test_no_trading_authority():
 text="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in PKG.rglob("*") if p.is_file() and p.suffix in {".yaml",".md",".json"})
 assert "live_order_submission_allowed: true" not in text
