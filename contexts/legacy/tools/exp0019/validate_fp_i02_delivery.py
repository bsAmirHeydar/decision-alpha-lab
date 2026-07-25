#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv,json,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
phase='contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02'
docrel='docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i02'
required=[
 'releases/history/exp0019/readmes/README_EXP0019_FP_I02_CORE_KERNEL.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I02_CORE_KERNEL.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I02_QA_REPORT.json',
 f'{phase}/artifacts/FP_I02_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I02_REASON_CODE_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I02_RELATION_REGISTRY.v2.json',f'{phase}/artifacts/FP_I02_STATE_MACHINE_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I02_GOLDEN_IDENTITY_VECTORS.v1.json',f'{phase}/artifacts/FP_I02_CONFORMANCE_REPORT.json',
 f'{phase}/artifacts/FP_I02_PHASE_STATUS.json',f'{phase}/artifacts/FP_I02_HANDOFF_TO_FP_I03.json',f'{phase}/artifacts/FP_I02_ACCEPTANCE_EVIDENCE.json',
 f'{phase}/config/FP_I02_CONFIGURATION_PROFILES.v1.json',
 'mql5/Include/FaerieProtocol/EXP0019/Core/FP_I02_All.mqh',
 'mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I02_ContractKernelSelfTest.mq5',
 'mql5/Experts/FaerieProtocol/EXP0019_FP_I02_ContractKernelDiagnostic.mq5',
 'contexts/legacy/tools/exp0019/check_fp_i02_boundaries.py','contexts/legacy/tools/exp0019/check_fp_i02_mql5_static.py','contexts/legacy/tools/exp0019/generate_fp_i02_vectors.py',
 'contexts/legacy/tools/exp0019/validate_fp_i02_delivery.py','contexts/legacy/tools/exp0019/build_fp_i02_release.py',
 f'{docrel}/00_FP_I02_DELIVERY_MOC.md',
]
for rel in required:
 if not (root/rel).is_file():errors.append('missing '+rel)

expected_modules={'__init__.py','canonical.py','cli.py','config.py','conformance.py','contracts.py','enums.py','errors.py','golden.py','identity.py','lifecycle.py','migration.py','reason_codes.py','registry.py','relations.py','validation.py'}
mods={p.name for p in (root/f'{phase}/python/fp_i02_kernel').glob('*.py')}
if mods!=expected_modules:errors.append(f'python module mismatch missing={sorted(expected_modules-mods)} extra={sorted(mods-expected_modules)}')
tests=list((root/f'{phase}/tests').glob('test_*.py'))
if len(tests)<11:errors.append(f'insufficient test modules {len(tests)}')
schemas=list((root/f'{phase}/schemas').glob('*.schema.json'))
if len(schemas)!=18:errors.append(f'public schema count {len(schemas)} != 18')
for path in schemas:
 try:
  schema=json.loads(path.read_text())
  if schema.get('$schema')!='https://json-schema.org/draft/2020-12/schema':errors.append('wrong dialect '+str(path.relative_to(root)))
  if schema.get('type')!='object' or schema.get('additionalProperties') is not False:errors.append('non-closed schema '+str(path.relative_to(root)))
 except Exception as exc:errors.append(f'invalid schema {path}: {exc}')

docroot=root/docrel;docs=list(docroot.rglob('*.md'))
if len(docs)<46:errors.append(f'insufficient FP-I02 docs {len(docs)}')
for path in docs:
 text=path.read_text(encoding='utf-8')
 if not text.startswith('---\n'):errors.append('missing frontmatter '+str(path.relative_to(root)))
 if path.parent==docroot and path.name!='00_FP_I02_DELIVERY_MOC.md' and len(text.splitlines())<80:errors.append('short chapter '+str(path.relative_to(root)))
concepts=list((root/'docs/obsidian_deep/01_concepts').glob('FP-I02_*.md'))
if len(concepts)!=7:errors.append(f'atomic concept count {len(concepts)} != 7')

json_files=[
 f'{phase}/artifacts/FP_I02_CONTRACT_REGISTRY.v1.json',f'{phase}/artifacts/FP_I02_REASON_CODE_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I02_RELATION_REGISTRY.v2.json',f'{phase}/artifacts/FP_I02_STATE_MACHINE_REGISTRY.v1.json',
 f'{phase}/artifacts/FP_I02_GOLDEN_IDENTITY_VECTORS.v1.json',f'{phase}/artifacts/FP_I02_CONFORMANCE_REPORT.json',
 f'{phase}/artifacts/FP_I02_PHASE_STATUS.json',f'{phase}/artifacts/FP_I02_HANDOFF_TO_FP_I03.json',f'{phase}/artifacts/FP_I02_ACCEPTANCE_EVIDENCE.json',
 f'{phase}/config/FP_I02_CONFIGURATION_PROFILES.v1.json','releases/history/exp0019/reports/EXP0019_FP_I02_QA_REPORT.json'
]
for rel in json_files:
 path=root/rel
 if path.exists():
  try:json.loads(path.read_text())
  except Exception as exc:errors.append(f'invalid JSON {rel}: {exc}')

status=root/f'{phase}/artifacts/FP_I02_PHASE_STATUS.json'
if status.exists():
 d=json.loads(status.read_text())
 expected={'python_module_count':16,'phase_test_count':64,'public_schema_count':18,'relation_count':7,'reason_code_count':35,'public_contract_count':16,'mql5_include_count':11,'mql5_entrypoint_count':2}
 for key,value in expected.items():
  if d.get(key)!=value:errors.append(f'status {key}={d.get(key)!r}, expected {value!r}')
 if d.get('runtime_authority')!='NONE':errors.append('runtime authority is not NONE')
 if d.get('metaeditor_compile_status')!='pending_local_windows':errors.append('dishonest MetaEditor status')

conf=root/f'{phase}/artifacts/FP_I02_CONFORMANCE_REPORT.json'
if conf.exists():
 d=json.loads(conf.read_text())
 if not d.get('passed') or d.get('check_count')!=19:errors.append('conformance report mismatch')

reasons=root/f'{phase}/artifacts/FP_I02_REASON_CODE_REGISTRY.v1.json'
relations=root/f'{phase}/artifacts/FP_I02_RELATION_REGISTRY.v2.json'
contracts=root/f'{phase}/artifacts/FP_I02_CONTRACT_REGISTRY.v1.json'
if reasons.exists() and json.loads(reasons.read_text()).get('reason_count')!=35:errors.append('reason artifact count mismatch')
if relations.exists() and json.loads(relations.read_text()).get('relation_count')!=7:errors.append('relation artifact count mismatch')
if contracts.exists() and json.loads(contracts.read_text()).get('contract_count')!=16:errors.append('contract artifact count mismatch')

for cache in (root/phase).rglob('__pycache__'):errors.append('release cache '+str(cache.relative_to(root)))
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I02_FILE_INDEX.txt'
if index.exists():
 for rel in index.read_text().splitlines():
  if rel.startswith(('lab/10_infrastructure/EXP0017_','lab/10_infrastructure/EXP0018_','mql5/Include/AlphaLab/')):
   errors.append('forbidden owned path '+rel)

if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'FP-I02 delivery validation PASS: {len(mods)} Python modules, {len(tests)} test modules, {len(schemas)} schemas, {len(docs)} docs, 7 relations, 35 reasons, 16 contracts, 11 MQL5 includes, no runtime authority.')
