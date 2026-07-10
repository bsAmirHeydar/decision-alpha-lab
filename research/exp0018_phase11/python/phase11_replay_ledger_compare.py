#!/usr/bin/env python3
"""Compare two EXP0018 P11 replay outputs by canonical immutable identities.

No third-party packages. The command fails when result/use/reference identities or
final hashes differ. It is intended for chunk-size, restart-from-zero, machine,
and broker-history equivalence checks.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path


def rows(path: Path, key: str):
    with path.open(newline='', encoding='utf-8-sig') as f:
        data=list(csv.DictReader(f))
    return {r[key]: r for r in data if r.get(key)}


def digest(mapping):
    payload='\n'.join(json.dumps(mapping[k], sort_keys=True, ensure_ascii=False) for k in sorted(mapping))
    return hashlib.sha256(payload.encode()).hexdigest()


def compare(left: Path, right: Path, suffix: str, key: str):
    a=rows(left/f'{left.name}_{suffix}.csv', key)
    b=rows(right/f'{right.name}_{suffix}.csv', key)
    return {'suffix':suffix,'left_count':len(a),'right_count':len(b),'left_digest':digest(a),'right_digest':digest(b),'equal':a==b,
            'left_only':sorted(set(a)-set(b))[:20],'right_only':sorted(set(b)-set(a))[:20]}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('left', type=Path, help='directory named with output prefix')
    ap.add_argument('right', type=Path)
    ap.add_argument('--report', type=Path)
    ns=ap.parse_args()
    checks=[compare(ns.left,ns.right,'confirmations','result_id'),compare(ns.left,ns.right,'references','reference_id'),compare(ns.left,ns.right,'uses','use_id')]
    result={'equal':all(x['equal'] for x in checks),'checks':checks}
    text=json.dumps(result,indent=2,ensure_ascii=False)
    print(text)
    if ns.report: ns.report.write_text(text,encoding='utf-8')
    raise SystemExit(0 if result['equal'] else 1)
if __name__=='__main__': main()
