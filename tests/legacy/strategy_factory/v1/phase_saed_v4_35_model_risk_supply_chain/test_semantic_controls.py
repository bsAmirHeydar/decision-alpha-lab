from copy import deepcopy
import pytest
from .conftest import FIXTURE
from saed_v4_model_risk_supply_chain import run

@pytest.mark.parametrize('field', ['production_authorization','live_trading_authority','promotion_authority'])
def test_authority_denied(field):assert run(deepcopy(FIXTURE))['authority'][field] is False

@pytest.mark.parametrize('field', ['real_signature_claim','real_scanner_claim','real_build_reproduction_claim','external_validation_claim','runtime_parity_claim','production_authorization_claim','live_trading_claim'])
def test_claims_denied(field):assert run(deepcopy(FIXTURE))['limitations'][field] is False

@pytest.mark.parametrize('name', ['models','datasets','dependencies','tools','runtimes','services'])
def test_catalogs_sorted(name):
    out=run(deepcopy(FIXTURE))[name]; ids=[next(v for k,v in r.items() if k.endswith('_id') and k not in ('owner_id','supplier_id','builder_id')) for r in out['records']]; assert ids==sorted(ids)

def test_order_invariance_catalogs():
    x=deepcopy(FIXTURE);x['dependencies']=list(reversed(x['dependencies']));x['signatures']=list(reversed(x['signatures']));x['governance_events']=list(reversed(x['governance_events']))
    a=run(deepcopy(FIXTURE));b=run(x);assert a['sbom']['sbom_hash']==b['sbom']['sbom_hash'];assert a['governance_ledger']['ledger_hash']==b['governance_ledger']['ledger_hash']

def test_future_suffix_invariance_declared():assert run(deepcopy(FIXTURE))['replay']['future_suffix_invariant']
def test_zero_quarantine_golden():assert run(deepcopy(FIXTURE))['quarantine']['item_count']==0
def test_reference_eligibility_not_production():
    e=run(deepcopy(FIXTURE))['eligibility'];assert e['reference_release_eligible'];assert not e['production_release_eligible'];assert not e['runtime_activation_allowed']
