from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import sys

ROOT = find_repository_root(__file__)
sys.path.insert(0, str(ROOT / "src/engine/packages"))
from saed_v4_continual_meta_transfer import run

E = ROOT / "examples/legacy/strategy_factory/saed_v4_25"
A = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_25"
config = json.loads((E / "FULL_REFERENCE_CONFIG.JSON").read_text(encoding="utf-8"))
upstream = json.loads((E / "UPSTREAM_V4_24_DOCUMENTS.JSON").read_text(encoding="utf-8"))
tasks = json.loads((E / "META_TASK_RECORDS.JSON").read_text(encoding="utf-8"))
outputs = run(config, upstream, tasks)
filenames = {
    "upstream_receipt": "GOLDEN_UPSTREAM_RECEIPT.JSON",
    "meta_dataset_summary": "GOLDEN_META_DATASET_SUMMARY.JSON",
    "meta_features": "GOLDEN_META_FEATURES.JSON",
    "drift_report": "GOLDEN_DRIFT_REPORT.JSON",
    "transfer_map": "GOLDEN_TRANSFER_MAP.JSON",
    "adaptations": "GOLDEN_ADAPTATIONS.JSON",
    "regularizations": "GOLDEN_REGULARIZATIONS.JSON",
    "transfer_evaluations": "GOLDEN_TRANSFER_EVALUATIONS.JSON",
    "transfer_report": "GOLDEN_TRANSFER_REPORT.JSON",
    "negative_transfer_guards": "GOLDEN_NEGATIVE_TRANSFER_GUARDS.JSON",
    "continual_calibration_states": "GOLDEN_CONTINUAL_CALIBRATION_STATES.JSON",
    "replay_buffer": "GOLDEN_REPLAY_BUFFER.JSON",
    "recalibration_experiment": "GOLDEN_RECALIBRATION_EXPERIMENT.JSON",
    "trial_ledger": "GOLDEN_TRIAL_LEDGER.JSON",
    "exposure_ledger": "GOLDEN_EXPOSURE_LEDGER.JSON",
    "budget_snapshot": "GOLDEN_BUDGET_SNAPSHOT.JSON",
    "authority_boundary": "GOLDEN_AUTHORITY_BOUNDARY.JSON",
    "certificate": "GOLDEN_CONTINUAL_META_TRANSFER_CERTIFICATE.JSON",
    "handoff": "V4_25_TO_V4_26_HANDOFF.JSON",
    "replay_receipt": "GOLDEN_REPLAY_RECEIPT.JSON",
}
for key, filename in filenames.items():
    expected = json.loads((A / filename).read_text(encoding="utf-8"))
    assert outputs[key] == expected, key
print(f"V4-25 golden reproduction passed: {len(filenames)} exact artifacts")
