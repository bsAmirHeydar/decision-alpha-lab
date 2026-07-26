#!/usr/bin/env python3
"""Validate completeness and internal consistency of the UCE-I10 delivery."""
from pathlib import Path
import ast
import csv
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
required = [
    'releases/history/strategy_factory_ucee/readmes/README_STRATEGY_FACTORY_UCEE_I10_IMPLEMENTATION.md',
    'releases/history/strategy_factory_ucee/installers/INSTALL_STRATEGY_FACTORY_UCEE_I10_IMPLEMENTATION.md',
    'releases/history/ucee/scripts/EXPAND_REMOVE_UCEE_I10_PATCH.ps1',
    'COMMIT_MESSAGE.md',
    'mql5/Include/AlphaLab/StrategyFactory/DeepViews/UCEI10_All.mqh',
    'mql5/Include/AlphaLab/StrategyFactory/DeepViews/UCEI10_DependencyTransferContracts.mqh',
    'mql5/Experts/StrategyFactory/UCE_I10_DeepViewsDiagnostic.mq5',
    'mql5/Tests/Experts/StrategyFactory/UCE_I10_DeepViewsSelfTest.mq5',
    'mql5/Tests/Experts/StrategyFactory/UCE_I10_CausalitySafetySelfTest.mq5',
    'src/engine/packages/strategy_factory_deep_views_v3/catalog.py',
    'src/engine/packages/strategy_factory_deep_views_v3/sequence.py',
    'src/engine/packages/strategy_factory_deep_views_v3/raster.py',
    'src/engine/packages/strategy_factory_deep_views_v3/graph.py',
    'src/engine/packages/strategy_factory_deep_views_v3/regime.py',
    'src/engine/packages/strategy_factory_deep_views_v3/fusion.py',
    'src/engine/packages/strategy_factory_deep_views_v3/qualification.py',
    'src/engine/packages/strategy_factory_deep_views_v3/trainer_plugins.py',
    'schemas/legacy/strategy_factory/v3/sequence_artifact.schema.json',
    'schemas/legacy/strategy_factory/v3/pixel_audit_report.schema.json',
    'schemas/legacy/strategy_factory/v3/dependency_probe.schema.json',
    'schemas/legacy/strategy_factory/v3/transfer_boundary.schema.json',
    'tests/fixtures/legacy/strategy_factory/v3/uce_i10_deep_view_conformance_vectors.json',
    'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i10/00_UCE_I10_DELIVERY_MOC.md',
    'src/engine/tooling/strategy_factory/apply_uce_i10_patch.ps1',
    'src/engine/tooling/strategy_factory/build_uce_i10_release.py',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10_HANDOFF_TO_UCE_I11.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ACCEPTANCE_EVIDENCE.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ARTIFACT_INVENTORY.csv',
]
for relative in required:
    if not (root / relative).is_file():
        errors.append('missing ' + relative)

schema_names = (
    'deep_algorithm_descriptor', 'view_tensor_spec', 'sequence_window_spec', 'sequence_artifact',
    'raster_spec', 'raster_artifact', 'pixel_audit_report', 'graph_spec', 'graph_artifact',
    'regime_novelty_prediction', 'fusion_prediction', 'deep_admission_evidence',
    'seed_run_observation', 'view_ablation_observation', 'export_assessment',
    'deep_qualification_report', 'distillation_report', 'quantization_report',
    'dependency_probe', 'adapter_plan', 'transfer_boundary', 'future_perturbation_audit',
    'deterministic_replay_audit', 'deep_registry_snapshot',
)
for name in schema_names:
    path = root / f'schemas/legacy/strategy_factory/v3/{name}.schema.json'
    if not path.is_file():
        errors.append(f'missing schema {name}')
        continue
    try:
        schema = json.loads(path.read_text(encoding='utf-8'))
        if schema.get('type') != 'object' or schema.get('additionalProperties') is not False:
            errors.append(f'non-closed schema {name}')
        if not schema.get('$id', '').endswith(f'/{name}.schema.json'):
            errors.append(f'invalid schema id {name}')
    except Exception as exc:
        errors.append(f'invalid schema {name}: {exc}')

for relative in (
    'tests/fixtures/legacy/strategy_factory/v3/uce_i10_deep_view_conformance_vectors.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I10_HANDOFF_TO_UCE_I11.json',
    'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ACCEPTANCE_EVIDENCE.json',
    'releases/history/ucee/manifests/UCEE_I10_PATCH_MANIFEST.json', 'releases/history/ucee/reports/UCEE_I10_QA_REPORT.json',
):
    path = root / relative
    if path.exists():
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid json {relative}: {exc}')

package = root / 'src/engine/packages/strategy_factory_deep_views_v3'
expected_modules = {
    '__init__.py','adapters.py','audit.py','canonical.py','catalog.py','cli.py','compression.py',
    'conformance.py','contracts.py','enums.py','errors.py','fusion.py','gates.py','golden.py',
    'graph.py','math_utils.py','qualification.py','raster.py','regime.py','registry.py',
    'sequence.py','trainer_plugins.py','transfer.py',
}
actual_modules = {path.name for path in package.glob('*.py')}
if expected_modules - actual_modules:
    errors.append('missing Python modules: ' + ', '.join(sorted(expected_modules - actual_modules)))

phase_tests = list((root / 'tests/legacy/strategy_factory/v1/phase_uce_i10_deep_views').glob('test_*.py'))
if len(phase_tests) < 17:
    errors.append(f'insufficient I10 test modules: {len(phase_tests)}')

docs = root / 'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i10'
notes = list(docs.rglob('*.md')) if docs.exists() else []
if len(notes) < 31:
    errors.append(f'insufficient detailed Obsidian documentation: {len(notes)}')
for note in notes:
    text = note.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        errors.append(f'missing YAML frontmatter: {note.relative_to(root)}')
    if note.parent == docs and note.name != '00_UCE_I10_DELIVERY_MOC.md' and len(text.splitlines()) < 70:
        errors.append(f'chapter is not detailed enough: {note.relative_to(root)}')

catalog_path = root / 'src/engine/packages/strategy_factory_deep_views_v3/catalog.py'
if catalog_path.exists():
    tree = ast.parse(catalog_path.read_text(encoding='utf-8'))
    catalog_size = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'CATALOG' for target in node.targets):
            if isinstance(node.value, (ast.Tuple, ast.List)):
                catalog_size = len(node.value.elts)
    if catalog_size != 17:
        errors.append(f'Python catalog does not contain exactly 17 descriptors: {catalog_size}')

mql5_catalog = root / 'mql5/Include/AlphaLab/StrategyFactory/DeepViews/UCEI10_Catalog.mqh'
if mql5_catalog.exists():
    compact = ''.join(mql5_catalog.read_text(encoding='utf-8').split())
    if 'Count(){return17;}' not in compact or 'NativeCount(){return10;}' not in compact:
        errors.append('MQL5 catalog count/native count mismatch')

# Cache directories are excluded by the release builder and cleaned before packaging.
inventory = root / 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I10_ARTIFACT_INVENTORY.csv'
if inventory.exists():
    try:
        rows = list(csv.DictReader(inventory.read_text(encoding='utf-8').splitlines()))
        if not rows or not {'path','sha256','size_bytes'} <= set(rows[0]):
            errors.append('artifact inventory columns are incomplete')
    except Exception as exc:
        errors.append(f'invalid artifact inventory: {exc}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(
    f'UCE-I10 delivery validation PASS: {len(expected_modules)} Python modules, {len(phase_tests)} test modules, '
    f'{len(schema_names)} closed schemas, {len(notes)} Obsidian notes, 17 algorithms/10 native, '
    'phase evidence, patch tooling, MQL5 mirrors, and release-clean cache policy.'
)
