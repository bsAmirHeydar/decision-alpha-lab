from __future__ import annotations
import argparse,json
from pathlib import Path
from .contracts import load_document,validate_closed
from .canonical import content_hash

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-data-foundation'); sub=p.add_subparsers(dest='cmd',required=True)
    v=sub.add_parser('validate'); v.add_argument('--document',required=True); v.add_argument('--schema',required=True)
    h=sub.add_parser('hash'); h.add_argument('--document',required=True)
    a=p.parse_args(argv)
    if a.cmd=='validate': validate_closed(load_document(a.document),load_document(a.schema)); print(json.dumps({'status':'pass','document':a.document,'schema':a.schema},indent=2)); return 0
    if a.cmd=='hash': print(content_hash(load_document(a.document))); return 0
    return 2
if __name__=='__main__': raise SystemExit(main())
