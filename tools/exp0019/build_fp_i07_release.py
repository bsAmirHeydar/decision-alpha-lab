#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import csv
import json
import zipfile

STATUS = 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i07'
META = {'releases/history/exp0019/indexes/EXP0019_FP_I07_FILE_INDEX.txt', 'releases/history/exp0019/hashes/EXP0019_FP_I07_FILE_HASHES.sha256', 'releases/history/exp0019/manifests/EXP0019_FP_I07_PATCH_MANIFEST.json'}

def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()

def owned(root: Path) -> list[Path]:
    paths: set[Path] = set()
    for rel in (
        STATUS,
        'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i07',
        'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07',
    ):
        base = root / rel
        if base.exists():
            for path in base.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and '.pytest_cache' not in path.parts and path.suffix != '.pyc':
                    paths.add(path)
    for path in (root / 'docs/obsidian_deep/01_concepts').glob('FP-I07_*.md'):
        paths.add(path)
    for rel in (
        'releases/history/exp0019/readmes/README_EXP0019_FP_I07_CONFIRMATION_ENGINE.md',
        'releases/history/exp0019/installers/INSTALL_EXP0019_FP_I07_CONFIRMATION_ENGINE.md',
        'COMMIT_MESSAGE.md',
        'releases/history/exp0019/reports/EXP0019_FP_I07_QA_REPORT.json',
        'releases/history/exp0019/indexes/EXP0019_FP_I07_FILE_INDEX.txt',
        'releases/history/exp0019/hashes/EXP0019_FP_I07_FILE_HASHES.sha256',
        'releases/history/exp0019/manifests/EXP0019_FP_I07_PATCH_MANIFEST.json',
        'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I07_ConfirmationDiagnostic.mq5',
        'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I07_ConfirmationSelfTest.mq5',
        'tools/exp0019/check_fp_i07_boundaries.py',
        'tools/exp0019/check_fp_i07_mql5_static.py',
        'tools/exp0019/validate_fp_i07_delivery.py',
        'tools/exp0019/build_fp_i07_release.py',
    ):
        path = root / rel
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())

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

    inventory = root / STATUS / 'artifacts/FP_I07_ARTIFACT_INVENTORY.csv'
    rows = []
    for path in owned(root):
        if path.name in META or path == inventory:
            continue
        rows.append({'path': path.relative_to(root).as_posix(), 'sha256': digest(path), 'size_bytes': path.stat().st_size})
    inventory.parent.mkdir(parents=True, exist_ok=True)
    with inventory.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['path', 'sha256', 'size_bytes'])
        writer.writeheader()
        writer.writerows(rows)

    final = owned(root)
    manifest = {
        'patch_id': 'EXP0019-FP-I07-CONFIRMATION-LIFECYCLE',
        'patch_version': '1.0.0',
        'phase': 'FP-I07',
        'created_at_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'file_count': len(final),
        'python_module_count': 19,
        'phase_test_count': 60,
        'cumulative_fp_test_count': 438,
        'previous_context_regression_count': 50,
        'total_executed_test_count': 488,
        'public_schema_count': 15,
        'public_contract_count': 11,
        'reason_code_count': 19,
        'outcome_count': 7,
        'mql5_include_count': 14,
        'delivery_doc_count': 49,
        'atomic_concept_count': 7,
        'metaeditor_compile_status': 'pending_local_windows',
        'runtime_authority': 'NONE',
        'next_phase': 'FP-I08 Weekly WW Context Engine, Recency, Neutralization, and Active Gate',
    }
    (root / 'releases/history/exp0019/indexes/EXP0019_FP_I07_FILE_INDEX.txt').write_text(
        '\n'.join(path.relative_to(root).as_posix() for path in final) + '\n', encoding='utf-8'
    )
    (root / 'releases/history/exp0019/manifests/EXP0019_FP_I07_PATCH_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )

    final = owned(root)
    (root / 'releases/history/exp0019/hashes/EXP0019_FP_I07_FILE_HASHES.sha256').write_text(
        '\n'.join(f'{digest(path)}  {path.relative_to(root).as_posix()}' for path in final if path.name != 'releases/history/exp0019/hashes/EXP0019_FP_I07_FILE_HASHES.sha256') + '\n',
        encoding='utf-8',
    )
    final = owned(root)
    manifest['file_count'] = len(final)
    (root / 'releases/history/exp0019/manifests/EXP0019_FP_I07_PATCH_MANIFEST.json').write_text(
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
