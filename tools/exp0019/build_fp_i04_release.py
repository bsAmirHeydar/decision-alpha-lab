#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import argparse,csv,json,zipfile
STATUS='lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04';META={'EXP0019_FP_I04_FILE_INDEX.txt','EXP0019_FP_I04_FILE_HASHES.sha256','EXP0019_FP_I04_PATCH_MANIFEST.json'}
def digest(path):return sha256(path.read_bytes()).hexdigest()
def owned(root):
    paths=set();dirs=[STATUS,'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i04','mql5/Include/FaerieProtocol/EXP0019/Data']
    for rel in dirs:
        base=root/rel
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':paths.add(p)
    for p in (root/'docs/obsidian_deep/01_concepts').glob('FP-I04_*.md'):paths.add(p)
    specific=['README_EXP0019_FP_I04_DATA_SYNC.md','INSTALL_EXP0019_FP_I04_DATA_SYNC.md','COMMIT_MESSAGE.md','EXP0019_FP_I04_QA_REPORT.json','EXP0019_FP_I04_FILE_INDEX.txt','EXP0019_FP_I04_FILE_HASHES.sha256','EXP0019_FP_I04_PATCH_MANIFEST.json','docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I04_MULTI-SYMBOL_M1_SYNCHRONIZATION_COVERAGE_AND_DATA_REVISION.md','mql5/Experts/FaerieProtocolTests/EXP0019_FP_I04_DataSyncSelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncDiagnostic.mq5','tools/exp0019/check_fp_i04_boundaries.py','tools/exp0019/check_fp_i04_mql5_static.py','tools/exp0019/generate_fp_i04_vectors.py','tools/exp0019/validate_fp_i04_delivery.py','tools/exp0019/build_fp_i04_release.py']
    for rel in specific:
        p=root/rel
        if p.is_file():paths.add(p)
    return sorted(paths,key=lambda p:p.relative_to(root).as_posix())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--zip');args=ap.parse_args();root=Path(args.root).resolve()
    for name in META:
        p=root/name
        if not p.exists():p.write_text('',encoding='utf-8')
    inv=root/STATUS/'artifacts/FP_I04_ARTIFACT_INVENTORY.csv';inv.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in owned(root):
        if p.name in META or p==inv:continue
        rows.append({'path':p.relative_to(root).as_posix(),'sha256':digest(p),'size_bytes':p.stat().st_size})
    with inv.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=['path','sha256','size_bytes']);w.writeheader();w.writerows(rows)
    final=owned(root)
    manifest={'patch_id':'EXP0019-FP-I04-DATA-SYNC','patch_version':'1.0.0','phase':'FP-I04','created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'file_count':len(final),'python_module_count':18,'phase_test_count':67,'cumulative_fp_test_count':279,'previous_context_regression_count':50,'total_executed_test_count':329,'public_schema_count':15,'public_contract_count':15,'data_reason_count':30,'mql5_include_count':13,'delivery_doc_count':57,'atomic_concept_count':7,'conformance_check_count':10,'metaeditor_compile_status':'pending_local_windows','runtime_authority':'NONE','next_phase':'FP-I05 Session/Week Window Store, Calendar-Day Selector, and Reference Engine'}
    (root/'EXP0019_FP_I04_FILE_INDEX.txt').write_text('\n'.join(p.relative_to(root).as_posix() for p in final)+'\n',encoding='utf-8')
    (root/'EXP0019_FP_I04_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    final=owned(root)
    (root/'EXP0019_FP_I04_FILE_HASHES.sha256').write_text('\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in final if p.name!='EXP0019_FP_I04_FILE_HASHES.sha256')+'\n',encoding='utf-8')
    final=owned(root)
    manifest['file_count']=len(final);(root/'EXP0019_FP_I04_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    if args.zip:
        target=Path(args.zip).resolve();target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in final:
                info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,7,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644&0xffff)<<16;z.writestr(info,p.read_bytes())
        print(f'{target} files={len(final)} sha256={digest(target)}')
    print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':main()
