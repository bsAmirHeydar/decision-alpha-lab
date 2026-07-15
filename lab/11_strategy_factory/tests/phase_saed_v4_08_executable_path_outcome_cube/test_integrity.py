from helpers import cube
from saed_v4_outcome_cube.integrity import build_receipt
from saed_v4_outcome_cube.validation import validate_cube
def test_integrity_receipt():
 c=cube();validate_cube(c);r=build_receipt(c);assert r['complete_exposure'];assert len(r['row_merkle_root'])==64
