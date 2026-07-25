#!/usr/bin/env python3
from pathlib import Path
import sys,json,csv,ast
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
required=[
'releases/history/exp0019/readmes/README_EXP0019_FP_I01_COMPATIBILITY.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I01_COMPATIBILITY.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I01_QA_REPORT.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/config/FP_I01_COMPATIBILITY_POLICY.v1.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_ADAPTER_REGISTRY.v1.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_GOLDEN_ADAPTER_FIXTURES.v1.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_COMPATIBILITY_REPORT.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_PHASE_STATUS.json',
'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_HANDOFF_TO_FP_I02.json',
'mql5/Include/FaerieProtocol/EXP0019/Compatibility/FP_I01_All.mqh',
'mql5/Experts/FaerieProtocolTests/EXP0019_FP_I01_CompatibilitySelfTest.mq5',
'mql5/Experts/FaerieProtocol/EXP0019_FP_I01_CompatibilityDiagnostic.mq5',
'tools/exp0019/check_fp_i01_boundaries.py','tools/exp0019/check_fp_i01_mql5_static.py','tools/exp0019/validate_fp_i01_delivery.py','tools/exp0019/build_fp_i01_release.py']
for r in required:
 if not (root/r).is_file():errors.append('missing '+r)
base=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/python/fp_i01_compatibility'
mods={p.name for p in base.glob('*.py')};expected={'__init__.py','adapters.py','canonical.py','cli.py','differential.py','duplicate_scan.py','enums.py','errors.py','fixtures.py','hash_guard.py','models.py','policy.py','registry.py','reporting.py','validator.py'}
if mods!=expected:errors.append(f'python modules mismatch missing={expected-mods} extra={mods-expected}')
tests=list((root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/tests').glob('test_*.py'))
if len(tests)<12:errors.append(f'insufficient test modules {len(tests)}')
docroot=root/'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i01'
docs=list(docroot.rglob('*.md'))
if len(docs)<35:errors.append(f'insufficient docs {len(docs)}')
for p in docs:
 text=p.read_text(encoding='utf-8')
 if not text.startswith('---\n'):errors.append('missing frontmatter '+str(p.relative_to(root)))
 if p.parent==docroot and p.name!='00_FP_I01_DELIVERY_MOC.md' and len(text.splitlines())<80:errors.append('short chapter '+str(p.relative_to(root)))
for name in ['FP_I01_ADAPTER_REGISTRY.v1.json','FP_I01_GOLDEN_ADAPTER_FIXTURES.v1.json','FP_I01_COMPATIBILITY_REPORT.json','FP_I01_PHASE_STATUS.json','FP_I01_HANDOFF_TO_FP_I02.json']:
 p=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts'/name
 if p.exists():
  try:json.loads(p.read_text())
  except Exception as e:errors.append(f'invalid json {name}: {e}')
report=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_COMPATIBILITY_REPORT.json'
if report.exists():
 d=json.loads(report.read_text())
 if d.get('status')!='PASS':errors.append('compatibility report not PASS')
 if len(d.get('dependency_results',[]))!=19:errors.append('dependency result count mismatch')
 if len(d.get('adapter_results',[]))!=8:errors.append('adapter result count mismatch')
status=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_PHASE_STATUS.json'
if status.exists():
 d=json.loads(status.read_text())
 if d.get('python_test_count')!=39:errors.append('phase test count mismatch')
 if d.get('metaeditor_compile_status')!='pending_local_windows':errors.append('metaeditor status dishonest')
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I01_FILE_INDEX.txt'
if index.exists():
 paths=index.read_text().splitlines()
 for prefix in ('mql5/Include/IntermarketDivergenceExecution/CG/','mql5/Include/DayeTrader/EXP0018/'):
  if any(x.startswith(prefix) for x in paths):errors.append('shared-core path in index '+prefix)
for p in (root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01').rglob('__pycache__'):errors.append('cache in release '+str(p.relative_to(root)))
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'FP-I01 delivery validation PASS: {len(mods)} modules, {len(tests)} test modules, {len(docs)} docs, 19 pins, 8 adapters, MQL5 mirror, no shared-core ownership.')
