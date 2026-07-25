from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import run

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--input-dir",required=True); parser.add_argument("--output-dir",required=True); args=parser.parse_args()
    src=Path(args.input_dir); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    def load(name): return json.loads((src/name).read_text(encoding="utf-8"))
    result=run(load("FULL_REFERENCE_CONFIG.JSON"),load("UPSTREAM_V4_29_DOCUMENTS.JSON"),load("REPLICATION_PROTOCOL.JSON"),load("REPLICATION_PACKAGE_MANIFEST.JSON"),load("REPLICATION_LABS.JSON"),load("LAB_ENVIRONMENTS.JSON"),load("SYNTHETIC_REPLICATION_PAYLOAD.JSON"))
    for key,value in result.items(): (out/(key.upper()+".JSON")).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
