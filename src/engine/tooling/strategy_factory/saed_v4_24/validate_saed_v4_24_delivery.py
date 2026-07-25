from tools.repository_paths import find_repository_root
from pathlib import Path
import csv
import hashlib
import json

ROOT = find_repository_root(__file__)
INDEX = ROOT / 'releases/history/saed/indexes/SAED_V4_24_FILE_INDEX.txt'
LEDGER = ROOT / 'releases/history/saed/hashes/SAED_V4_24_FILE_HASHES.sha256'
MANIFEST = ROOT / 'releases/history/saed/manifests/SAED_V4_24_PATCH_MANIFEST.json'
QA = ROOT / 'releases/history/saed/reports/SAED_V4_24_QA_REPORT.json'
INVENTORY = ROOT / 'releases/history/saed/inventories/SAED_V4_24_ARTIFACT_INVENTORY.csv'
required = [INDEX, LEDGER, MANIFEST, QA, INVENTORY]
assert all(path.is_file() for path in required)

paths = [line.strip() for line in INDEX.read_text(encoding='utf-8').splitlines() if line.strip()]
assert paths == sorted(paths)
assert len(paths) == len(set(paths))
assert not [path for path in paths if not (ROOT / path).is_file()]
assert not [path for path in paths if '__pycache__' in path or path.endswith('.pyc')]

expected = {}
for line in LEDGER.read_text(encoding='utf-8').splitlines():
    if line.strip():
        digest, path = line.split('  ', 1)
        expected[path] = digest
assert set(expected) == set(paths) - {'releases/history/saed/hashes/SAED_V4_24_FILE_HASHES.sha256'}
for path, digest in expected.items():
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    assert actual == digest, path

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
qa = json.loads(QA.read_text(encoding='utf-8'))
status = json.loads((ROOT / 'releases/history/strategy_factory/program/status/SAED_V4_24.json').read_text(encoding='utf-8'))
assert manifest['phase'] == 'SAED_V4_24' and manifest['version'] == '1.0.0'
assert manifest['file_count'] == len(paths) and manifest['hash_count'] == len(expected)
assert manifest['qa_passed'] and qa['passed'] and status['qa_passed']
assert status['python_tests'] >= 269 and status['closed_schemas'] >= 34
assert status['obsidian_notes'] >= 247 and status['mql5_static_files'] >= 22
assert status['metaeditor_compile'] == 'pending_local_windows'
assert status['real_alpha'] is False and status['promotion_authority'] is False
assert status['runtime_executable'] is False and status['risk_allocation_authority'] is False
assert status['execution_authority'] is False and status['production_authorization'] is False

A = ROOT / 'releases/history/strategy_factory/artifacts/saed_v4_24'
certificate = json.loads((A / 'GOLDEN_CONFORMAL_OOD_SELECTIVE_CERTIFICATE.JSON').read_text(encoding='utf-8'))
assert certificate['accepted_for_conformal_ood_selective_research']
assert all(certificate['gates'].values())
assert certificate['selection_is_research_only']
assert certificate['promotion_authority'] is False
assert certificate['runtime_executable'] is False
assert certificate['risk_allocation_authority'] is False
assert certificate['execution_authority'] is False
assert certificate['production_authority'] is False
assert certificate['real_alpha_claim'] is False
assert certificate['prospective_success_claim'] is False
assert not any(certificate['authority_boundary']['authority'].values())

handoff = json.loads((A / 'V4_24_TO_V4_25_HANDOFF.JSON').read_text(encoding='utf-8'))
assert handoff['next_phase'] == 'SAED_V4_25'
assert all(handoff['entry_gates'].values())
assert handoff['research_only'] and not any(handoff['authority'].values())
assert set(handoff['allowed_next_work']) == {
    'continual_calibration_research', 'meta_learning_dataset_design',
    'transfer_shift_mapping', 'drift_segment_taxonomy',
    'safe_recalibration_experiments'
}

exposure = json.loads((A / 'GOLDEN_EXPOSURE_LEDGER.JSON').read_text(encoding='utf-8'))
assert exposure['complete']
assert exposure['hidden_evaluation_queries'] == 0
assert exposure['protected_evidence_exposures'] == 0
assert exposure['runtime_compilations'] == 0
assert exposure['order_submissions'] == 0
assert exposure['online_policy_mutations'] == 0

budget = json.loads((A / 'GOLDEN_BUDGET_SNAPSHOT.JSON').read_text(encoding='utf-8'))
assert budget['complete']
assert budget['counts']['records'] == 180
assert budget['counts']['conformal_fits'] == 1
assert budget['counts']['ood_fits'] == 1
assert budget['counts']['selective_evaluations'] == 60
assert budget['counts']['bootstrap_draws'] == 3000
assert budget['counts']['hidden_evaluation_queries'] == 0
assert budget['counts']['protected_evidence_exposures'] == 0
assert budget['counts']['runtime_compilations'] == 0
assert budget['counts']['order_submissions'] == 0

decisions = json.loads((A / 'GOLDEN_SELECTIVE_DECISIONS.JSON').read_text(encoding='utf-8'))
assert len(decisions) == 60
assert all(row['uses_realized_outcome'] is False for row in decisions)
assert all(row['promotion_eligible'] is False and row['runtime_executable'] is False for row in decisions)
assert all(row['selected_action'] == row['candidate_action'] if row['accepted'] else row['selected_action'] == 'skip' for row in decisions)

leakage = json.loads((A / 'KNOWN_TIME_LEAKAGE_REVIEW.JSON').read_text(encoding='utf-8'))
assert leakage['passed']
assert leakage['decision_artifact_uses_realized_outcome'] is False
assert leakage['outcome_mutation_changes_decisions'] is False
assert leakage['outcome_mutation_changes_retrospective_risk'] is True
assert leakage['future_suffix_queries'] == 0 and leakage['protected_evidence_queries'] == 0

replay = json.loads((A / 'GOLDEN_REPLAY_RECEIPT.JSON').read_text(encoding='utf-8'))
assert replay['deterministic'] and replay['network_access'] is False
assert replay['future_suffix_queries'] == 0 and replay['protected_evidence_queries'] == 0
assert replay['runtime_compilations'] == 0 and replay['order_submissions'] == 0

with INVENTORY.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == len(paths)
assert {row['path'] for row in rows} == set(paths)
print(f'V4-24 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
