from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_generative_path_stress_lab.service import run_reference
load=lambda p:json.loads(p.read_text())
ex=ROOT/'lab/11_strategy_factory/examples/saed_v4_22';art=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22'
out=run_reference(load(ex/'FULL_REFERENCE_CONFIG.JSON'),load(ex/'UPSTREAM_V4_21_DOCUMENTS.JSON'),load(ex/'REAL_REFERENCE_PATHS.JSON'),load(ex/'CANDIDATE_POLICY.JSON'),{'passed':True})
checks={'GOLDEN_GENERATIVE_STRESS_CERTIFICATE':out['certificate'],'GOLDEN_REPLAY_RECEIPT':out['replay_receipt'],'V4_22_TO_V4_23_HANDOFF':out['handoff'],'GOLDEN_FIDELITY_REPORT':out['fidelity_report'],'GOLDEN_BUDGET_SNAPSHOT':out['budget_snapshot']}
for name,obj in checks.items():assert obj==load(art/f'{name}.JSON'),name
print(json.dumps({'passed':True,'reproduced':sorted(checks),'reference_run_hash':out['reference_run_hash']},sort_keys=True))
