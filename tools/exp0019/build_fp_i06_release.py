#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import csv
import json
import zipfile

STATUS = 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i06'
META = {'EXP0019_FP_I06_FILE_INDEX.txt', 'EXP0019_FP_I06_FILE_HASHES.sha256', 'EXP0019_FP_I06_PATCH_MANIFEST.json'}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def owned(root: Path) -> list[Path]:
    paths: set[Path] = set()
    dirs = [
        STATUS,
        'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i06',
        'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I06',
    ]
    for rel in dirs:
        base = root / rel
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts and p.suffix != '.pyc':
                    paths.add(p)
    for p in (root / 'docs/obsidian_deep/01_concepts').glob('FP-I06_*.md'):
        paths.add(p)
    specific = [
        'README_EXP0019_FP_I06_RELATION_ENGINE.md',
        'INSTALL_EXP0019_FP_I06_RELATION_ENGINE.md',
        'COMMIT_MESSAGE.md',
        'EXP0019_FP_I06_QA_REPORT.json',
        'EXP0019_FP_I06_FILE_INDEX.txt',
        'EXP0019_FP_I06_FILE_HASHES.sha256',
        'EXP0019_FP_I06_PATCH_MANIFEST.json',
        'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I06_RELATION_COMPILER_HUNT_FACTS_FIRST-SWEEP_CLASSIFICATION_AND_CANDIDATES.md',
        'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationDiagnostic.mq5',
        'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I06_RelationSelfTest.mq5',
        'tools/exp0019/check_fp_i06_boundaries.py',
        'tools/exp0019/check_fp_i06_mql5_static.py',
        'tools/exp0019/generate_fp_i06_vectors.py',
        'tools/exp0019/validate_fp_i06_delivery.py',
        'tools/exp0019/build_fp_i06_release.py',
    ]
    for rel in specific:
        p = root / rel
        if p.is_file():
            paths.add(p)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--zip')
    args = parser.parse_args()
    root = Path(args.root).resolve()

    for name in META:
        p = root / name
        if not p.exists():
            p.write_text('', encoding='utf-8')

    inventory = root / STATUS / 'artifacts/FP_I06_ARTIFACT_INVENTORY.csv'
    inventory.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in owned(root):
        if p.name in META or p == inventory:
            continue
        rows.append({'path': p.relative_to(root).as_posix(), 'sha256': digest(p), 'size_bytes': p.stat().st_size})
    with inventory.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['path', 'sha256', 'size_bytes'])
        writer.writeheader()
        writer.writerows(rows)

    final = owned(root)
    manifest = {
        'patch_id': 'EXP0019-FP-I06-RELATION-HUNT-ENGINE',
        'patch_version': '1.0.0',
        'phase': 'FP-I06',
        'created_at_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'file_count': len(final),
        'python_module_count': 17,
        'phase_test_count': 48,
        'cumulative_fp_test_count': 378,
        'previous_context_regression_count': 50,
        'total_executed_test_count': 428,
        'public_schema_count': 15,
        'public_contract_count': 15,
        'reason_code_count': 70,
        'relation_registry_count': 7,
        'supported_relation_count': 6,
        'mql5_include_count': 12,
        'delivery_doc_count': 48,
        'atomic_concept_count': 7,
        'conformance_check_count': 6,
        'metaeditor_compile_status': 'pending_local_windows',
        'runtime_authority': 'NONE',
        'next_phase': 'FP-I07 Host-Candle Confirmation, Strict Session Deadline, Invalidation, and Lifecycle',
    }
    (root / 'EXP0019_FP_I06_FILE_INDEX.txt').write_text(
        '\n'.join(p.relative_to(root).as_posix() for p in final) + '\n', encoding='utf-8'
    )
    (root / 'EXP0019_FP_I06_PATCH_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )

    final = owned(root)
    (root / 'EXP0019_FP_I06_FILE_HASHES.sha256').write_text(
        '\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in final if p.name != 'EXP0019_FP_I06_FILE_HASHES.sha256') + '\n',
        encoding='utf-8',
    )
    final = owned(root)
    manifest['file_count'] = len(final)
    (root / 'EXP0019_FP_I06_PATCH_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )

    if args.zip:
        target = Path(args.zip).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for p in final:
                info = zipfile.ZipInfo(p.relative_to(root).as_posix(), (2026, 7, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, p.read_bytes())
        print(f'{target} files={len(final)} sha256={digest(target)}')
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
