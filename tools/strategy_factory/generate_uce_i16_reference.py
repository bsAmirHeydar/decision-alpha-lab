#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from strategy_factory_onboarding_v3.golden import golden_run
from strategy_factory_onboarding_v3.canonical import normalize
r=golden_run(ROOT)
out=ROOT/'lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16/reference_generation.json'
payload={'context_spec_hash':r[0].spec_hash,'manifest_hash':r[2].manifest_hash,'compiled_tournament_hash':r[4].compiled_hash,'core_invariance':r[5].status.value,'parity':r[7].status.value,'migration_report_hash':r[9].report_hash,'generated_file_count':len(r[3])}
out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding='utf-8');print(out)
