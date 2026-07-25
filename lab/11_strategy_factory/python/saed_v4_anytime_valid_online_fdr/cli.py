from __future__ import annotations
import argparse, json
from pathlib import Path
from .service import run

def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--upstream",required=True); p.add_argument("--hypotheses",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    load=lambda x:json.loads(Path(x).read_text(encoding="utf-8"))
    out=run(load(a.config),load(a.upstream),load(a.hypotheses)); Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
