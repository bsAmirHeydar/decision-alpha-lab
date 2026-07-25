#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import csv,json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
phase='contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03'
docrel='docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i03'
required=[
 'releases/history/exp0019/readmes/README_EXP0019_FP_I03_TIME_CALENDAR.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I03_TIME_CALENDAR.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I03_QA_REPORT.json',
 f'{phase}/artifacts/FP_I03_TIME_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I03_TIME_REASON_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I03_SESSION_REGISTRY.v1.json',f'{phase}/artifacts/FP_I03_GOLDEN_TIME_VECTORS.v1.json',
 f'{phase}/artifacts/FP_I03_CONFORMANCE_REPORT.json',f'{phase}/artifacts/FP_I03_BOUNDARY_FIXTURE_CATALOG.v1.json',
 f'{phase}/artifacts/FP_I03_DST_TRANSITION_TABLE_2007_2035.v1.json',f'{phase}/artifacts/FP_I03_PHASE_STATUS.json',
 f'{phase}/artifacts/FP_I03_HANDOFF_TO_FP_I04.json',f'{phase}/artifacts/FP_I03_ACCEPTANCE_EVIDENCE.json',
 f'{phase}/config/FP_I03_TIME_CALENDAR_PROFILES.v1.json',
 'mql5/Include/FaerieProtocol/EXP0019/Time/FP_I03_All.mqh',
 'mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarSelfTest.mq5',
 'mql5/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarDiagnostic.mq5',
 'contexts/legacy/tools/exp0019/check_fp_i03_boundaries.py','contexts/legacy/tools/exp0019/check_fp_i03_mql5_static.py','contexts/legacy/tools/exp0019/generate_fp_i03_vectors.py',
 'contexts/legacy/tools/exp0019/validate_fp_i03_delivery.py','contexts/legacy/tools/exp0019/build_fp_i03_release.py',
 f'{docrel}/00_FP_I03_DELIVERY_MOC.md',
 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I03_NEW_YORK_TIME_TRADING-DAY_SESSION_AND_WEEK_KERNEL.md',
]
for rel in required:
    if not (root/rel).is_file():errors.append('missing '+rel)
expected_modules={'__init__.py','broker.py','calendar.py','canonical.py','cli.py','conformance.py','constants.py','contracts.py','enums.py','errors.py','golden.py','reason_codes.py','registry.py','time_math.py','validation.py'}
mods={p.name for p in (root/f'{phase}/python/fp_i03_time').glob('*.py')}
if mods!=expected_modules:errors.append(f'python module mismatch missing={sorted(expected_modules-mods)} extra={sorted(mods-expected_modules)}')
tests=list((root/f'{phase}/tests').glob('test_*.py'))
if len(tests)!=13:errors.append(f'test module count {len(tests)} != 13')
schemas=list((root/f'{phase}/schemas').glob('*.schema.json'))
if len(schemas)!=12:errors.append(f'public schema count {len(schemas)} != 12')
for path in schemas:
    try:
        schema=json.loads(path.read_text())
        if schema.get('$schema')!='https://json-schema.org/draft/2020-12/schema':errors.append('wrong dialect '+str(path.relative_to(root)))
        if schema.get('type')!='object' or schema.get('additionalProperties') is not False:errors.append('non-closed schema '+str(path.relative_to(root)))
    except Exception as exc:errors.append(f'invalid schema {path}: {exc}')
docs=list((root/docrel).rglob('*.md'))
if len(docs)!=53:errors.append(f'FP-I03 doc count {len(docs)} != 53')
for path in docs:
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):errors.append('missing frontmatter '+str(path.relative_to(root)))
    if path.parent==root/docrel and path.name!='00_FP_I03_DELIVERY_MOC.md' and len(text.splitlines())<90:errors.append('short chapter '+str(path.relative_to(root)))
concepts=list((root/'docs/obsidian_deep/01_concepts').glob('FP-I03_*.md'))
if len(concepts)!=7:errors.append(f'atomic concept count {len(concepts)} != 7')
mqls=list((root/'mql5/Include/FaerieProtocol/EXP0019/Time').glob('*.mqh'))
if len(mqls)!=12:errors.append(f'MQL5 include count {len(mqls)} != 12')
json_files=[
 f'{phase}/artifacts/FP_I03_TIME_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I03_TIME_REASON_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I03_SESSION_REGISTRY.v1.json',f'{phase}/artifacts/FP_I03_GOLDEN_TIME_VECTORS.v1.json',
 f'{phase}/artifacts/FP_I03_CONFORMANCE_REPORT.json',f'{phase}/artifacts/FP_I03_BOUNDARY_FIXTURE_CATALOG.v1.json',
 f'{phase}/artifacts/FP_I03_DST_TRANSITION_TABLE_2007_2035.v1.json',f'{phase}/artifacts/FP_I03_PHASE_STATUS.json',
 f'{phase}/artifacts/FP_I03_HANDOFF_TO_FP_I04.json',f'{phase}/artifacts/FP_I03_ACCEPTANCE_EVIDENCE.json',
 f'{phase}/config/FP_I03_TIME_CALENDAR_PROFILES.v1.json','releases/history/exp0019/reports/EXP0019_FP_I03_QA_REPORT.json'
]
json_files += [f'{phase}/examples/{p.name}' for p in (root/f'{phase}/examples').glob('*.json')]
for rel in json_files:
    path=root/rel
    if path.exists():
        try:json.loads(path.read_text())
        except Exception as exc:errors.append(f'invalid JSON {rel}: {exc}')
status_path=root/f'{phase}/artifacts/FP_I03_PHASE_STATUS.json'
if status_path.exists():
    d=json.loads(status_path.read_text())
    expected={'python_module_count':15,'phase_test_count':83,'public_schema_count':12,'public_contract_count':11,'time_reason_count':15,'mql5_include_count':12,'mql5_entrypoint_count':2,'conformance_check_count':20,'session_count':3,'boundary_fixture_count':12}
    for key,value in expected.items():
        if d.get(key)!=value:errors.append(f'status {key}={d.get(key)!r}, expected {value!r}')
    if d.get('runtime_authority')!='NONE':errors.append('runtime authority is not NONE')
    if d.get('metaeditor_compile_status')!='pending_local_windows':errors.append('dishonest MetaEditor status')
conf=root/f'{phase}/artifacts/FP_I03_CONFORMANCE_REPORT.json'
if conf.exists():
    d=json.loads(conf.read_text())
    if not d.get('passed') or d.get('check_count')!=20:errors.append('conformance report mismatch')
contracts=root/f'{phase}/artifacts/FP_I03_TIME_CONTRACT_REGISTRY.v1.json'
reasons=root/f'{phase}/artifacts/FP_I03_TIME_REASON_REGISTRY.v1.json'
sessions=root/f'{phase}/artifacts/FP_I03_SESSION_REGISTRY.v1.json'
if contracts.exists() and json.loads(contracts.read_text()).get('contract_count')!=11:errors.append('contract count mismatch')
if reasons.exists() and json.loads(reasons.read_text()).get('reason_count')!=15:errors.append('reason count mismatch')
if sessions.exists() and len(json.loads(sessions.read_text()).get('registry',{}).get('sessions',[]))!=3:errors.append('session count mismatch')
for cache in (root/phase).rglob('__pycache__'):errors.append('release cache '+str(cache.relative_to(root)))
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I03_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text().splitlines():
        if rel.startswith(('mql5/Include/DayeTrader/','lab/10_infrastructure/EXP0018_','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/')):
            errors.append('forbidden owned path '+rel)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'FP-I03 delivery validation PASS: {len(mods)} Python modules, {len(tests)} test modules, {len(schemas)} schemas, {len(docs)} docs, 7 concepts, 11 contracts, 15 reasons, 12 MQL5 includes, no runtime authority.')
