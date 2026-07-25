#!/usr/bin/env python3
"""Build exact file index, hashes, manifest, inventory, and deterministic I12 patch ZIP."""
from __future__ import annotations
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import argparse,csv,json,zipfile
STATUS='releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation'
SCHEMAS=(
'promotion_trial_evidence','promotion_selection_universe','promotion_family_definition','promotion_test_evidence','promotion_uncertainty_request','promotion_uncertainty_report','promotion_sequential_confidence_report','promotion_multiplicity_report','promotion_nested_selection_audit','promotion_universe_reconciliation','promotion_pbo_report','promotion_deflated_performance_report','promotion_reality_check_report','promotion_spa_report','promotion_null_control_plan','promotion_null_control_result','promotion_stress_plan','promotion_stress_result','promotion_calibration_report','promotion_prospective_challenge_freeze','promotion_policy','promotion_model_risk_scorecard','promotion_evidence_bundle','promotion_decision','promotion_registry_snapshot')
META={'releases/history/ucee/indexes/UCEE_I12_FILE_INDEX.txt','releases/history/ucee/hashes/UCEE_I12_FILE_HASHES.sha256','releases/history/ucee/manifests/UCEE_I12_PATCH_MANIFEST.json'}
def digest(p:Path)->str:return sha256(p.read_bytes()).hexdigest()
def owned(root:Path)->list[Path]:
    paths=set()
    for rel in ('src/engine/packages/strategy_factory_promotion_v3','tests/legacy/strategy_factory/v1/phase_uce_i12_promotion','examples/legacy/strategy_factory/uce_i12','docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i12','mql5/Include/AlphaLab/StrategyFactory/StatisticalPromotion'):
        base=root/rel
        for p in base.rglob('*') if base.exists() else ():
            if p.is_file() and p.suffix!='.pyc' and '__pycache__' not in p.parts: paths.add(p)
    specific=['releases/history/strategy_factory_ucee/readmes/README_STRATEGY_FACTORY_UCEE_I12_IMPLEMENTATION.md','releases/history/strategy_factory_ucee/installers/INSTALL_STRATEGY_FACTORY_UCEE_I12_IMPLEMENTATION.md','releases/history/ucee/scripts/EXPAND_REMOVE_UCEE_I12_PATCH.ps1','COMMIT_MESSAGE.md','releases/history/ucee/reports/UCEE_I12_QA_REPORT.json','releases/history/ucee/indexes/UCEE_I12_FILE_INDEX.txt','releases/history/ucee/hashes/UCEE_I12_FILE_HASHES.sha256','releases/history/ucee/manifests/UCEE_I12_PATCH_MANIFEST.json','src/engine/packages/pyproject.toml','tests/fixtures/legacy/strategy_factory/v3/uce_i12_promotion_conformance_vectors.json','docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phases/UCE_I12_STATISTICAL_AND_ANTI_OVERFIT_PROMOTION_GATE.md','mql5/Experts/StrategyFactory/UCE_I12_StatisticalPromotionDiagnostic.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I12_PromotionContractsSelfTest.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I12_NonCompensatoryGateSelfTest.mq5',f'{STATUS}/phase_status/UCE_I12.json',f'{STATUS}/phase_status/UCE_I12_HANDOFF_TO_UCE_I13.json',f'{STATUS}/artifacts/UCE_I12_ACCEPTANCE_EVIDENCE.json',f'{STATUS}/artifacts/UCE_I12_ARTIFACT_INVENTORY.csv','src/engine/tooling/strategy_factory/check_uce_i12_boundaries.py','src/engine/tooling/strategy_factory/check_uce_i12_mql5_static.py','src/engine/tooling/strategy_factory/compile_uce_i12_statistical_promotion.ps1','src/engine/tooling/strategy_factory/generate_uce_i12_vectors.py','src/engine/tooling/strategy_factory/run_uce_i12_tests.ps1','src/engine/tooling/strategy_factory/validate_uce_i12_delivery.py','src/engine/tooling/strategy_factory/build_uce_i12_release.py']
    specific += [f'schemas/legacy/strategy_factory/v3/{n}.schema.json' for n in SCHEMAS]
    specific += [p.relative_to(root).as_posix() for p in (root/'docs/obsidian_deep/01_concepts').glob('UCE-I12_*.md')]
    for rel in specific:
        p=root/rel
        if p.is_file(): paths.add(p)
    return sorted(paths,key=lambda p:p.relative_to(root).as_posix())
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); ap.add_argument('--zip',dest='zip_path'); ap.add_argument('--phase-tests',type=int,default=86); ap.add_argument('--cumulative-tests',type=int,default=376); ap.add_argument('--engineering-checks',type=int,default=4); a=ap.parse_args(); root=Path(a.root).resolve()
    inventory=root/f'{STATUS}/artifacts/UCE_I12_ARTIFACT_INVENTORY.csv'; inventory.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in owned(root):
        if p.name in META or p==inventory: continue
        rows.append({'path':p.relative_to(root).as_posix(),'sha256':digest(p),'size_bytes':p.stat().st_size})
    with inventory.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=('path','sha256','size_bytes')); w.writeheader(); w.writerows(rows)
    # Create placeholder metadata so owned() includes them.
    for name in META:
        p=root/name
        if not p.exists(): p.write_text('',encoding='utf-8')
    paths=owned(root); rels=[p.relative_to(root).as_posix() for p in paths]
    (root/'releases/history/ucee/indexes/UCEE_I12_FILE_INDEX.txt').write_text('\n'.join(rels)+'\n',encoding='utf-8')
    generated=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    docs=list((root/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i12').glob('*.md')); concepts=list((root/'docs/obsidian_deep/01_concepts').glob('UCE-I12_*.md'))
    manifest={'patch_id':'decision-alpha-lab-ucee-i12-unified-statistical-anti-overfit-promotion-governance','patch_version':'1.0.0','phase_id':'UCE-I12','created_at_utc':generated,'title':'Unified Statistical, Anti-Overfit, and Promotion Governance Gate','authority_boundary':'offline statistical evidence and promotion governance only; no trading or network authority','python_module_count':18,'suite_count':7,'public_schema_count':len(SCHEMAS),'delivery_document_count':len(docs),'atomic_concept_count':len(concepts),'phase_test_count':a.phase_tests,'cumulative_ucee_test_count':a.cumulative_tests,'engineering_policy_check_count':a.engineering_checks,'mql5_file_count':11,'metaeditor_compile_status':'pending_local_windows','file_count':len(rels),'file_index':'releases/history/ucee/indexes/UCEE_I12_FILE_INDEX.txt','file_hashes':'releases/history/ucee/hashes/UCEE_I12_FILE_HASHES.sha256','next_phase':'UCE-I13 Manual AI Hybrid Policy Graph'}
    (root/'releases/history/ucee/manifests/UCEE_I12_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    paths=owned(root); rels=[p.relative_to(root).as_posix() for p in paths]; (root/'releases/history/ucee/indexes/UCEE_I12_FILE_INDEX.txt').write_text('\n'.join(rels)+'\n',encoding='utf-8'); manifest['file_count']=len(rels); (root/'releases/history/ucee/manifests/UCEE_I12_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    paths=owned(root); (root/'releases/history/ucee/hashes/UCEE_I12_FILE_HASHES.sha256').write_text('\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in paths if p.name!='releases/history/ucee/hashes/UCEE_I12_FILE_HASHES.sha256')+'\n',encoding='utf-8')
    if a.zip_path:
        target=Path(a.zip_path).resolve(); target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in owned(root):
                info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,7,13,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=(0o644&0xFFFF)<<16; z.writestr(info,p.read_bytes())
        print(f'{target} files={len(owned(root))} sha256={digest(target)}')
    print(json.dumps(manifest,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
