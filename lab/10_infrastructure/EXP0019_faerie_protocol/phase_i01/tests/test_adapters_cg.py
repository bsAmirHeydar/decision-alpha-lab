from copy import deepcopy
import pytest
from fp_i01_compatibility.fixtures import fixtures
from fp_i01_compatibility.adapters import run_read_only_adapter,adapt_cgr_reference,adapt_cgh_hunt
from fp_i01_compatibility.enums import *
from fp_i01_compatibility.errors import CompatibilityError

def test_all_cg_fixtures_are_read_only_and_deterministic():
    for fixture,(key,payload) in fixtures().items():
        if not key.startswith('FP_CG'):continue
        original=deepcopy(payload);out,before,after,h1,h2=run_read_only_adapter(key,payload)
        assert payload==original and before==after and h1==h2

def test_cgr_missing_field_fails_closed():
    with pytest.raises(CompatibilityError,match='missing fields'):adapt_cgr_reference({'group_name':'x'})

def test_cgr_not_ready_is_degraded_not_fabricated():
    _,payload=fixtures()['CGR_REFERENCE_READY'];payload=deepcopy(payload);payload['symbol_b']['data_ok']=False
    out=adapt_cgr_reference(payload)
    assert not out.ready and out.health is HealthState.DEGRADED

def test_cgh_one_sided_high_roles_are_exact():
    _,payload=fixtures()['CGH_HIGH_A_ONLY'];out=adapt_cgh_hunt(payload)
    assert out.side is HuntSide.HIGH and out.pair_state is PairState.A_ONLY
    assert out.hunter_symbol=='US500' and out.protected_symbol=='USTEC'

def test_unknown_adapter_rejected():
    with pytest.raises(CompatibilityError,match='unknown_adapter'):run_read_only_adapter('missing',{})
