from __future__ import annotations
import argparse,json
from pathlib import Path
from .conformance import run_vectors

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-event-model')
    sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('conformance')
    c.add_argument('vectors')
    c.add_argument('--output')
    a=p.parse_args(argv)
    results=run_vectors(json.loads(Path(a.vectors).read_text()))
    payload={'total':len(results),'passed':sum(x['passed'] for x in results),'results':results}
    text=json.dumps(payload,indent=2,sort_keys=True)
    if a.output:Path(a.output).write_text(text+'\n')
    else:print(text)
    return 0 if payload['passed']==payload['total'] else 1
if __name__=='__main__':raise SystemExit(main())
