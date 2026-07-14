import pytest
from fp_i09_ledger.identity import build_quota_key
from fp_i09_ledger.errors import FPI09Error

def test_quota_key_deterministic(qkey): assert qkey==build_quota_key('EPOCH-1','NYDAY-2026-09-08','PAIR-ES-NQ','NYDAY-2026-09-08:N','N')
def test_session_kind_changes_key(qkey): assert qkey.quota_key_id!=build_quota_key('EPOCH-1','NYDAY-2026-09-08','PAIR-ES-NQ','NYDAY-2026-09-08:L','L').quota_key_id
def test_pair_changes_key(qkey): assert qkey.quota_key_id!=build_quota_key('EPOCH-1','NYDAY-2026-09-08','PAIR-X-Y','NYDAY-2026-09-08:N','N').quota_key_id
def test_invalid_session_kind():
    with pytest.raises(FPI09Error): build_quota_key('E','D','P','S','W')
