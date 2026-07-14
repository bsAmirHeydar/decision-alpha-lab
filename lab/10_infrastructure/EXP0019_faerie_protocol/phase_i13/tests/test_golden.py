from pathlib import Path
import json
def test_golden_catalog_present():
 p=Path(__file__).resolve().parents[1]/'golden/FP_I13_GOLDEN_VECTORS.v1.json';d=json.load(open(p));assert len(d['vectors'])>=8
