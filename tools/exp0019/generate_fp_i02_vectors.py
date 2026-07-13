#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

root=Path(__file__).resolve().parents[2]
pyroot=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python'
sys.path.insert(0,str(pyroot))
from fp_i02_kernel.golden import golden_vector_material

parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
target=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/artifacts/FP_I02_GOLDEN_IDENTITY_VECTORS.v1.json'
expected=json.dumps(golden_vector_material(),indent=2,sort_keys=True)+'\n'
if args.verify_only:
    if not target.exists() or target.read_text(encoding='utf-8')!=expected:
        print('FP-I02 vector mismatch');raise SystemExit(1)
    print('FP-I02 golden vectors PASS')
else:
    target.write_text(expected,encoding='utf-8');print(target)
