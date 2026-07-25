#!/usr/bin/env python3
from __future__ import annotations
from tools.repository_paths import find_repository_root
import json, sys
from pathlib import Path
ROOT=find_repository_root(__file__)
INDEX=ROOT/'releases/history/saed/indexes/SAED_V4_00_FILE_INDEX.txt'
allowed_prefixes=(
'src/engine/packages/saed_v4_constitution/',
'schemas/legacy/strategy_factory/saed_v4_00/',
'examples/legacy/strategy_factory/saed_v4_00/',
'tests/legacy/strategy_factory/v1/phase_saed_v4_00_program_constitution/',
'releases/history/strategy_factory/program/status/SAED_V4_00',
'releases/history/strategy_factory/artifacts/SAED_V4_00',
'mql5/Include/AlphaLab/StrategyFactory/SAEDV4Constitution/',
'mql5/Experts/StrategyFactory/SAED_V4_00_',
'mql5/Tests/Experts/StrategyFactory/SAED_V4_00_',
'src/engine/tooling/strategy_factory/saed_v4_00/',
'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_00/',
'docs/obsidian_deep/01_concepts/SAED-V4-00_',
'README_SAED_V4_00_','INSTALL_SAED_V4_00_','COMMIT_MESSAGE.md','releases/history/saed/scripts/EXPAND_REMOVE_SAED_V4_00_PATCH.ps1','SAED_V4_00_')
viol=[]
if INDEX.exists():
 for line in INDEX.read_text(encoding='utf-8').splitlines():
  rel=line.strip()
  if rel and not rel.startswith(allowed_prefixes): viol.append(rel)
print(json.dumps({'status':'pass' if not viol else 'fail','violations':viol},indent=2))
raise SystemExit(0 if not viol else 1)
