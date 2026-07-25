#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
import os,subprocess,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
env=dict(os.environ);env['PYTHONPATH']=str(ROOT/'src/engine/packages');env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q',str(ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_01_sovereign_data_foundation')],cwd=ROOT,env=env))
