#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
phase = 'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06'
docrel = 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i06'
required = [
    'releases/history/exp0019/readmes/README_EXP0019_FP_I06_RELATION_ENGINE.md',
    'releases/history/exp0019/installers/INSTALL_EXP0019_FP_I06_RELATION_ENGINE.md',
    'COMMIT_MESSAGE.md',
    'releases/history/exp0019/reports/EXP0019_FP_I06_QA_REPORT.json',
    f'{phase}/artifacts/FP_I06_CONTRACT_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_HUNT_REASON_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_RELATION_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_GOLDEN_RELATION_VECTORS.v1.json',
    f'{phase}/artifacts/FP_I06_PHASE_STATUS.json',
    f'{phase}/artifacts/FP_I06_HANDOFF_TO_FP_I07.json',
    f'{phase}/artifacts/FP_I06_ACCEPTANCE_EVIDENCE.json',
    f'{phase}/config/FP_I06_RELATION_ENGINE_PROFILES.v1.json',
    f'{docrel}/00_FP_I06_DELIVERY_MOC.md',
    'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I06/FP_I06_All.mqh',
    'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationDiagnostic.mq5',
    'mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I06_RelationSelfTest.mq5',
    'contexts/legacy/tools/exp0019/check_fp_i06_boundaries.py',
    'contexts/legacy/tools/exp0019/check_fp_i06_mql5_static.py',
    'contexts/legacy/tools/exp0019/generate_fp_i06_vectors.py',
    'contexts/legacy/tools/exp0019/validate_fp_i06_delivery.py',
    'contexts/legacy/tools/exp0019/build_fp_i06_release.py',
]
for rel in required:
    if not (root / rel).is_file():
        errors.append('missing ' + rel)

expected_modules = {
    '__init__.py', 'benchmark.py', 'canonical.py', 'checkpoint.py', 'classification.py',
    'cli.py', 'compiler.py', 'conformance.py', 'constants.py', 'contracts.py',
    'engine.py', 'enums.py', 'errors.py', 'golden.py', 'hunt.py', 'registry.py', 'revision.py',
}
mods = {p.name for p in (root / f'{phase}/python/fp_i06_relations').glob('*.py')}
if mods != expected_modules:
    errors.append(f'python module mismatch missing={sorted(expected_modules-mods)} extra={sorted(mods-expected_modules)}')

tests = list((root / f'{phase}/tests').glob('test_*.py'))
if len(tests) != 13:
    errors.append(f'test module count {len(tests)} != 13')

schemas = list((root / f'{phase}/schemas').glob('*.schema.json'))
if len(schemas) != 15:
    errors.append(f'public schema count {len(schemas)} != 15')
for path in schemas:
    try:
        schema = json.loads(path.read_text(encoding='utf-8'))
        if schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            errors.append('wrong dialect ' + str(path.relative_to(root)))
        if schema.get('type') != 'object' or schema.get('additionalProperties') is not False:
            errors.append('non-closed schema ' + str(path.relative_to(root)))
    except Exception as exc:
        errors.append(f'invalid schema {path}: {exc}')

docs = list((root / docrel).rglob('*.md'))
if len(docs) != 48:
    errors.append(f'FP-I06 doc count {len(docs)} != 48')
for path in docs:
    if not path.read_text(encoding='utf-8').startswith('---\n'):
        errors.append('missing frontmatter ' + str(path.relative_to(root)))

concepts = list((root / 'docs/obsidian_deep/01_concepts').glob('FP-I06_*.md'))
if len(concepts) != 7:
    errors.append(f'atomic concept count {len(concepts)} != 7')

mqls = list((root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I06').glob('*.mqh'))
if len(mqls) != 12:
    errors.append(f'MQL5 include count {len(mqls)} != 12')

json_files = [
    f'{phase}/artifacts/FP_I06_CONTRACT_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_HUNT_REASON_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_RELATION_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I06_GOLDEN_RELATION_VECTORS.v1.json',
    f'{phase}/artifacts/FP_I06_PHASE_STATUS.json',
    f'{phase}/artifacts/FP_I06_HANDOFF_TO_FP_I07.json',
    f'{phase}/artifacts/FP_I06_ACCEPTANCE_EVIDENCE.json',
    f'{phase}/config/FP_I06_RELATION_ENGINE_PROFILES.v1.json',
    'releases/history/exp0019/reports/EXP0019_FP_I06_QA_REPORT.json',
]
json_files += [f'{phase}/examples/{p.name}' for p in (root / f'{phase}/examples').glob('*.json')]
for rel in json_files:
    path = root / rel
    if path.exists():
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid JSON {rel}: {exc}')

status_path = root / f'{phase}/artifacts/FP_I06_PHASE_STATUS.json'
if status_path.exists():
    d = json.loads(status_path.read_text(encoding='utf-8'))
    expected = {
        'python_module_count': 17,
        'phase_test_count': 48,
        'cumulative_fp_test_count': 378,
        'previous_context_regression_count': 50,
        'public_schema_count': 15,
        'public_contract_count': 15,
        'reason_code_count': 70,
        'relation_registry_count': 7,
        'supported_relation_count': 6,
        'mql5_include_count': 12,
        'mql5_entrypoint_count': 2,
        'delivery_doc_count': 48,
        'atomic_concept_count': 7,
        'conformance_check_count': 6,
    }
    for key, value in expected.items():
        if d.get(key) != value:
            errors.append(f'status {key}={d.get(key)!r}, expected {value!r}')
    if d.get('runtime_authority') != 'NONE':
        errors.append('runtime authority is not NONE')
    if d.get('metaeditor_compile_status') != 'pending_local_windows':
        errors.append('dishonest MetaEditor status')

contracts = root / f'{phase}/artifacts/FP_I06_CONTRACT_REGISTRY.v1.json'
if contracts.exists() and json.loads(contracts.read_text(encoding='utf-8')).get('contract_count') != 15:
    errors.append('contract count mismatch')
relations = root / f'{phase}/artifacts/FP_I06_RELATION_REGISTRY.v1.json'
if relations.exists():
    d = json.loads(relations.read_text(encoding='utf-8'))
    if d.get('relation_count') != 7 or d.get('supported_relation_count') != 6:
        errors.append('relation registry count mismatch')

for cache in (root / phase).rglob('__pycache__'):
    errors.append('release cache ' + str(cache.relative_to(root)))

index = root / 'releases/history/exp0019/indexes/EXP0019_FP_I06_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text(encoding='utf-8').splitlines():
        if any(f'/phase_i0{i}/' in rel for i in range(6)) or rel.startswith(('mql5/Include/DayeTrader/', 'lab/10_infrastructure/EXP0018_')):
            errors.append('forbidden owned path ' + rel)

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'FP-I06 delivery validation PASS: {len(mods)} Python modules, {len(tests)} test modules, {len(schemas)} schemas, {len(docs)} docs, 7 concepts, 15 contracts, 7 relations/6 supported, 12 MQL5 includes, no runtime authority.')
