from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--upstream',required=True);p.add_argument('--dataset',required=True);p.add_argument('--baseline',required=True);p.add_argument('--output',required=True);a=p.parse_args(argv)
    load=lambda x:json.loads(Path(x).read_text(encoding='utf-8'))
    out=run(load(a.config),load(a.upstream),load(a.dataset),load(a.baseline));Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'
',encoding='utf-8');return 0
if __name__=='__main__':raise SystemExit(main())
