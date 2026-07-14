import json
from pathlib import Path
from fp_i14_diagnostic import *
def test_golden_vectors_exist():
    p=Path(__file__).resolve().parents[1]/'golden/FP_I14_GOLDEN_VECTORS.v1.json';d=json.loads(p.read_text());assert len(d['vectors'])==9
def test_all_golden_have_hash():
    p=Path(__file__).resolve().parents[1]/'golden/FP_I14_GOLDEN_VECTORS.v1.json';d=json.loads(p.read_text());assert all(len(x['expected_hash'])==64 for x in d['vectors'])
