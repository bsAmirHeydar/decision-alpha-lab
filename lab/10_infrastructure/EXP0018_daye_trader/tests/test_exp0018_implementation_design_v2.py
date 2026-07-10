from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/'lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_implementation_design_v2.py'
spec=importlib.util.spec_from_file_location('validator',SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def test_design_registry():
    assert mod.validate(ROOT)==[]
