#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import csv
import json
import zipfile

PHASE = 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i08'
DOCS = 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i08'
PROGRAM = 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program'
META = {
    'EXP0019_FP_I08_FILE_INDEX.txt',
    'EXP0019_FP_I08_FILE_HASHES.sha256',
    'EXP0019_FP_I08_PATCH_MANIFEST.json',
}

def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()

def add_tree(paths: set[Path], base: Path) -> None:
    if not base.exists():
        return
    for path in base.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and '.pytest_cache' not in path.parts and path.suffix != '.pyc':
            paths.add(path)

def owned(root: Path) -> list[Path]:
    paths: set[Path] = set()
    add_tree(paths, root / PHASE)
    add_tree(paths, root / DOCS)
    add_tree(paths, root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I08')
    for path in (root / 'docs/obsidian_deep/01_concepts').glob('FP-I08_*.md'):
        paths.add(path)
    for rel in (
        'README_EXP0019_FP_I08_WEEKLY_ENGINE.md',
        'INSTALL_EXP0019_FP_I08_WEEKLY_ENGINE.md',
        'COMMIT_MESSAGE.md',
        'EXP0019_FP_I08_QA_REPORT.json',
        'EXP0019_FP_I08_FILE_INDEX.txt',
        'EXP0019_FP_I08_FILE_HASHES.sha256',
        'EXP0019_FP_I08_PATCH_MANIFEST.json',
        f'{PROGRAM}/fp_implementation_phase_registry.v1.json',
        f'{PROGRAM}/fp_implementation_task_ledger.v1.csv',
        'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I08_WeeklyDiagnostic.mq5',
        'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I08_WeeklySelfTest.mq5',
        'tools/exp0019/check_fp_i08_boundaries.py',
        'tools/exp0019/check_fp_i08_mql5_static.py',
        'tools/exp0019/validate_fp_i08_delivery.py',
        'tools/exp0019/build_fp_i08_release.py',
    ):
        path = root / rel
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())

def counts(root: Path) -> dict[str, int]:
    return {
        'python_module_count': len(list((root / f'{PHASE}/python/fp_i08_weekly').glob('*.py'))),
        'test_module_count': len(list((root / f'{PHASE}/tests').glob('test_*.py'))),
        'public_schema_count': len(list((root / f'{PHASE}/schemas').glob('*.schema.json'))),
        'mql5_include_count': len(list((root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I08').glob('*.mqh'))),
        'delivery_doc_count': len(list((root / DOCS).rglob('*.md'))),
        'atomic_concept_count': len(list((root / 'docs/obsidian_deep/01_concepts').glob('FP-I08_*.md'))),
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--zip')
    args = parser.parse_args()
    root = Path(args.root).resolve()

    for name in META:
        path = root / name
        if not path.exists():
            path.write_text('', encoding='utf-8')

    inventory = root / PHASE / 'artifacts/FP_I08_ARTIFACT_INVENTORY.csv'
    rows = []
    for path in owned(root):
        if path.name in META or path == inventory:
            continue
        rows.append({
            'path': path.relative_to(root).as_posix(),
            'sha256': digest(path),
            'size_bytes': path.stat().st_size,
        })
    inventory.parent.mkdir(parents=True, exist_ok=True)
    with inventory.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['path', 'sha256', 'size_bytes'])
        writer.writeheader()
        writer.writerows(rows)

    final = owned(root)
    c = counts(root)
    manifest = {
        'patch_id': 'EXP0019-FP-I08-WEEKLY-WW-ENGINE',
        'patch_version': '1.0.0',
        'phase': 'FP-I08',
        'created_at_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'file_count': len(final),
        **c,
        'phase_test_count': 47,
        'available_cumulative_fp_test_count': 420,
        'available_cumulative_scope': 'FP-I02 through FP-I08',
        'reason_code_count': 13,
        'public_contract_count': 15,
        'golden_vector_count': 6,
        'metaeditor_compile_status': 'pending_local_windows',
        'runtime_authority': 'NONE',
        'clean_baseline_patch': 'pass',
        'upstream_regression_note': 'FP-I00/FP-I01 pinned assets and EXP0018 Daye tree are absent from supplied base archive',
        'next_phase': 'FP-I09 Signal Ledger, Deduplication, Pair-Session Arbitration, Checkpoints, and Restart',
    }
    (root / 'EXP0019_FP_I08_FILE_INDEX.txt').write_text(
        '\n'.join(path.relative_to(root).as_posix() for path in final) + '\n', encoding='utf-8'
    )
    (root / 'EXP0019_FP_I08_PATCH_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )

    final = owned(root)
    (root / 'EXP0019_FP_I08_FILE_HASHES.sha256').write_text(
        '\n'.join(
            f'{digest(path)}  {path.relative_to(root).as_posix()}'
            for path in final
            if path.name != 'EXP0019_FP_I08_FILE_HASHES.sha256'
        ) + '\n',
        encoding='utf-8',
    )
    final = owned(root)
    manifest['file_count'] = len(final)
    (root / 'EXP0019_FP_I08_PATCH_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )

    if args.zip:
        target = Path(args.zip).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in final:
                info = zipfile.ZipInfo(path.relative_to(root).as_posix(), (2026, 7, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())
        print(f'{target} files={len(final)} sha256={digest(target)}')
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
