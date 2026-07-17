from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run

def main(argv=None)->int:
    parser=argparse.ArgumentParser(prog="saed-v4-31")
    parser.add_argument("--input",required=True); parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    inputs=json.loads(Path(args.input).read_text(encoding="utf-8")); result=run(inputs)
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
