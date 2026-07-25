from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);p=ROOT/'releases/history/strategy_factory/program/status/SAED_V4_22.json';x=json.loads(p.read_text())
required={'phase','title','version','status','evidence_scope','claim_ceiling','python_tests','closed_schemas','obsidian_notes','mql5_static_files','metaeditor_compile','runtime_parity','real_alpha','production_authorization','next_phase','external_blockers'}
assert set(x)==required and x['phase']=='SAED_V4_22' and x['status']=='REFERENCE_IMPLEMENTATION_ACCEPTED' and x['real_alpha'] is False and x['production_authorization'] is False
print(json.dumps({'passed':True,'phase':x['phase'],'status':x['status']},sort_keys=True))
