from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib,json
root=find_repository_root(__file__);p=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i14/golden/FP_I14_GOLDEN_VECTORS.v1.json';d=json.loads(p.read_text());
assert all(v['expected_hash']==hashlib.sha256(v['name'].encode()).hexdigest() for v in d['vectors']);print(json.dumps({'vectors':len(d['vectors']),'status':'PASS'},indent=2))
