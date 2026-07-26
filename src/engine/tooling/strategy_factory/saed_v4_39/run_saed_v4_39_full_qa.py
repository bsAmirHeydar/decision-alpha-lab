from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,subprocess,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
cmds=[[sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_39_prospective_shadow_micro_live'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_39/validate_schemas.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_39/validate_mql5_static.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_39/validate_docs.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_39/validate_authority.py']]
for c in cmds:subprocess.run(c,cwd=ROOT,check=True)
report={'phase':'SAED_V4_39','passed':True,'python_tests':'passed','closed_schema_pairs':len(list((ROOT/'schemas/legacy/strategy_factory/saed_v4_39').glob('*.schema.json'))),'phase_documents':len(list((ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_39').glob('*.md'))),'atomic_documents':len(list((ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_39').glob('*.md'))),'mql5_static_files':len(list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_39').glob('*')))+len(list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_39').glob('*'))),'actual_metaeditor_compile':'pending_external','actual_terminal_replay':'pending_external','actual_broker_qualification':'pending_external','actual_prospective_paper':'pending_external','actual_prospective_shadow':'pending_external','micro_live_authorized':False,'production_authorized':False}
(ROOT/'releases/history/saed/reports/SAED_V4_39_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
status={'phase':'SAED_V4_39','status':'accepted_reference_external_gates_open','qa_passed':True,'reference_paper_passed':True,'reference_shadow_passed':True,'actual_micro_live_authorized':False,'production_authorized':False}
(ROOT/'releases/history/strategy_factory/program/status/SAED_V4_39.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2))
