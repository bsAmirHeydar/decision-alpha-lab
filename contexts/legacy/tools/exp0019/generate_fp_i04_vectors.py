#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
parser=argparse.ArgumentParser();parser.add_argument('root',nargs='?',default='.');parser.add_argument('--verify-only',action='store_true');args=parser.parse_args();root=Path(args.root).resolve()
for rel in ('contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/python','contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i04/python'):sys.path.insert(0,str(root/rel))
from fp_i04_data.conformance import run_conformance
from fp_i04_data.registry import contract_registry,reason_registry
from fp_i02_kernel.canonical import canonical_value
expected={'FP_I04_CONFORMANCE_REPORT.json':canonical_value(run_conformance()),'FP_I04_DATA_CONTRACT_REGISTRY.v1.json':canonical_value(contract_registry()),'FP_I04_DATA_REASON_REGISTRY.v1.json':canonical_value(reason_registry())}
base=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i04/artifacts';errors=[]
for name,value in expected.items():
    path=base/name;render=json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.verify_only:
        if not path.exists() or json.loads(path.read_text())!=value:errors.append('vector drift '+name)
    else:path.write_text(render,encoding='utf-8')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('FP-I04 vector verification PASS: conformance, contract registry, and reason registry match executable code.')
