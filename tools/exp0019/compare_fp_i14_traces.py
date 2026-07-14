from pathlib import Path
import argparse,json,hashlib
ap=argparse.ArgumentParser();ap.add_argument('left',type=Path);ap.add_argument('right',type=Path);a=ap.parse_args()
def load(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
l,r=load(a.left),load(a.right);print(json.dumps({'left_records':len(l),'right_records':len(r),'exact_equal':l==r,'left_hash':hashlib.sha256(json.dumps(l,sort_keys=True).encode()).hexdigest(),'right_hash':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()},indent=2));raise SystemExit(0 if l==r else 1)
