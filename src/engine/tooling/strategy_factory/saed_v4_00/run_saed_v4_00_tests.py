#!/usr/bin/env python3
from __future__ import annotations
from tools.repository_paths import find_repository_root
import os, subprocess, sys
from pathlib import Path
ROOT=find_repository_root(__file__)
env=os.environ.copy(); env['PYTHONPATH']=str(ROOT/'src/engine/packages')+os.pathsep+env.get('PYTHONPATH','')
cmd=[sys.executable,'-m','pytest','-q',str(ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_00_program_constitution')]
raise SystemExit(subprocess.call(cmd,cwd=ROOT,env=env))
