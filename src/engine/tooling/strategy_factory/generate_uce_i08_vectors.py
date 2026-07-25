from pathlib import Path
import argparse,json,sys
from dataclasses import asdict
def default(x):return x.value if hasattr(x,'value') else str(x)
def main():
 q=argparse.ArgumentParser();q.add_argument('root',nargs='?',default='.');q.add_argument('--verify-only',action='store_true');a=q.parse_args();root=Path(a.root).resolve();sys.path.insert(0,str(root/'src/engine/packages'))
 from strategy_factory_classical_v3 import run_conformance,ClassicalAlgorithmRegistry
 c=run_conformance();s=ClassicalAlgorithmRegistry().freeze().snapshot();payload=json.dumps(c,indent=2,sort_keys=True,default=default)+'\n';sp=json.dumps(asdict(s),indent=2,sort_keys=True,default=default)+'\n';targets=[(root/'tests/fixtures/legacy/strategy_factory/v3/uce_i08_classical_conformance_vectors.json',payload),(root/'tests/fixtures/legacy/strategy_factory/v3/uce_i08_algorithm_registry_snapshot.json',sp)]
 if a.verify_only:
  bad=[str(f) for f,x in targets if not f.exists() or f.read_text(encoding='utf-8')!=x]
  if bad:print('stale vectors:\n'+'\n'.join(bad));return 1
  print('UCE-I08 vector verification PASS');return 0
 for f,x in targets:f.parent.mkdir(parents=True,exist_ok=True);f.write_text(x,encoding='utf-8')
 return 0
if __name__=='__main__':raise SystemExit(main())
