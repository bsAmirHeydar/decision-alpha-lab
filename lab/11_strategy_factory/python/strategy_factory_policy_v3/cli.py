from __future__ import annotations
import argparse,json
from .registry import registry_snapshot
from .conformance import generate_vectors,verify_vectors

def main(argv=None):
    p=argparse.ArgumentParser(prog='strategy-factory-policy-v3'); p.add_argument('command',choices=('registry','golden','verify')); p.add_argument('--input'); a=p.parse_args(argv)
    if a.command=='registry': out=registry_snapshot()
    elif a.command=='golden': out=generate_vectors()
    else:
        if not a.input: p.error('--input is required for verify')
        out={'valid':verify_vectors(json.load(open(a.input,encoding='utf-8')))}
    print(json.dumps(out,sort_keys=True,separators=(',',':'))); return 0
if __name__=='__main__': raise SystemExit(main())
