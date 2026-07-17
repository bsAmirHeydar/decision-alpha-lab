from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run

def main(argv=None):
    p=argparse.ArgumentParser(prog="saed-v4-36"); p.add_argument("input"); p.add_argument("--output",required=True); a=p.parse_args(argv)
    data=json.loads(Path(a.input).read_text(encoding="utf-8")); out=run(data); Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8"); return 0
if __name__=="__main__": raise SystemExit(main())
