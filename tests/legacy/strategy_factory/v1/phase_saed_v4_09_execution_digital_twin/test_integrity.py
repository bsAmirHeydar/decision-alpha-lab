import copy, pytest
from .helpers import built
from saed_v4_execution_twin.integrity import build_integrity_receipt
from saed_v4_execution_twin.validation import validate_twin
from saed_v4_execution_twin.errors import IntegrityError

def test_integrity_receipt_is_deterministic():
    *_,twin=built();assert build_integrity_receipt(twin)==build_integrity_receipt(copy.deepcopy(twin))

def test_row_mutation_is_detected():
    *_,twin=built();twin=copy.deepcopy(twin);twin['rows'][0]['adjusted_net_r']+=1
    with pytest.raises(IntegrityError):validate_twin(twin)
