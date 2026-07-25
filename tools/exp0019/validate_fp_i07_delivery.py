#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
phase = 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i07'
docrel = 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i07'
required = [
    'releases/history/exp0019/readmes/README_EXP0019_FP_I07_CONFIRMATION_ENGINE.md',
    'releases/history/exp0019/installers/INSTALL_EXP0019_FP_I07_CONFIRMATION_ENGINE.md',
    'COMMIT_MESSAGE.md',
    'releases/history/exp0019/reports/EXP0019_FP_I07_QA_REPORT.json',
    f'{phase}/artifacts/FP_I07_CONTRACT_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I07_CONFIRMATION_REASON_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I07_GOLDEN_CONFIRMATION_VECTORS.v1.json',
    f'{phase}/artifacts/FP_I07_PHASE_STATUS.json',
    f'{phase}/artifacts/FP_I07_HANDOFF_TO_FP_I08.json',
    f'{phase}/artifacts/FP_I07_ACCEPTANCE_EVIDENCE.json',
    f'{phase}/config/FP_I07_CONFIRMATION_PROFILES.v1.json',
    f'{docrel}/00_FP_I07_DELIVERY_MOC.md',
    'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07/FP_I07_All.mqh',
    'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I07_ConfirmationDiagnostic.mq5',
    'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I07_ConfirmationSelfTest.mq5',
    'tools/exp0019/check_fp_i07_boundaries.py',
    'tools/exp0019/check_fp_i07_mql5_static.py',
    'tools/exp0019/validate_fp_i07_delivery.py',
    'tools/exp0019/build_fp_i07_release.py',
]
for rel in required:
    if not (root / rel).is_file():
        errors.append('missing ' + rel)

mods = list((root / f'{phase}/python/fp_i07_confirmation').glob('*.py'))
tests = list((root / f'{phase}/tests').glob('test_*.py'))
schemas = list((root / f'{phase}/schemas').glob('*.schema.json'))
docs = list((root / docrel).rglob('*.md'))
concepts = list((root / 'docs/obsidian_deep/01_concepts').glob('FP-I07_*.md'))
mql = list((root / 'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I07').glob('*.mqh'))
expected = (19, 14, 15, 49, 7, 14)
actual = (len(mods), len(tests), len(schemas), len(docs), len(concepts), len(mql))
if actual != expected:
    errors.append(f'count mismatch actual={actual} expected={expected}')

for path in schemas:
    try:
        schema = json.loads(path.read_text(encoding='utf-8'))
        if schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            errors.append('wrong schema dialect ' + str(path.relative_to(root)))
        if schema.get('type') != 'object' or schema.get('additionalProperties') is not False:
            errors.append('nonclosed schema ' + str(path.relative_to(root)))
    except Exception as exc:
        errors.append(f'invalid schema {path}: {exc}')

for path in docs:
    if not path.read_text(encoding='utf-8').startswith('---\n') and 'templates/' not in path.as_posix():
        errors.append('missing frontmatter ' + str(path.relative_to(root)))

for path in (root / phase).rglob('__pycache__'):
    errors.append('release cache ' + str(path.relative_to(root)))

json_files = [
    f'{phase}/artifacts/FP_I07_CONTRACT_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I07_CONFIRMATION_REASON_REGISTRY.v1.json',
    f'{phase}/artifacts/FP_I07_GOLDEN_CONFIRMATION_VECTORS.v1.json',
    f'{phase}/artifacts/FP_I07_PHASE_STATUS.json',
    f'{phase}/artifacts/FP_I07_HANDOFF_TO_FP_I08.json',
    f'{phase}/artifacts/FP_I07_ACCEPTANCE_EVIDENCE.json',
    f'{phase}/config/FP_I07_CONFIRMATION_PROFILES.v1.json',
    'releases/history/exp0019/reports/EXP0019_FP_I07_QA_REPORT.json',
]
for rel in json_files:
    path = root / rel
    if path.exists():
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid JSON {rel}: {exc}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(
    f'FP-I07 delivery PASS: {len(mods)} modules, {len(tests)} test modules, '
    f'{len(schemas)} schemas, {len(docs)} docs, {len(concepts)} concepts, '
    f'{len(mql)} MQL5 includes, no runtime authority.'
)
