from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run_reference

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--upstream',required=True);ap.add_argument('--paths',required=True);ap.add_argument('--policy',required=True);ap.add_argument('--output',required=True);ns=ap.parse_args(argv)
    load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
    out=run_reference(load(ns.config),load(ns.upstream),load(ns.paths),load(ns.policy));Path(ns.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'
',encoding='utf-8');return 0
if __name__=='__main__':raise SystemExit(main())
