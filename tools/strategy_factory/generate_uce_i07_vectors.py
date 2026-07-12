from pathlib import Path
import argparse,json,sys

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+"\n"
def main():
 p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default='.');p.add_argument('--verify-only',action='store_true');a=p.parse_args();root=Path(a.root).resolve();sys.path.insert(0,str(root/'lab/11_strategy_factory/python'))
 from strategy_factory_trainers_v3.conformance import run_conformance
 from strategy_factory_trainers_v3.registry import TrainerRegistry
 from strategy_factory_trainers_v3.reference_trainers import register_reference_trainers
 from dataclasses import asdict
 result=run_conformance();reg=TrainerRegistry();register_reference_trainers(reg)
 registry={'release':'UCE-I07','entries':[asdict(x) for x in reg.snapshot()]}
 def default(x):return x.value if hasattr(x,'value') else str(x)
 target=root/'lab/11_strategy_factory/test_vectors/v3/uce_i07_trainer_conformance_vectors.json';payload=json.dumps(result,indent=2,sort_keys=True,default=default)+"\n"
 rtarget=root/'lab/11_strategy_factory/test_vectors/v3/uce_i07_registry_snapshot.json';rpayload=json.dumps(registry,indent=2,sort_keys=True,default=default)+"\n"
 if a.verify_only:
  bad=[]
  if not target.exists() or target.read_text(encoding='utf-8')!=payload:bad.append(str(target))
  if not rtarget.exists() or rtarget.read_text(encoding='utf-8')!=rpayload:bad.append(str(rtarget))
  if bad:print('stale vectors:\n'+'\n'.join(bad));return 1
  print('UCE-I07 vector verification PASS');return 0
 target.parent.mkdir(parents=True,exist_ok=True);target.write_text(payload,encoding='utf-8');rtarget.write_text(rpayload,encoding='utf-8');print('generated',target,rtarget);return 0
if __name__=='__main__':raise SystemExit(main())
