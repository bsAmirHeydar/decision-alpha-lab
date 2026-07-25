import csv
import json
from collections import Counter

from tools.strategy_factory.lcm.lcm_02.canonical import digest_object


def _rows(root):
    with (root / 'artifacts/artifact_classification_records.csv').open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def test_receipt_is_immutable_and_non_self_referential(classification_root):
    receipt = json.loads((classification_root / 'classification_receipt.json').read_text(encoding='utf-8'))
    assert receipt['receipt_digest'] == digest_object(receipt, 'receipt_digest')
    assert 'output_manifest_digest' not in receipt
    assert receipt['source_move_performed'] is False
    assert receipt['source_delete_performed'] is False
    assert receipt['semantic_refactor_performed'] is False
    assert receipt['merge_performed'] is False
    assert receipt['cutover_performed'] is False


def test_manifest_includes_final_receipt(classification_root):
    manifest = json.loads((classification_root / 'output_manifest.json').read_text(encoding='utf-8'))
    artifacts = {a['path']: a for a in manifest['artifacts']}
    assert 'classification_receipt.json' in artifacts


def test_every_security_sensitive_record_has_security_reviewer(classification_root):
    rows = _rows(classification_root)
    secured = [r for r in rows if r['security_sensitive'] == 'true']
    assert secured
    assert all(r['security_reviewer_role'] == 'SECURITY_REVIEWER' for r in secured)
    assert all(r['primary_disposition'] == 'SECURITY_RESTRICTED' for r in secured)


def test_every_active_candidate_is_owned_or_explicitly_blocked(classification_root):
    rows = _rows(classification_root)
    active = [r for r in rows if r['activity_status'] in {'ACTIVE_PLATFORM', 'ACTIVE_RUNTIME_CANDIDATE', 'ACTIVE_RESEARCH'}]
    assert active
    for row in active:
        assert row['semantic_owner_role']
        assert row['code_owner_role']
        assert row['ownership_is_human_approved'] == 'false'
        assert 'OWNER' in row['ownership_blockers'] or 'PENDING' in row['ownership_blockers']


def test_generated_projection_never_canonical(classification_root):
    rows = _rows(classification_root)
    generated = [r for r in rows if r['artifact_role'] == 'GENERATED_PROJECTION']
    assert generated
    assert all(r['canonical_selection_status'] == 'NON_CANONICAL_GENERATED' for r in generated)
    assert all(r['generated_projection_canonical_authority'] == 'false' for r in generated)
    assert all(r['primary_disposition'] != 'KEEP_CANONICAL' for r in generated)


def test_exactly_one_nonempty_primary_disposition(classification_root):
    rows = _rows(classification_root)
    counts = Counter(r['artifact_path'] for r in rows)
    assert all(v == 1 for v in counts.values())
    assert all(r['primary_disposition'] for r in rows)


def test_no_destructive_or_runtime_authority(classification_root):
    rows = _rows(classification_root)
    denied = [
        'source_move_authorized', 'source_delete_authorized', 'semantic_refactor_authorized',
        'merge_authorized', 'cutover_authorized', 'runtime_authorized',
        'live_order_authorized', 'capital_authorized',
    ]
    assert all(all(r[k] == 'false' for k in denied) for r in rows)


def test_unresolved_queue_counts_match_files(classification_root):
    summary = json.loads((classification_root / 'unresolved/unresolved_summary.json').read_text(encoding='utf-8'))
    for queue_name, expected in summary['queue_counts'].items():
        path = classification_root / f'unresolved/{queue_name}_queue.jsonl'
        actual = sum(1 for line in path.read_text(encoding='utf-8').splitlines() if line.strip())
        assert actual == expected
