from pathlib import Path
import ast

REPO = Path(__file__).resolve().parents[4]
MOD = REPO / "tools/strategy_factory/lcm/lcm_08c"

def test_python_modules_parse():
    for p in MOD.glob("*.py"):
        ast.parse(p.read_text(), filename=str(p))

def test_no_order_or_chart_object_api_in_phase_module():
    text = "\n".join(p.read_text() for p in MOD.glob("*.py") if p.name != "qa.py")
    forbidden = ["OrderSend","CTrade",".Buy(",".Sell(","PositionOpen","PositionModify","PositionClose","ObjectCreate","ObjectSet","ChartRedraw"]
    assert not [x for x in forbidden if x in text]
