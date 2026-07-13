from copy import deepcopy
from fp_i01_compatibility.fixtures import fixtures
from fp_i01_compatibility.adapters import run_read_only_adapter,adapt_daye_confirmation,adapt_daye_lifecycle
from fp_i01_compatibility.enums import *

def test_all_daye_fixtures_are_read_only_and_deterministic():
    for fixture,(key,payload) in fixtures().items():
        if 'DAYE' not in key:continue
        original=deepcopy(payload);out,before,after,h1,h2=run_read_only_adapter(key,payload)
        assert payload==original and before==after and h1==h2

def test_daye_low_confirmation_maps_to_bullish():
    _,payload=fixtures()['DAYE_CONFIRM_CONFIRMED'];out=adapt_daye_confirmation(payload)
    assert out.side is HuntSide.LOW and out.direction is Direction.BULLISH
    assert out.outcome is ConfirmationOutcome.CONFIRMED and out.immutable

def test_daye_lifecycle_preserves_counts_and_retirement():
    _,payload=fixtures()['DAYE_LIFECYCLE_SURVIVES'];out=adapt_daye_lifecycle(payload)
    assert (out.accepted_use_count,out.duplicate_use_count,out.rejected_use_count)==(2,1,0)
    assert not out.retired and out.state=='PROTECTED_SURVIVES'
