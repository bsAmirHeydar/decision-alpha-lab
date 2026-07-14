#!/usr/bin/env python3
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
env=os.environ.copy(); env['PYTHONPATH']=str(ROOT/'lab/11_strategy_factory/python')+os.pathsep+env.get('PYTHONPATH','')
cmd=[sys.executable,'-m','pytest','-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_00_program_constitution')]
raise SystemExit(subprocess.call(cmd,cwd=ROOT,env=env))
