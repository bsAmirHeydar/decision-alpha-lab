import json
from pathlib import Path
def test_golden_vectors():
 p=Path(__file__).resolve().parents[1]/'artifacts/FP_I12_GOLDEN_VECTORS.v1.json';d=json.loads(p.read_text());assert len(d['vectors'])>=7 and all(len(x['expected_hash'])==64 for x in d['vectors'])
