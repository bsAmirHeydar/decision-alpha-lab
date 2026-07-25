from tools.repository_paths import find_repository_root
from pathlib import Path
import importlib.util

ROOT=find_repository_root(__file__)
SCRIPT=ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_implementation_design_v2.py'
spec=importlib.util.spec_from_file_location('validator',SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def test_design_registry():
    assert mod.validate(ROOT)==[]
