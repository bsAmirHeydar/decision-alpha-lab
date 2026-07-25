#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import argparse,csv,json,zipfile
STATUS='lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05'
META={'releases/history/exp0019/indexes/EXP0019_FP_I05_FILE_INDEX.txt','releases/history/exp0019/hashes/EXP0019_FP_I05_FILE_HASHES.sha256','releases/history/exp0019/manifests/EXP0019_FP_I05_PATCH_MANIFEST.json'}
def digest(path):return sha256(path.read_bytes()).hexdigest()
def owned(root):
    paths=set();dirs=[STATUS,'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i05','mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I05']
    for rel in dirs:
        base=root/rel
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':paths.add(p)
    for p in (root/'docs/obsidian_deep/01_concepts').glob('FP-I05_*.md'):paths.add(p)
    specific=['releases/history/exp0019/readmes/README_EXP0019_FP_I05_REFERENCE_ENGINE.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I05_REFERENCE_ENGINE.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I05_QA_REPORT.json','releases/history/exp0019/indexes/EXP0019_FP_I05_FILE_INDEX.txt','releases/history/exp0019/hashes/EXP0019_FP_I05_FILE_HASHES.sha256','releases/history/exp0019/manifests/EXP0019_FP_I05_PATCH_MANIFEST.json','docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I05_SESSION_WEEK_WINDOW_STORE_CALENDAR-DAY_SELECTOR_AND_REFERENCE_ENGINE.md','mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I05_ReferenceDiagnostic.mq5','mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I05_ReferenceSelfTest.mq5','tools/exp0019/check_fp_i05_boundaries.py','tools/exp0019/check_fp_i05_mql5_static.py','tools/exp0019/generate_fp_i05_vectors.py','tools/exp0019/validate_fp_i05_delivery.py','tools/exp0019/build_fp_i05_release.py']
    for rel in specific:
        p=root/rel
        if p.is_file():paths.add(p)
    return sorted(paths,key=lambda p:p.relative_to(root).as_posix())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--zip');args=ap.parse_args();root=Path(args.root).resolve()
    for name in META:
        p=root/name
        if not p.exists():p.write_text('',encoding='utf-8')
    inv=root/STATUS/'artifacts/FP_I05_ARTIFACT_INVENTORY.csv';inv.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in owned(root):
        if p.name in META or p==inv:continue
        rows.append({'path':p.relative_to(root).as_posix(),'sha256':digest(p),'size_bytes':p.stat().st_size})
    with inv.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=['path','sha256','size_bytes']);w.writeheader();w.writerows(rows)
    final=owned(root)
    status=json.loads((root/STATUS/'artifacts/FP_I05_PHASE_STATUS.json').read_text())
    manifest={'patch_id':'EXP0019-FP-I05-REFERENCE-ENGINE','patch_version':'1.0.0','phase':'FP-I05','created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'file_count':len(final),'python_module_count':17,'phase_test_count':51,'cumulative_fp_test_count':330,'previous_context_regression_count':50,'total_executed_test_count':380,'public_schema_count':12,'public_contract_count':12,'reference_reason_count':status['reference_reason_count'],'mql5_include_count':9,'delivery_doc_count':35,'atomic_concept_count':7,'conformance_check_count':5,'metaeditor_compile_status':'pending_local_windows','runtime_authority':'NONE','next_phase':'FP-I06 Relation Compiler, Hunt Facts, First-Sweep Classification, and Candidates'}
    (root/'releases/history/exp0019/indexes/EXP0019_FP_I05_FILE_INDEX.txt').write_text('\n'.join(p.relative_to(root).as_posix() for p in final)+'\n',encoding='utf-8')
    (root/'releases/history/exp0019/manifests/EXP0019_FP_I05_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    final=owned(root)
    (root/'releases/history/exp0019/hashes/EXP0019_FP_I05_FILE_HASHES.sha256').write_text('\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in final if p.name!='releases/history/exp0019/hashes/EXP0019_FP_I05_FILE_HASHES.sha256')+'\n',encoding='utf-8')
    final=owned(root);manifest['file_count']=len(final);(root/'releases/history/exp0019/manifests/EXP0019_FP_I05_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    if args.zip:
        target=Path(args.zip).resolve();target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in final:
                info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,7,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644&0xffff)<<16;z.writestr(info,p.read_bytes())
        print(f'{target} files={len(final)} sha256={digest(target)}')
    print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':main()
