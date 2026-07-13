#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse,csv,json,zipfile

META={'EXP0019_FP_I02_FILE_INDEX.txt','EXP0019_FP_I02_FILE_HASHES.sha256','EXP0019_FP_I02_PATCH_MANIFEST.json'}
PHASE='lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02'
DOC='docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i02'

def digest(path:Path)->str:return sha256(path.read_bytes()).hexdigest()

def owned(root:Path)->list[Path]:
    paths:set[Path]=set()
    for rel in (PHASE,'mql5/Include/FaerieProtocol/EXP0019/Core',DOC):
        base=root/rel
        if base.exists():
            for path in base.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix!='.pyc':paths.add(path)
    specific=[
        'mql5/Experts/FaerieProtocolTests/EXP0019_FP_I02_ContractKernelSelfTest.mq5',
        'mql5/Experts/FaerieProtocol/EXP0019_FP_I02_ContractKernelDiagnostic.mq5',
        'README_EXP0019_FP_I02_CORE_KERNEL.md','INSTALL_EXP0019_FP_I02_CORE_KERNEL.md','COMMIT_MESSAGE.md','EXP0019_FP_I02_QA_REPORT.json',
        'tools/exp0019/check_fp_i02_boundaries.py','tools/exp0019/check_fp_i02_mql5_static.py','tools/exp0019/generate_fp_i02_vectors.py',
        'tools/exp0019/validate_fp_i02_delivery.py','tools/exp0019/build_fp_i02_release.py',
        'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/fp_implementation_phase_registry.v1.json',
        'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/fp_implementation_task_ledger.v1.csv',
    ]
    for rel in specific:
        path=root/rel
        if path.is_file():paths.add(path)
    for path in (root/'docs/obsidian_deep/01_concepts').glob('FP-I02_*.md'):paths.add(path)
    for name in META:
        path=root/name
        if path.is_file():paths.add(path)
    return sorted(paths,key=lambda p:p.relative_to(root).as_posix())

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--zip');ap.add_argument('--phase-tests',type=int,default=64);ap.add_argument('--cumulative-tests',type=int,default=129);args=ap.parse_args()
    root=Path(args.root).resolve()
    inventory=root/f'{PHASE}/artifacts/FP_I02_ARTIFACT_INVENTORY.csv'
    rows=[]
    for path in owned(root):
        if path.name not in META and path.name!='FP_I02_ARTIFACT_INVENTORY.csv':
            rows.append({'path':path.relative_to(root).as_posix(),'sha256':digest(path),'size_bytes':path.stat().st_size})
    with inventory.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=['path','sha256','size_bytes']);writer.writeheader();writer.writerows(rows)
    initial=owned(root)
    rels=sorted({p.relative_to(root).as_posix() for p in initial}|META)
    (root/'EXP0019_FP_I02_FILE_INDEX.txt').write_text('\n'.join(rels)+'\n',encoding='utf-8')
    manifest={
        'patch_id':'decision-alpha-lab-exp0019-faerie-protocol-fp-i02-core-kernel','patch_version':'1.0.0','phase_id':'FP-I02',
        'title':'Core Context Types, Identity, Configuration, Reason Codes, Relations, State Machines, and Schemas',
        'created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
        'file_count':len(rels),'python_module_count':16,'phase_test_count':args.phase_tests,'cumulative_fp_test_count':args.cumulative_tests,
        'public_schema_count':18,'relation_count':7,'reason_code_count':35,'public_contract_count':16,'state_machine_count':4,
        'mql5_include_count':11,'mql5_entrypoint_count':2,'runtime_authority':'NONE','open_decisions':['FP-DEC-012'],
        'metaeditor_compile_status':'pending_local_windows','next_phase':'FP-I03 New York Time, Trading-Day, Session, and Week Kernel',
        'file_index':'EXP0019_FP_I02_FILE_INDEX.txt','file_hashes':'EXP0019_FP_I02_FILE_HASHES.sha256',
    }
    (root/'EXP0019_FP_I02_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    paths=owned(root)
    (root/'EXP0019_FP_I02_FILE_INDEX.txt').write_text('\n'.join(p.relative_to(root).as_posix() for p in paths)+'\n',encoding='utf-8')
    paths=owned(root)
    (root/'EXP0019_FP_I02_FILE_HASHES.sha256').write_text('\n'.join(f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in paths if p.name!='EXP0019_FP_I02_FILE_HASHES.sha256')+'\n',encoding='utf-8')
    if args.zip:
        target=Path(args.zip).resolve();target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for path in owned(root):
                info=zipfile.ZipInfo(path.relative_to(root).as_posix(),(2026,7,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644&0xffff)<<16
                archive.writestr(info,path.read_bytes())
        print(f'{target} files={len(owned(root))} sha256={digest(target)}')
    print(json.dumps(manifest,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
