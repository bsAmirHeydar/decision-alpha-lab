from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_robust_optimization_regret.service import run_reference
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
e=ROOT/'lab/11_strategy_factory/examples/saed_v4_21';a=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_21'
r=run_reference(load(e/'FULL_REFERENCE_CONFIG.JSON'),load(e/'UPSTREAM_V4_20_DOCUMENTS.JSON'),load(e/'GOLDEN_CANDIDATE_SCORE_TABLE.JSON'))
checks={'GOLDEN_SCENARIO_SET.JSON':'scenario_set','GOLDEN_AMBIGUITY_SET.JSON':'ambiguity_set','GOLDEN_ALLOCATION_UNIVERSE.JSON':'allocation_universe','GOLDEN_ROBUST_OPTIMIZATION_REPORT.JSON':'optimization_report','GOLDEN_ADVERSARY_REPORT.JSON':'adversary_report','GOLDEN_STABILITY_REPORT.JSON':'stability_report','GOLDEN_RADIUS_SENSITIVITY.JSON':'radius_sensitivity','GOLDEN_BUDGET_SNAPSHOT.JSON':'budget_snapshot','GOLDEN_ROBUST_CERTIFICATE.JSON':'certificate','GOLDEN_REPLAY_RECEIPT.JSON':'replay_receipt'}
for fn,k in checks.items():assert load(a/fn)==r[k],fn
print(json.dumps({'passed':True,'golden_artifacts':len(checks),'reference_run_hash':r['reference_run_hash']},sort_keys=True))
