#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
parser=argparse.ArgumentParser();parser.add_argument('root',nargs='?',default='.');parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
root=Path(args.root).resolve();sys.path[:0]=[str(root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python'),str(root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/python')]
from fp_i02_kernel.canonical import canonical_value
from fp_i03_time.golden import golden_vector_material
path=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/artifacts/FP_I03_GOLDEN_TIME_VECTORS.v1.json'
expected=json.dumps(canonical_value(golden_vector_material()),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
if args.verify_only:
    if not path.is_file() or path.read_text(encoding='utf-8')!=expected:
        print('FP-I03 golden vector mismatch');raise SystemExit(1)
    print('FP-I03 golden vector verification PASS: '+golden_vector_material()['vector_hash'])
else:
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(expected,encoding='utf-8');print(path)
