from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run
def main():
    p=argparse.ArgumentParser(description="SAED V4-35 model-risk and supply-chain deterministic reference");p.add_argument("input");p.add_argument("--output",required=True);a=p.parse_args()
    result=run(json.loads(Path(a.input).read_text(encoding="utf-8")));Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__":main()
