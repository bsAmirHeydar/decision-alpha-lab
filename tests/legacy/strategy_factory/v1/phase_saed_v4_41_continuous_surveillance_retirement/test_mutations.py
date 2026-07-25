from copy import deepcopy
import pytest
from saed_v4_continuous_surveillance_retirement.pipeline import run_reference
from saed_v4_continuous_surveillance_retirement.errors import SAEDV441Error
MUTATIONS=['future_observation','duplicate_observation','unknown_metric','cross_tenant_observation','missing_metric','bad_policy_auto_live','bad_reinstatement','bad_constitution_live','bad_upstream_phase','bad_handoff_kind','insufficient_sample','threshold_order','duplicate_metric','unknown_policy_field','approval_future','approval_unknown_role','non_synthetic_observation','future_suffix','registry_cell_mismatch','incomplete_coverage']
@pytest.mark.parametrize('kind',MUTATIONS)
def test_fail_closed_mutations(fixture,kind):
 x=deepcopy(fixture)
 if kind=='future_observation':x['observations'][0]['known_time']='2099-01-01T00:00:00Z'
 elif kind=='duplicate_observation':x['observations'].append(deepcopy(x['observations'][0]))
 elif kind=='unknown_metric':x['observations'][0]['metric_id']='UNKNOWN'
 elif kind=='cross_tenant_observation':x['observations'][0]['tenant_id']='TENANT_99'
 elif kind=='missing_metric':x['observations'].pop()
 elif kind=='bad_policy_auto_live':x['policy']['automatic_live_action_allowed']=True
 elif kind=='bad_reinstatement':x['policy']['reinstatement_requires_new_qualification']=False
 elif kind=='bad_constitution_live':x['constitution']['live_order_submission_allowed']=True
 elif kind=='bad_upstream_phase':x['upstream_certificate']['phase']='BAD'
 elif kind=='bad_handoff_kind':x['upstream_handoff']['kind']='BAD'
 elif kind=='insufficient_sample':x['observations'][0]['sample_count']=0
 elif kind=='threshold_order':x['policy']['metrics'][0]['critical_threshold']=x['policy']['metrics'][0]['warn_threshold']
 elif kind=='duplicate_metric':x['policy']['metrics'].append(deepcopy(x['policy']['metrics'][0]))
 elif kind=='unknown_policy_field':x['policy']['unknown']=1
 elif kind=='approval_future':x['retirement_approvals'][0]['known_time']='2099-01-01T00:00:00Z'
 elif kind=='approval_unknown_role':x['retirement_approvals'][0]['role']='UNKNOWN'
 elif kind=='non_synthetic_observation':x['observations'][0]['synthetic_fixture']=False
 elif kind=='future_suffix':x['observations'][0]['future_suffix_used']=True
 elif kind=='registry_cell_mismatch':x['observations'][0]['cell_id']='UNKNOWN'
 elif kind=='incomplete_coverage':x['observations']=x['observations'][:-2000]
 with pytest.raises((SAEDV441Error,AssertionError,KeyError,ValueError)):run_reference(x)
