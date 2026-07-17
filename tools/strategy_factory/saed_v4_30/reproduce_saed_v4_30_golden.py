from __future__ import annotations
import argparse,json
from _common import AR,MAP,reference_result,load
parser=argparse.ArgumentParser(); parser.add_argument("--write",action="store_true"); args=parser.parse_args()
result=reference_result()
for key,name in MAP.items():
 path=AR/name
 if args.write: path.write_text(json.dumps(result[key],indent=2,sort_keys=True)+"\n",encoding="utf-8")
 else:
  expected=load(path)
  if expected!=result[key]: raise SystemExit(f"golden mismatch: {name}")
print(f"V4-30 golden reproduction passed: {len(MAP)} exact artifacts")
