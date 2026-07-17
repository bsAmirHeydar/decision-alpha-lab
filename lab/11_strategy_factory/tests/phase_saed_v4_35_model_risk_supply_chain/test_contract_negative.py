from copy import deepcopy
import pytest
from conftest import FIXTURE
from saed_v4_model_risk_supply_chain import run
from saed_v4_model_risk_supply_chain.errors import SAEDV435Error

MUTATIONS=[
 lambda x:x['models'][0].__setitem__('unknown_field',1),
 lambda x:x['constitution'].__setitem__('unsigned_artifacts_allowed',True),
 lambda x:x['upstream_documents'][0].__setitem__('document_hash','bad'),
 lambda x:x['models'][0].__setitem__('known_time','2099-01-01T00:00:00Z'),
 lambda x:x['models'][0].__setitem__('immutable',False),
 lambda x:x['dependencies'][0].__setitem__('status','unapproved'),
 lambda x:x['license_policy'].__setitem__('unknown_license_action','ALLOW'),
 lambda x:x['build_statements'][0].__setitem__('network_disabled',False),
 lambda x:x['build_statements'][0].__setitem__('hermetic',False),
 lambda x:x['signatures'][0].__setitem__('revoked',True),
 lambda x:x['signatures'][0].__setitem__('algorithm','NONE'),
 lambda x:x['model_cards'][0].__setitem__('known_failure_modes',[]),
 lambda x:x['data_cards'][0].__setitem__('known_time_policy','PERMISSIVE'),
 lambda x:x['validation_plan'].__setitem__('research_only',False),
 lambda x:x['validation_plan'].__setitem__('security_test_required',False),
 lambda x:x['three_lines_assignments'][0].__setitem__('line',4),
 lambda x:x['committee_review'].__setitem__('decision','ACCEPT_PRODUCTION'),
 lambda x:x['independent_audit'].__setitem__('independent',False),
 lambda x:x['exceptions'][0].__setitem__('production_scope_allowed',True),
 lambda x:x['incident_plan'].__setitem__('tabletop_completed',False),
 lambda x:x['recall_plan'].__setitem__('drill_completed',False),
]
@pytest.mark.parametrize('mutator',MUTATIONS)
def test_fail_closed_mutations(mutator):
    x=deepcopy(FIXTURE);mutator(x)
    with pytest.raises((SAEDV435Error,KeyError,TypeError,ValueError)):run(x)

def test_signature_gap_rejected():
    x=deepcopy(FIXTURE);x['signatures']=x['signatures'][:-1]
    with pytest.raises(SAEDV435Error):run(x)

def test_dependency_cycle_rejected():
    x=deepcopy(FIXTURE);a=x['dependencies'][0]['dependency_id'];b=x['dependencies'][1]['dependency_id'];x['dependency_edges'] += [{'source_id':a,'target_id':b,'relation':'depends-on','optional':False},{'source_id':b,'target_id':a,'relation':'depends-on','optional':False}]
    with pytest.raises(SAEDV435Error):run(x)
