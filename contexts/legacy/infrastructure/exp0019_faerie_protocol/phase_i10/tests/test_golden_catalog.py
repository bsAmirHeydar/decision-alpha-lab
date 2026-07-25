import json
from pathlib import Path

def test_golden_vectors():
 p=Path(__file__).resolve().parents[1]/'golden/FP_I10_GOLDEN_VECTORS.v1.json'; d=json.loads(p.read_text()); assert d['phase_id']=='FP-I10' and len(d['vectors'])==7
