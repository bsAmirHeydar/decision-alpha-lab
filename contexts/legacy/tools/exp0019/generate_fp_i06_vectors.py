#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    for rel in (
        'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python',
        'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/python',
        'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i04/python',
        'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i05/python',
        'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06/python',
    ):
        sys.path.insert(0, str(root / rel))
    from fp_i06_relations.conformance import run_conformance

    report = run_conformance()
    target = root / 'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06/artifacts/FP_I06_GOLDEN_RELATION_VECTORS.v1.json'
    if args.verify_only:
        if not target.exists():
            raise SystemExit('golden vector file missing')
        if json.loads(target.read_text(encoding='utf-8')) != report:
            raise SystemExit('FP-I06 golden vector mismatch')
        print('FP-I06 golden vector verification PASS')
        return 0
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(target)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
