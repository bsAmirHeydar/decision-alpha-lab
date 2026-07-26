#!/usr/bin/env python3
"""Build deterministic UCE-I10 patch metadata and optional ZIP from owned files."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import zipfile

SCHEMAS = (
    'deep_algorithm_descriptor','view_tensor_spec','sequence_window_spec','sequence_artifact',
    'raster_spec','raster_artifact','pixel_audit_report','graph_spec','graph_artifact',
    'regime_novelty_prediction','fusion_prediction','deep_admission_evidence',
    'seed_run_observation','view_ablation_observation','export_assessment',
    'deep_qualification_report','distillation_report','quantization_report',
    'dependency_probe','adapter_plan','transfer_boundary','future_perturbation_audit',
    'deterministic_replay_audit','deep_registry_snapshot',
)


def owned_paths(root: Path) -> list[Path]:
    paths: set[Path] = set()
    dirs = (
        'src/engine/packages/strategy_factory_deep_views_v3',
        'tests/legacy/strategy_factory/v1/phase_uce_i10_deep_views',
        'examples/legacy/strategy_factory/uce_i10',
        'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i10',
        'mql5/Include/AlphaLab/StrategyFactory/DeepViews',
    )
    for relative in dirs:
        for path in (root / relative).rglob('*'):
            if path.is_file() and path.name not in {'.DS_Store'} and path.suffix != '.pyc' and '__pycache__' not in path.parts:
                paths.add(path)
    specific = [
        'releases/history/strategy_factory_ucee/readmes/README_STRATEGY_FACTORY_UCEE_I10_IMPLEMENTATION.md','releases/history/strategy_factory_ucee/installers/INSTALL_STRATEGY_FACTORY_UCEE_I10_IMPLEMENTATION.md','releases/history/ucee/scripts/EXPAND_REMOVE_UCEE_I10_PATCH.ps1','COMMIT_MESSAGE.md',
        'releases/history/ucee/manifests/UCEE_I10_PATCH_MANIFEST.json','releases/history/ucee/reports/UCEE_I10_QA_REPORT.json','releases/history/ucee/indexes/UCEE_I10_FILE_INDEX.txt','releases/history/ucee/hashes/UCEE_I10_FILE_HASHES.sha256',
        'docs/history/systems/ucee/implementation_program/phases/UCE_I10_DEEP_MULTI_VIEW_GRAPH_AND_REGIME_PACK.md',
        'mql5/Experts/StrategyFactory/UCE_I10_DeepViewsDiagnostic.mq5',
        'mql5/Tests/Experts/StrategyFactory/UCE_I10_DeepViewsSelfTest.mq5',
        'mql5/Tests/Experts/StrategyFactory/UCE_I10_CausalitySafetySelfTest.mq5',
        'tests/fixtures/legacy/strategy_factory/v3/uce_i10_deep_view_conformance_vectors.json',
        'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10.json',
        'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10_HANDOFF_TO_UCE_I11.json',
        'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ACCEPTANCE_EVIDENCE.json',
        'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ARTIFACT_INVENTORY.csv',
        'src/engine/tooling/strategy_factory/check_uce_i10_boundaries.py','src/engine/tooling/strategy_factory/check_uce_i10_mql5_static.py',
        'src/engine/tooling/strategy_factory/compile_uce_i10_deep_views.ps1','src/engine/tooling/strategy_factory/generate_uce_i10_vectors.py',
        'src/engine/tooling/strategy_factory/run_uce_i10_tests.ps1','src/engine/tooling/strategy_factory/validate_uce_i10_delivery.py',
        'src/engine/tooling/strategy_factory/apply_uce_i10_patch.ps1','src/engine/tooling/strategy_factory/build_uce_i10_release.py',
    ]
    specific += [f'schemas/legacy/strategy_factory/v3/{name}.schema.json' for name in SCHEMAS]
    concept_dir = root / 'docs/history/obsidian/deep/01_concepts'
    for path in concept_dir.glob('UCE-I10*.md'):
        paths.add(path)
    for relative in specific:
        path = root / relative
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--zip', dest='zip_path')
    parser.add_argument('--phase-tests', type=int, required=True)
    parser.add_argument('--cumulative-tests', type=int, required=True)
    parser.add_argument('--engineering-checks', type=int, default=4)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

    # Build inventory without self-referential root index/hash/manifest files.
    paths = [p for p in owned_paths(root) if p.name not in {'releases/history/ucee/indexes/UCEE_I10_FILE_INDEX.txt','releases/history/ucee/hashes/UCEE_I10_FILE_HASHES.sha256','releases/history/ucee/manifests/UCEE_I10_PATCH_MANIFEST.json','UCE_I10_ARTIFACT_INVENTORY.csv'}]
    rows = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        rows.append({'path': rel, 'sha256': digest(path), 'size_bytes': path.stat().st_size})

    inventory = root / 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ARTIFACT_INVENTORY.csv'
    inventory.parent.mkdir(parents=True, exist_ok=True)
    with inventory.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=('path','sha256','size_bytes'))
        writer.writeheader(); writer.writerows(rows)

    # Recompute list including the freshly generated inventory, still excluding self-referential release indexes.
    paths = [p for p in owned_paths(root) if p.name not in {'releases/history/ucee/indexes/UCEE_I10_FILE_INDEX.txt','releases/history/ucee/hashes/UCEE_I10_FILE_HASHES.sha256','releases/history/ucee/manifests/UCEE_I10_PATCH_MANIFEST.json'}]
    entries = [(p.relative_to(root).as_posix(), digest(p), p.stat().st_size) for p in paths]
    (root / 'releases/history/ucee/indexes/UCEE_I10_FILE_INDEX.txt').write_text('\n'.join(rel for rel,_,_ in entries)+'\n', encoding='utf-8')
    (root / 'releases/history/ucee/hashes/UCEE_I10_FILE_HASHES.sha256').write_text('\n'.join(f'{h}  {rel}' for rel,h,_ in entries)+'\n', encoding='utf-8')

    docs = list((root / 'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i10').rglob('*.md'))
    schemas = [root / f'schemas/legacy/strategy_factory/v3/{name}.schema.json' for name in SCHEMAS]
    manifest = {
        'patch_id':'decision-alpha-lab-ucee-i10-deep-multi-view-graph-regime-pack',
        'patch_version':'1.1.0','phase_id':'UCE-I10','created_at_utc':generated,
        'title':'Deep Sequence, Deterministic Raster, Graph, Regime, Multi-View Fusion, and Qualification Pack',
        'authority_boundary':'offline research and runtime-neutral contracts; no live order authority',
        'catalog_algorithm_count':17,'native_algorithm_count':10,'trainer_plugin_count':5,
        'schema_count':len(schemas),'documentation_note_count':len(docs),
        'phase_test_count':args.phase_tests,'cumulative_ucee_test_count':args.cumulative_tests,
        'engineering_policy_check_count':args.engineering_checks,
        'metaeditor_compile_status':'pending_local_windows',
        'file_count':len(entries)+3,
        'next_phase':'UCE-I11 Experiment DAG, Search, and Budgeting',
        'file_index':'releases/history/ucee/indexes/UCEE_I10_FILE_INDEX.txt','file_hashes':'releases/history/ucee/hashes/UCEE_I10_FILE_HASHES.sha256',
    }
    (root / 'releases/history/ucee/manifests/UCEE_I10_PATCH_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n', encoding='utf-8')

    if args.zip_path:
        target = Path(args.zip_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        release_paths = owned_paths(root)
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in release_paths:
                rel = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(rel, (2026, 7, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())
        print(f'{target} files={len(release_paths)} sha256={digest(target)}')
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
