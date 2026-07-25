from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_decision_focused_treatment_selection.service import select_treatments
from saed_v4_decision_focused_treatment_selection.canonical import content_hash
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_20';ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_20'
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
r=select_treatments(load(EX/'FULL_REFERENCE_CONFIG.JSON'),load(EX/'GOLDEN_CONTEXT.JSON'),load(EX/'GOLDEN_OUTCOMES.JSON'),load(EX/'GOLDEN_PROOFS.JSON'),load(EX/'UPSTREAM_HASHES.JSON'))
assert r['certificate']==load(ART/'GOLDEN_SELECTION_CERTIFICATE.JSON')
assert r['ranking']==load(ART/'GOLDEN_TREATMENT_RANKING.JSON')['rows']
assert r['decision']==load(ART/'GOLDEN_SET_VALUED_DECISION.JSON')
assert r['mask']==load(ART/'GOLDEN_ACTION_MASK.JSON')
assert r['baseline_report']==load(ART/'GOLDEN_BASELINE_REPORT.JSON')
print('SAED V4-20 deterministic golden reproduction passed: '+r['certificate']['certificate_hash'])
