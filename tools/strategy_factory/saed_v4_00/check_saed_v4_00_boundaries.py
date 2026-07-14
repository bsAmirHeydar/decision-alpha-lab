#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
INDEX=ROOT/'SAED_V4_00_FILE_INDEX.txt'
allowed_prefixes=(
'lab/11_strategy_factory/python/saed_v4_constitution/',
'lab/11_strategy_factory/schemas/saed_v4_00/',
'lab/11_strategy_factory/examples/saed_v4_00/',
'lab/11_strategy_factory/tests/phase_saed_v4_00_program_constitution/',
'lab/11_strategy_factory/phase_status/SAED_V4_00',
'lab/11_strategy_factory/artifacts/SAED_V4_00',
'mql5/Include/AlphaLab/StrategyFactory/SAEDV4Constitution/',
'mql5/Experts/StrategyFactory/SAED_V4_00_',
'mql5/Experts/StrategyFactoryTests/SAED_V4_00_',
'tools/strategy_factory/saed_v4_00/',
'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_00/',
'docs/obsidian_deep/01_concepts/SAED-V4-00_',
'README_SAED_V4_00_','INSTALL_SAED_V4_00_','COMMIT_MESSAGE.md','EXPAND_REMOVE_SAED_V4_00_PATCH.ps1','SAED_V4_00_')
viol=[]
if INDEX.exists():
 for line in INDEX.read_text(encoding='utf-8').splitlines():
  rel=line.strip()
  if rel and not rel.startswith(allowed_prefixes): viol.append(rel)
print(json.dumps({'status':'pass' if not viol else 'fail','violations':viol},indent=2))
raise SystemExit(0 if not viol else 1)
