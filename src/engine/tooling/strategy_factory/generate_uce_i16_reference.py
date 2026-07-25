#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from strategy_factory_onboarding_v3.golden import golden_run
from strategy_factory_onboarding_v3.canonical import normalize
r=golden_run(ROOT)
out=ROOT/'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16/reference_generation.json'
payload={'context_spec_hash':r[0].spec_hash,'manifest_hash':r[2].manifest_hash,'compiled_tournament_hash':r[4].compiled_hash,'core_invariance':r[5].status.value,'parity':r[7].status.value,'migration_report_hash':r[9].report_hash,'generated_file_count':len(r[3])}
out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding='utf-8');print(out)
