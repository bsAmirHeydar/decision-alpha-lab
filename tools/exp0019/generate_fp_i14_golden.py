from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2];p=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i14/golden/FP_I14_GOLDEN_VECTORS.v1.json';d=json.loads(p.read_text());
assert all(v['expected_hash']==hashlib.sha256(v['name'].encode()).hexdigest() for v in d['vectors']);print(json.dumps({'vectors':len(d['vectors']),'status':'PASS'},indent=2))
