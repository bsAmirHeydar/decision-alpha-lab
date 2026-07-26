#!/usr/bin/env python3
"""Validate completeness and internal consistency of the UCE-I12 delivery."""
from __future__ import annotations
from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); errors=[]
PACKAGE_REL='src/engine/packages/strategy_factory_promotion_v3'
TEST_REL='tests/legacy/strategy_factory/v1/phase_uce_i12_promotion'
DOC_REL='docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i12'
STATUS='releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation'
MODULES={'__init__.py','calibration.py','canonical.py','cli.py','conformance.py','contracts.py','enums.py','errors.py','evidence.py','gate.py','golden.py','multiplicity.py','nulls.py','registry.py','scorecard.py','stress.py','uncertainty.py','winner_overfit.py'}
SCHEMAS=(
'promotion_trial_evidence','promotion_selection_universe','promotion_family_definition','promotion_test_evidence','promotion_uncertainty_request','promotion_uncertainty_report','promotion_sequential_confidence_report','promotion_multiplicity_report','promotion_nested_selection_audit','promotion_universe_reconciliation','promotion_pbo_report','promotion_deflated_performance_report','promotion_reality_check_report','promotion_spa_report','promotion_null_control_plan','promotion_null_control_result','promotion_stress_plan','promotion_stress_result','promotion_calibration_report','promotion_prospective_challenge_freeze','promotion_policy','promotion_model_risk_scorecard','promotion_evidence_bundle','promotion_decision','promotion_registry_snapshot')
required=[
'releases/history/strategy_factory_ucee/readmes/README_STRATEGY_FACTORY_UCEE_I12_IMPLEMENTATION.md','releases/history/strategy_factory_ucee/installers/INSTALL_STRATEGY_FACTORY_UCEE_I12_IMPLEMENTATION.md','releases/history/ucee/scripts/EXPAND_REMOVE_UCEE_I12_PATCH.ps1','COMMIT_MESSAGE.md',
f'{PACKAGE_REL}/uncertainty.py',f'{PACKAGE_REL}/multiplicity.py',f'{PACKAGE_REL}/winner_overfit.py',f'{PACKAGE_REL}/nulls.py',f'{PACKAGE_REL}/stress.py',f'{PACKAGE_REL}/calibration.py',f'{PACKAGE_REL}/gate.py',f'{PACKAGE_REL}/evidence.py',
'tests/fixtures/legacy/strategy_factory/v3/uce_i12_promotion_conformance_vectors.json',f'{DOC_REL}/00_UCE_I12_DELIVERY_MOC.md','docs/history/systems/ucee/implementation_program/phases/UCE_I12_STATISTICAL_AND_ANTI_OVERFIT_PROMOTION_GATE.md',
'mql5/Include/AlphaLab/StrategyFactory/StatisticalPromotion/UCEI12_All.mqh','mql5/Experts/StrategyFactory/UCE_I12_StatisticalPromotionDiagnostic.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I12_PromotionContractsSelfTest.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I12_NonCompensatoryGateSelfTest.mq5',
f'{STATUS}/phase_status/UCE_I12.json',f'{STATUS}/phase_status/UCE_I12_HANDOFF_TO_UCE_I13.json',f'{STATUS}/artifacts/UCE_I12_ACCEPTANCE_EVIDENCE.json',
'src/engine/tooling/strategy_factory/check_uce_i12_boundaries.py','src/engine/tooling/strategy_factory/check_uce_i12_mql5_static.py','src/engine/tooling/strategy_factory/compile_uce_i12_statistical_promotion.ps1','src/engine/tooling/strategy_factory/generate_uce_i12_vectors.py','src/engine/tooling/strategy_factory/run_uce_i12_tests.ps1','src/engine/tooling/strategy_factory/validate_uce_i12_delivery.py','src/engine/tooling/strategy_factory/build_uce_i12_release.py','src/engine/packages/pyproject.toml']
for rel in required:
    if not (root/rel).is_file(): errors.append('missing '+rel)
actual={p.name for p in (root/PACKAGE_REL).glob('*.py')}
if actual!=MODULES: errors.append(f'Python module mismatch missing={sorted(MODULES-actual)} extra={sorted(actual-MODULES)}')
tests=list((root/TEST_REL).glob('test_*.py'))
if len(tests)<11: errors.append(f'insufficient phase test modules: {len(tests)}')
for name in SCHEMAS:
    p=root/f'schemas/legacy/strategy_factory/v3/{name}.schema.json'
    if not p.is_file(): errors.append('missing schema '+name); continue
    try:
        s=json.loads(p.read_text())
        if s.get('$schema')!='https://json-schema.org/draft/2020-12/schema' or s.get('type')!='object' or s.get('additionalProperties') is not False: errors.append('non-closed schema '+name)
        if not s.get('$id','').endswith('/'+name+'.schema.json'): errors.append('bad schema id '+name)
    except Exception as exc: errors.append(f'invalid schema {name}: {exc}')
for p in [root/'tests/fixtures/legacy/strategy_factory/v3/uce_i12_promotion_conformance_vectors.json',root/f'{STATUS}/phase_status/UCE_I12.json',root/f'{STATUS}/phase_status/UCE_I12_HANDOFF_TO_UCE_I13.json',root/f'{STATUS}/artifacts/UCE_I12_ACCEPTANCE_EVIDENCE.json']+list((root/'examples/legacy/strategy_factory/uce_i12').glob('*.json')):
    try: json.loads(p.read_text())
    except Exception as exc: errors.append(f'invalid JSON {p.relative_to(root)}: {exc}')
docs=list((root/DOC_REL).glob('*.md'))
if len(docs)<34: errors.append(f'insufficient detailed delivery notes: {len(docs)}')
for p in docs:
    text=p.read_text()
    if not text.startswith('---\n'): errors.append(f'missing frontmatter {p.relative_to(root)}')
    for heading in ('## Core invariants','## Failure matrix','## Executable test obligations','## Operator runbook','## Evidence retained'):
        if heading not in text: errors.append(f'{p.relative_to(root)} missing {heading}')
concepts=list((root/'docs/history/obsidian/deep/01_concepts').glob('UCE-I12_*.md'))
if len(concepts)<8: errors.append(f'insufficient atomic concepts: {len(concepts)}')
mql=list((root/'mql5/Include/AlphaLab/StrategyFactory/StatisticalPromotion').glob('UCEI12_*.mqh'))+[root/'mql5/Experts/StrategyFactory/UCE_I12_StatisticalPromotionDiagnostic.mq5',root/'mql5/Tests/Experts/StrategyFactory/UCE_I12_PromotionContractsSelfTest.mq5',root/'mql5/Tests/Experts/StrategyFactory/UCE_I12_NonCompensatoryGateSelfTest.mq5']
if len(mql)!=11 or not all(p.is_file() for p in mql): errors.append(f'MQL5 file set invalid: {len(mql)}')
pyproject=(root/'src/engine/packages/pyproject.toml').read_text()
for token in ('strategy-factory-experiments-v3','strategy-factory-promotion-v3','strategy_factory_promotion_v3*','version="0.31.0"'):
    if token not in pyproject: errors.append('pyproject missing '+token)
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'UCE-I12 delivery validation PASS: {len(MODULES)} Python modules, {len(tests)} test modules, {len(SCHEMAS)} closed schemas, {len(docs)} detailed notes, {len(concepts)} concepts, 7 suites, 11 MQL5 files.')
