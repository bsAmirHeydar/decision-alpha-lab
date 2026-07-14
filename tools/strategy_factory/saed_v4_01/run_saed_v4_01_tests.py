#!/usr/bin/env python3
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
env=dict(os.environ);env['PYTHONPATH']=str(ROOT/'lab/11_strategy_factory/python');env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_01_sovereign_data_foundation')],cwd=ROOT,env=env))
