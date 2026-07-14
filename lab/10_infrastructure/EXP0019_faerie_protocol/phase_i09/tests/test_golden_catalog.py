import json
from pathlib import Path

def test_golden_vector_catalog_is_complete():
    p=Path(__file__).resolve().parents[1]/'artifacts/FP_I09_GOLDEN_ARBITRATION_VECTORS.v1.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    assert d['phase_id']=='FP-I09' and len(d['vectors'])==6
    assert len({x['id'] for x in d['vectors']})==6
