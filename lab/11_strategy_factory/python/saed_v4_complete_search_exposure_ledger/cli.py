from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .service import run

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def main(argv=None):
    p=argparse.ArgumentParser(prog="saed-v4-27-ledger")
    p.add_argument("--config",required=True); p.add_argument("--upstream",required=True); p.add_argument("--manifests",required=True); p.add_argument("--trials",required=True); p.add_argument("--exposures",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(argv); out=run(load(a.config),load(a.upstream),load(a.manifests),load(a.trials),load(a.exposures)); Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8"); return 0
if __name__=="__main__": raise SystemExit(main())
