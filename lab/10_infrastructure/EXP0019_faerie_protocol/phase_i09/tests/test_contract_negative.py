import pytest
from fp_i09_ledger.contracts import PairSessionQuotaKey
from fp_i09_ledger.errors import FPI09Error

def test_bad_hash_rejected():
    with pytest.raises(FPI09Error): PairSessionQuotaKey('Q','E','D','P','S','N','bad')
