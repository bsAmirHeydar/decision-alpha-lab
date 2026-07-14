from __future__ import annotations
import argparse,json
from pathlib import Path
from .conformance import run_vectors
def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-views');sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('conformance');c.add_argument('vectors');c.add_argument('--out')
    args=p.parse_args(argv)
    data=json.loads(Path(args.vectors).read_text());result=run_vectors(data);payload={'total':len(result),'passed':sum(x['passed'] for x in result),'results':result}
    text=json.dumps(payload,indent=2,sort_keys=True)
    if args.out:Path(args.out).write_text(text+'
')
    else:print(text)
    return 0 if payload['passed']==payload['total'] else 1
if __name__=='__main__':raise SystemExit(main())
