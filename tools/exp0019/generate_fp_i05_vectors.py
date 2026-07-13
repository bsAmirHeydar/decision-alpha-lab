#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    root=Path(args.root).resolve()
    for rel in ('lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05/python'):
        sys.path.insert(0,str(root/rel))
    from fp_i05_reference.conformance import run_conformance
    report=run_conformance();target=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05/artifacts/FP_I05_GOLDEN_REFERENCE_VECTORS.v1.json'
    if args.verify_only:
        if not target.exists():raise SystemExit('golden vector file missing')
        existing=json.loads(target.read_text())
        if existing!=report:raise SystemExit('FP-I05 golden vector mismatch')
        print('FP-I05 golden vector verification PASS');return 0
    target.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(target);return 0
if __name__=='__main__':raise SystemExit(main())
