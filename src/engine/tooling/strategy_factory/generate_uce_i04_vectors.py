#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from strategy_factory_treatment_compiler_v3.conformance import run_conformance
from strategy_factory_treatment_compiler_v3.golden import compile_golden,run_golden_paths
from strategy_factory_treatments_v3.enums import TradeSide
def dump(path,data): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,sort_keys=True,default=str)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default='.');p.add_argument('--verify-only',action='store_true');a=p.parse_args();root=Path(a.root).resolve();out=root/'tests/fixtures/legacy/strategy_factory/v3'
 expected={'uce_i04_treatment_compiler_vectors.json':run_conformance()}
 tr,paths=run_golden_paths();expected['uce_i04_golden_path_library.json']={'schema_version':'3.0.0','treatment':tr,'paths':paths}
 long,_=compile_golden(TradeSide.LONG);short,_=compile_golden(TradeSide.SHORT);runner,_=compile_golden(TradeSide.LONG,runner=True);expected['uce_i04_identity_vectors.json']={'schema_version':'3.0.0','long_fixed_r':long.to_dict(),'short_fixed_r':short.to_dict(),'long_runner':runner.to_dict()}
 failures=[]
 for name,data in expected.items():
  path=out/name
  if a.verify_only:
   if not path.exists() or json.loads(path.read_text())!=json.loads(json.dumps(data,default=str)): failures.append(name)
  else: dump(path,data)
 if failures: print('vector mismatch: '+','.join(failures));return 1
 print('UCE-I04 vectors '+('verified' if a.verify_only else 'generated'));return 0
if __name__=='__main__': raise SystemExit(main())
