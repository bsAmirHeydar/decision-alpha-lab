from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,subprocess,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
cmds=[[sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_40_context_fleet_scaleout'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_40/validate_schemas.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_40/validate_mql5_static.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_40/validate_docs.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_40/validate_authority.py']]
for c in cmds:subprocess.run(c,cwd=ROOT,check=True)
report={'phase':'SAED_V4_40','passed':True,'python_tests':'passed','closed_schema_pairs':len(list((ROOT/'schemas/legacy/strategy_factory/saed_v4_40').glob('*.schema.json'))),'phase_documents':len(list((ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_40').glob('*.md'))),'atomic_documents':len(list((ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_40').glob('*.md'))),'mql5_static_files':len(list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_40').glob('*')))+len(list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_40').glob('*'))),'reference_context_cells':128,'actual_metaeditor_compile_matrix':'pending_external','actual_multi_terminal_replay':'pending_external','actual_hundred_context_soak':'pending_external','actual_failure_domain_failover':'pending_external','actual_broker_fleet_reconciliation':'pending_external','capital_activation_allowed':False,'production_authorized':False}
(ROOT/'releases/history/saed/reports/SAED_V4_40_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
status={'phase':'SAED_V4_40','status':'accepted_reference_external_gates_open','qa_passed':True,'reference_fleet_scaleout_passed':True,'actual_scale_soak_passed':False,'production_authorized':False}
(ROOT/'releases/history/strategy_factory/program/status/SAED_V4_40.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2))
