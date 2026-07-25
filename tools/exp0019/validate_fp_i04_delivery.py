#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
phase='lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04';docrel='docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i04'
required=[
 'releases/history/exp0019/readmes/README_EXP0019_FP_I04_DATA_SYNC.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I04_DATA_SYNC.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I04_QA_REPORT.json',
 f'{phase}/artifacts/FP_I04_DATA_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I04_DATA_REASON_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I04_SYMBOL_PAIR_PROFILES.v1.json',f'{phase}/artifacts/FP_I04_GOLDEN_SYNC_VECTORS.v1.json',
 f'{phase}/artifacts/FP_I04_CONFORMANCE_REPORT.json',f'{phase}/artifacts/FP_I04_GAP_FIXTURE_CATALOG.v1.json',
 f'{phase}/artifacts/FP_I04_REVISION_FIXTURE_CATALOG.v1.json',f'{phase}/artifacts/FP_I04_PHASE_STATUS.json',
 f'{phase}/artifacts/FP_I04_HANDOFF_TO_FP_I05.json',f'{phase}/artifacts/FP_I04_ACCEPTANCE_EVIDENCE.json',
 f'{phase}/config/FP_I04_DATA_SYNC_PROFILES.v1.json',
 'mql5/Include/FaerieProtocol/EXP0019/Data/FP_I04_All.mqh',
 'mql5/Experts/FaerieProtocolTests/EXP0019_FP_I04_DataSyncSelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncDiagnostic.mq5',
 'tools/exp0019/check_fp_i04_boundaries.py','tools/exp0019/check_fp_i04_mql5_static.py','tools/exp0019/generate_fp_i04_vectors.py','tools/exp0019/validate_fp_i04_delivery.py','tools/exp0019/build_fp_i04_release.py',
 f'{docrel}/00_FP_I04_DELIVERY_MOC.md','docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I04_MULTI-SYMBOL_M1_SYNCHRONIZATION_COVERAGE_AND_DATA_REVISION.md']
for rel in required:
    if not (root/rel).is_file():errors.append('missing '+rel)
expected_modules={'__init__.py','backfill.py','bar_validation.py','canonical.py','cli.py','conformance.py','constants.py','contracts.py','coverage.py','cursor.py','enums.py','errors.py','golden.py','normalization.py','registry.py','revision.py','symbol_resolver.py','synchronization.py'}
mods={p.name for p in (root/f'{phase}/python/fp_i04_data').glob('*.py')}
if mods!=expected_modules:errors.append(f'python module mismatch missing={sorted(expected_modules-mods)} extra={sorted(mods-expected_modules)}')
tests=list((root/f'{phase}/tests').glob('test_*.py'))
if len(tests)!=15:errors.append(f'test module count {len(tests)} != 15')
schemas=list((root/f'{phase}/schemas').glob('*.schema.json'))
if len(schemas)!=15:errors.append(f'public schema count {len(schemas)} != 15')
for path in schemas:
    try:
        schema=json.loads(path.read_text())
        if schema.get('$schema')!='https://json-schema.org/draft/2020-12/schema':errors.append('wrong dialect '+str(path.relative_to(root)))
        if schema.get('type')!='object' or schema.get('additionalProperties') is not False:errors.append('non-closed schema '+str(path.relative_to(root)))
    except Exception as exc:errors.append(f'invalid schema {path}: {exc}')
docs=list((root/docrel).rglob('*.md'))
if len(docs)!=57:errors.append(f'FP-I04 doc count {len(docs)} != 57')
for path in docs:
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):errors.append('missing frontmatter '+str(path.relative_to(root)))
    if path.parent==root/docrel and path.name!='00_FP_I04_DELIVERY_MOC.md' and len(text.splitlines())<85:errors.append('short chapter '+str(path.relative_to(root)))
concepts=list((root/'docs/obsidian_deep/01_concepts').glob('FP-I04_*.md'))
if len(concepts)!=7:errors.append(f'atomic concept count {len(concepts)} != 7')
mqls=list((root/'mql5/Include/FaerieProtocol/EXP0019/Data').glob('*.mqh'))
if len(mqls)!=13:errors.append(f'MQL5 include count {len(mqls)} != 13')
json_files=[
 f'{phase}/artifacts/FP_I04_DATA_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I04_DATA_REASON_REGISTRY.v1.json',f'{phase}/artifacts/FP_I04_SYMBOL_PAIR_PROFILES.v1.json',f'{phase}/artifacts/FP_I04_GOLDEN_SYNC_VECTORS.v1.json',f'{phase}/artifacts/FP_I04_CONFORMANCE_REPORT.json',f'{phase}/artifacts/FP_I04_GAP_FIXTURE_CATALOG.v1.json',f'{phase}/artifacts/FP_I04_REVISION_FIXTURE_CATALOG.v1.json',f'{phase}/artifacts/FP_I04_PHASE_STATUS.json',f'{phase}/artifacts/FP_I04_HANDOFF_TO_FP_I05.json',f'{phase}/artifacts/FP_I04_ACCEPTANCE_EVIDENCE.json',f'{phase}/config/FP_I04_DATA_SYNC_PROFILES.v1.json','releases/history/exp0019/reports/EXP0019_FP_I04_QA_REPORT.json']
json_files += [f'{phase}/examples/{p.name}' for p in (root/f'{phase}/examples').glob('*.json')]
for rel in json_files:
    path=root/rel
    if path.exists():
        try:json.loads(path.read_text())
        except Exception as exc:errors.append(f'invalid JSON {rel}: {exc}')
status_path=root/f'{phase}/artifacts/FP_I04_PHASE_STATUS.json'
if status_path.exists():
    d=json.loads(status_path.read_text())
    expected={'python_module_count':18,'phase_test_count':67,'cumulative_fp_test_count':279,'previous_context_regression_count':50,'public_schema_count':15,'public_contract_count':15,'data_reason_count':30,'mql5_include_count':13,'mql5_entrypoint_count':2,'delivery_doc_count':57,'atomic_concept_count':7,'conformance_check_count':10}
    for key,value in expected.items():
        if d.get(key)!=value:errors.append(f'status {key}={d.get(key)!r}, expected {value!r}')
    if d.get('runtime_authority')!='NONE':errors.append('runtime authority is not NONE')
    if d.get('metaeditor_compile_status')!='pending_local_windows':errors.append('dishonest MetaEditor status')
conf=root/f'{phase}/artifacts/FP_I04_CONFORMANCE_REPORT.json'
if conf.exists():
    d=json.loads(conf.read_text())
    if not d.get('passed') or d.get('check_count')!=10:errors.append('conformance report mismatch')
contracts=root/f'{phase}/artifacts/FP_I04_DATA_CONTRACT_REGISTRY.v1.json';reasons=root/f'{phase}/artifacts/FP_I04_DATA_REASON_REGISTRY.v1.json'
if contracts.exists() and json.loads(contracts.read_text()).get('contract_count')!=15:errors.append('contract count mismatch')
if reasons.exists() and json.loads(reasons.read_text()).get('reason_count')!=30:errors.append('reason count mismatch')
for cache in (root/phase).rglob('__pycache__'):errors.append('release cache '+str(cache.relative_to(root)))
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I04_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text().splitlines():
        if any(f'/phase_i0{i}/' in rel for i in range(4)) or rel.startswith(('mql5/Include/DayeTrader/','lab/10_infrastructure/EXP0018_')):errors.append('forbidden owned path '+rel)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'FP-I04 delivery validation PASS: {len(mods)} Python modules, {len(tests)} test modules, {len(schemas)} schemas, {len(docs)} docs, 7 concepts, 15 contracts, 30 reasons, 13 MQL5 includes, no runtime authority.')
