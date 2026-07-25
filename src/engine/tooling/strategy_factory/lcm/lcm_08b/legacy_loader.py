from __future__ import annotations
import importlib.util,sys
from pathlib import Path

def load_legacy(repo_root:Path):
    path=repo_root/"contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/experiment.py"
    spec=importlib.util.spec_from_file_location("lcm08b_exp0015_legacy",path)
    if spec is None or spec.loader is None:raise RuntimeError("cannot load legacy source")
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);return module
