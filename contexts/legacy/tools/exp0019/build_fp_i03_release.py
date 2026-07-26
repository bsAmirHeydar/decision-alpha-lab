#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import argparse,csv,json,zipfile
STATUS='contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03'
META={'releases/history/exp0019/indexes/EXP0019_FP_I03_FILE_INDEX.txt','releases/history/exp0019/hashes/EXP0019_FP_I03_FILE_HASHES.sha256','releases/history/exp0019/manifests/EXP0019_FP_I03_PATCH_MANIFEST.json'}

def digest(path):return sha256(path.read_bytes()).hexdigest()
def owned(root):
    paths=set()
    dirs=[STATUS,'docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i03','mql5/Include/FaerieProtocol/EXP0019/Time']
    for rel in dirs:
        base=root/rel
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':paths.add(p)
    for p in (root/'docs/history/obsidian/deep/01_concepts').glob('FP-I03_*.md'):paths.add(p)
    specific=[
      'releases/history/exp0019/readmes/README_EXP0019_FP_I03_TIME_CALENDAR.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I03_TIME_CALENDAR.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I03_QA_REPORT.json',
      'releases/history/exp0019/indexes/EXP0019_FP_I03_FILE_INDEX.txt','releases/history/exp0019/hashes/EXP0019_FP_I03_FILE_HASHES.sha256','releases/history/exp0019/manifests/EXP0019_FP_I03_PATCH_MANIFEST.json',
      'docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I03_NEW_YORK_TIME_TRADING-DAY_SESSION_AND_WEEK_KERNEL.md',
      'mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarSelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I03_TimeCalendarDiagnostic.mq5',
      'contexts/legacy/tools/exp0019/check_fp_i03_boundaries.py','contexts/legacy/tools/exp0019/check_fp_i03_mql5_static.py','contexts/legacy/tools/exp0019/generate_fp_i03_vectors.py','contexts/legacy/tools/exp0019/validate_fp_i03_delivery.py','contexts/legacy/tools/exp0019/build_fp_i03_release.py']
    for rel in specific:
        p=root/rel
        if p.is_file():paths.add(p)
    return sorted(paths,key=lambda p:p.relative_to(root).as_posix())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--zip');args=ap.parse_args();root=Path(args.root).resolve()
    # Materialize release metadata names first so the final file set is stable.
    for name in META:
        path=root/name
        if not path.exists():path.write_text('',encoding='utf-8')
    inv=root/STATUS/'artifacts/FP_I03_ARTIFACT_INVENTORY.csv';inv.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in owned(root):
        if p.name in META or p==inv:continue
        rows.append({'path':p.relative_to(root).as_posix(),'sha256':digest(p),'size_bytes':p.stat().st_size})
    with inv.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=['path','sha256','size_bytes']);w.writeheader();w.writerows(rows)
    final_paths=owned(root)
    manifest={'patch_id':'EXP0019-FP-I03-TIME-CALENDAR','patch_version':'1.0.0','phase':'FP-I03','created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'file_count':len(final_paths),'python_module_count':15,'phase_test_count':83,'cumulative_total_test_count':262,'public_schema_count':12,'public_contract_count':11,'time_reason_count':15,'mql5_include_count':12,'delivery_doc_count':53,'atomic_concept_count':7,'conformance_check_count':20,'metaeditor_compile_status':'pending_local_windows','runtime_authority':'NONE','next_phase':'FP-I04 Multi-Symbol M1 Synchronization, Coverage, and Data Revision'}
    (root/'releases/history/exp0019/indexes/EXP0019_FP_I03_FILE_INDEX.txt').write_text('\n'.join(p.relative_to(root).as_posix() for p in final_paths)+'\n',encoding='utf-8')
    (root/'releases/history/exp0019/manifests/EXP0019_FP_I03_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    final_paths=owned(root)
    (root/'releases/history/exp0019/hashes/EXP0019_FP_I03_FILE_HASHES.sha256').write_text('\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in final_paths if p.name!='releases/history/exp0019/hashes/EXP0019_FP_I03_FILE_HASHES.sha256')+'\n',encoding='utf-8')
    final_paths=owned(root)
    if len(final_paths)!=manifest['file_count']:
        raise SystemExit(f"release file-set drift: manifest={manifest['file_count']} actual={len(final_paths)}")
    if args.zip:
        target=Path(args.zip).resolve();target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in final_paths:
                info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,7,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644&0xffff)<<16;z.writestr(info,p.read_bytes())
        print(f'{target} files={len(final_paths)} sha256={digest(target)}')
    print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':main()
