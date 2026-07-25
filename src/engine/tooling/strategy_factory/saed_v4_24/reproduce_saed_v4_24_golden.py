from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import sys
ROOT = find_repository_root(__file__)
sys.path.insert(0, str(ROOT / 'src/engine/packages'))
from saed_v4_conformal_ood_selective_control.service import run
EX = ROOT / 'examples/legacy/strategy_factory/saed_v4_24'
ART = ROOT / 'releases/history/strategy_factory/artifacts/saed_v4_24'
load = lambda path: json.loads(Path(path).read_text())
outputs = run(load(EX / 'FULL_REFERENCE_CONFIG.JSON'), load(EX / 'UPSTREAM_V4_23_DOCUMENTS.JSON'), load(EX / 'CALIBRATION_SELECTION_DRIFT_RECORDS.JSON'))
files = {
    'upstream_receipt': 'GOLDEN_UPSTREAM_RECEIPT.JSON', 'dataset_summary': 'GOLDEN_DATASET_SUMMARY.JSON',
    'conformal_calibrator': 'GOLDEN_CONFORMAL_CALIBRATOR.JSON', 'conformal_bounds': 'GOLDEN_CONFORMAL_BOUNDS.JSON',
    'retrospective_coverage': 'GOLDEN_RETROSPECTIVE_COVERAGE.JSON', 'ood_detector': 'GOLDEN_OOD_DETECTOR.JSON',
    'selection_ood_evaluations': 'GOLDEN_SELECTION_OOD_EVALUATIONS.JSON', 'selective_decisions': 'GOLDEN_SELECTIVE_DECISIONS.JSON',
    'coverage_risk_frontier': 'GOLDEN_COVERAGE_RISK_FRONTIER.JSON', 'abstention_policy': 'GOLDEN_ABSTENTION_POLICY.JSON',
    'drift_ood_evaluations': 'GOLDEN_DRIFT_OOD_EVALUATIONS.JSON', 'drift_report': 'GOLDEN_DRIFT_REPORT.JSON',
    'trial_ledger': 'GOLDEN_TRIAL_LEDGER.JSON', 'exposure_ledger': 'GOLDEN_EXPOSURE_LEDGER.JSON',
    'budget_snapshot': 'GOLDEN_BUDGET_SNAPSHOT.JSON', 'authority_boundary': 'GOLDEN_AUTHORITY_BOUNDARY.JSON',
    'certificate': 'GOLDEN_CONFORMAL_OOD_SELECTIVE_CERTIFICATE.JSON', 'handoff': 'V4_24_TO_V4_25_HANDOFF.JSON',
    'replay_receipt': 'GOLDEN_REPLAY_RECEIPT.JSON',
}
for key, name in files.items(): assert outputs[key] == load(ART / name), name
print(f'V4-24 golden reproduction passed: {len(files)} exact artifacts; replay {outputs["replay_receipt"]["replay_hash"]}')
