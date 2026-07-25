from __future__ import annotations

import json
from pathlib import Path

from tools.consolidation.uc03p1.apply import AhoRewriter, KEEP_ROOT, apply, sha256


def _write_release(repo: Path, rows: list[dict], static_paths: list[str]) -> None:
    release = repo / 'releases/unified_consolidation/uc03/part1'
    release.mkdir(parents=True, exist_ok=True)
    (release / 'ROOT_RELOCATION_MAP.jsonl').write_text(
        '\n'.join(json.dumps(row) for row in rows) + '\n', encoding='utf-8'
    )
    (release / 'STATIC_PATCH_FILE_INDEX.txt').write_text(
        '\n'.join(static_paths) + '\n', encoding='utf-8'
    )


def test_rewriter_replaces_exact_artifact_name() -> None:
    r = AhoRewriter({'README_OLD.md': 'releases/history/demo/readmes/README_OLD.md'})
    updated, count = r.rewrite('See README_OLD.md now.')
    assert count == 1
    assert updated == 'See releases/history/demo/readmes/README_OLD.md now.'


def test_rewriter_does_not_duplicate_canonical_destination() -> None:
    destination = 'releases/history/demo/readmes/README_OLD.md'
    r = AhoRewriter({'README_OLD.md': destination})
    updated, count = r.rewrite(destination)
    assert count == 0
    assert updated == destination


def test_apply_moves_bytes_preserves_history_and_rewrites_active_reference(tmp_path: Path) -> None:
    for name in KEEP_ROOT:
        (tmp_path / name).write_text(name, encoding='utf-8')
    source = tmp_path / 'README_OLD.md'
    source.write_bytes(b'legacy bytes\r\n')
    active = tmp_path / 'tools/reference.txt'
    active.parent.mkdir(parents=True)
    active.write_text('README_OLD.md', encoding='utf-8')
    static = tmp_path / 'tools/consolidation/uc03p1/apply.py'
    static.parent.mkdir(parents=True)
    static.write_text('# static', encoding='utf-8')
    row = {
        'source': 'README_OLD.md',
        'destination': 'releases/history/demo/readmes/README_OLD.md',
        'sha256': sha256(source),
        'program': 'demo',
        'artifact_type': 'readmes',
    }
    _write_release(tmp_path, [row], ['tools/consolidation/uc03p1/apply.py'])
    result = apply(tmp_path)
    destination = tmp_path / row['destination']
    assert result['moved_count'] == 1
    assert not source.exists()
    assert destination.read_bytes() == b'legacy bytes\r\n'
    assert active.read_text(encoding='utf-8') == row['destination']
    assert json.loads((tmp_path / 'registry/consolidation/uc03/part1/part1_exit_decision.json').read_text())['uc03_part2_authorized'] is True


def test_historical_archive_is_not_rewritten(tmp_path: Path) -> None:
    for name in KEEP_ROOT:
        (tmp_path / name).write_text(name, encoding='utf-8')
    source = tmp_path / 'README_OLD.md'
    source.write_text('README_OLD.md', encoding='utf-8')
    static = tmp_path / 'tools/consolidation/uc03p1/apply.py'
    static.parent.mkdir(parents=True)
    static.write_text('# static', encoding='utf-8')
    row = {
        'source': 'README_OLD.md',
        'destination': 'releases/history/demo/readmes/README_OLD.md',
        'sha256': sha256(source),
        'program': 'demo',
        'artifact_type': 'readmes',
    }
    _write_release(tmp_path, [row], ['tools/consolidation/uc03p1/apply.py'])
    apply(tmp_path)
    assert (tmp_path / row['destination']).read_text(encoding='utf-8') == 'README_OLD.md'


def test_generated_index_contains_old_new_modified_and_receipts(tmp_path: Path) -> None:
    for name in KEEP_ROOT:
        (tmp_path / name).write_text(name, encoding='utf-8')
    source = tmp_path / 'OLD_FILE.json'
    source.write_text('{}', encoding='utf-8')
    active = tmp_path / 'tools/ref.json'
    active.parent.mkdir(parents=True)
    active.write_text('{"path":"OLD_FILE.json"}', encoding='utf-8')
    static = tmp_path / 'tools/consolidation/uc03p1/apply.py'
    static.parent.mkdir(parents=True)
    static.write_text('# static', encoding='utf-8')
    row = {
        'source': 'OLD_FILE.json',
        'destination': 'releases/history/demo/metadata/OLD_FILE.json',
        'sha256': sha256(source),
        'program': 'demo',
        'artifact_type': 'metadata',
    }
    _write_release(tmp_path, [row], ['tools/consolidation/uc03p1/apply.py'])
    apply(tmp_path)
    index = set((tmp_path / 'releases/unified_consolidation/uc03/part1/PATCH_FILE_INDEX.txt').read_text().splitlines())
    assert 'OLD_FILE.json' in index
    assert row['destination'] in index
    assert 'tools/ref.json' in index
    assert 'registry/consolidation/uc03/part1/root_relocation_receipt.json' in index


def test_resume_preserves_prior_rewrite_paths_in_staging_index(tmp_path: Path) -> None:
    for name in KEEP_ROOT:
        (tmp_path / name).write_text(name, encoding='utf-8')
    source = tmp_path / 'OLD_FILE.json'
    source.write_text('{}', encoding='utf-8')
    active = tmp_path / 'tools/ref.json'
    active.parent.mkdir(parents=True)
    active.write_text('{"path":"OLD_FILE.json"}', encoding='utf-8')
    static = tmp_path / 'tools/consolidation/uc03p1/apply.py'
    static.parent.mkdir(parents=True, exist_ok=True)
    static.write_text('# static', encoding='utf-8')
    row = {
        'source': 'OLD_FILE.json',
        'destination': 'releases/history/demo/metadata/OLD_FILE.json',
        'sha256': sha256(source),
        'program': 'demo',
        'artifact_type': 'metadata',
    }
    _write_release(tmp_path, [row], ['tools/consolidation/uc03p1/apply.py'])
    first = apply(tmp_path)
    assert first['rewrite_file_count'] == 1
    second = apply(tmp_path)
    assert second['rewrite_file_count'] == 1
    index = set((tmp_path / 'releases/unified_consolidation/uc03/part1/PATCH_FILE_INDEX.txt').read_text().splitlines())
    assert 'tools/ref.json' in index
