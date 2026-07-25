#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import argparse,json,csv,zipfile
META={'releases/history/exp0019/indexes/EXP0019_FP_I01_FILE_INDEX.txt','releases/history/exp0019/hashes/EXP0019_FP_I01_FILE_HASHES.sha256','releases/history/exp0019/manifests/EXP0019_FP_I01_PATCH_MANIFEST.json'}

def h(p):return sha256(p.read_bytes()).hexdigest()
def owned(root):
 paths=set();dirs=[
 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01',
 'mql5/Include/FaerieProtocol/EXP0019/Compatibility',
 'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i01']
 for rel in dirs:
  for p in (root/rel).rglob('*'):
   if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':paths.add(p)
 for rel in [
 'mql5/Experts/FaerieProtocolTests/EXP0019_FP_I01_CompatibilitySelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I01_CompatibilityDiagnostic.mq5',
 'releases/history/exp0019/readmes/README_EXP0019_FP_I01_COMPATIBILITY.md','releases/history/exp0019/installers/INSTALL_EXP0019_FP_I01_COMPATIBILITY.md','COMMIT_MESSAGE.md','releases/history/exp0019/reports/EXP0019_FP_I01_QA_REPORT.json',
 'tools/exp0019/check_fp_i01_boundaries.py','tools/exp0019/check_fp_i01_mql5_static.py','tools/exp0019/validate_fp_i01_delivery.py','tools/exp0019/build_fp_i01_release.py']:
  p=root/rel
  if p.is_file():paths.add(p)
 for p in (root/'docs/obsidian_deep/01_concepts').glob('EXP0019_FP_I01_*.md'):paths.add(p)
 for name in META:
  p=root/name
  if p.is_file():paths.add(p)
 return sorted(paths,key=lambda p:p.relative_to(root).as_posix())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--zip');ap.add_argument('--phase-tests',type=int,default=39);a=ap.parse_args();root=Path(a.root).resolve()
 inv=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts/FP_I01_ARTIFACT_INVENTORY.csv'
 rows=[]
 for p in owned(root):
  if p.name not in META and p.name!='FP_I01_ARTIFACT_INVENTORY.csv':rows.append({'path':p.relative_to(root).as_posix(),'sha256':h(p),'size_bytes':p.stat().st_size})
 with inv.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['path','sha256','size_bytes']);w.writeheader();w.writerows(rows)
 paths=owned(root);rels=sorted({p.relative_to(root).as_posix() for p in paths}|META)
 (root/'releases/history/exp0019/indexes/EXP0019_FP_I01_FILE_INDEX.txt').write_text('\n'.join(rels)+'\n')
 manifest={'patch_id':'decision-alpha-lab-exp0019-faerie-protocol-fp-i01-compatibility','patch_version':'1.0.0','phase_id':'FP-I01','created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'file_count':len(rels),'python_test_count':a.phase_tests,'dependency_pin_count':19,'adapter_count':8,'metaeditor_compile_status':'pending_local_windows','next_phase':'FP-I02'}
 (root/'releases/history/exp0019/manifests/EXP0019_FP_I01_PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 paths=owned(root);(root/'releases/history/exp0019/indexes/EXP0019_FP_I01_FILE_INDEX.txt').write_text('\n'.join(p.relative_to(root).as_posix() for p in paths)+'\n')
 paths=owned(root);(root/'releases/history/exp0019/hashes/EXP0019_FP_I01_FILE_HASHES.sha256').write_text('\n'.join(f'{h(p)}  {p.relative_to(root).as_posix()}' for p in paths if p.name!='releases/history/exp0019/hashes/EXP0019_FP_I01_FILE_HASHES.sha256')+'\n')
 if a.zip:
  target=Path(a.zip).resolve();target.parent.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for p in owned(root):
    info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,7,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644&0xffff)<<16;z.writestr(info,p.read_bytes())
  print(f'{target} files={len(owned(root))} sha256={h(target)}')
 print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':main()
