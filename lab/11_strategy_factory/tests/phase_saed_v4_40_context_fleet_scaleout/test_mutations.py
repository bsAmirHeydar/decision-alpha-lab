from copy import deepcopy
import pytest
from saed_v4_context_fleet_scaleout import run_reference,SAEDV440Error
M=[]
# Constitution mutations
for key in ['immutable_cell_identity','tenant_isolation_required','no_mutable_global_state','idempotent_side_effects_required','journal_every_transition','fail_closed_required','baseline_preservation_required','research_only']:
 M.append((f'constitution_{key}',lambda f,k=key:f['constitution'].__setitem__(k,False)))
for key in ['automatic_live_promotion_allowed','cross_tenant_routing_allowed','live_order_submission_allowed','capital_activation_allowed','production_authorization_allowed']:
 M.append((f'constitution_forbid_{key}',lambda f,k=key:f['constitution'].__setitem__(k,True)))
# Registry mutations
M += [('registry_mutable',lambda f:f['registry'].__setitem__('immutable',False)),('cell_mutable',lambda f:f['registry']['cells'][0].__setitem__('mutable',True)),('cell_hash',lambda f:f['registry']['cells'][0].__setitem__('runtime_bundle_hash','bad')),('cell_tenant',lambda f:f['registry']['cells'][0].__setitem__('tenant_id','UNKNOWN')),('cell_duplicate',lambda f:f['registry']['cells'][1].__setitem__('cell_id',f['registry']['cells'][0]['cell_id'])),('context_duplicate',lambda f:(f['registry']['cells'][1].__setitem__('tenant_id',f['registry']['cells'][0]['tenant_id']),f['registry']['cells'][1].__setitem__('context_id',f['registry']['cells'][0]['context_id']),f['registry']['cells'][1].__setitem__('context_version',f['registry']['cells'][0]['context_version'])))]
# Resource/quota
M += [('overcommit',lambda f:f['resource_catalog'].__setitem__('overcommit_allowed',True)),('domain_unhealthy',lambda f:f['resource_catalog']['failure_domains'][0].__setitem__('healthy',False)),('quota_soft',lambda f:f['quotas'].__setitem__('hard_enforcement',False)),('quota_cells',lambda f:f['quotas']['tenant_quotas'][0].__setitem__('max_cells',1)),('quota_missing',lambda f:f['quotas']['tenant_quotas'].pop())]
# Route
M += [('route_cross_tenant',lambda f:f['routing_table']['routes'][0].__setitem__('tenant_id',f['registry']['cells'][1]['tenant_id'])),('route_cross_namespace',lambda f:f['routing_table']['routes'][0].__setitem__('namespace',f['registry']['cells'][1]['namespace'])),('route_unknown',lambda f:f['routing_table']['routes'][0].__setitem__('cell_id','UNKNOWN')),('route_weight',lambda f:f['routing_table']['routes'][0].__setitem__('weight_bps',9999)),('route_live_default',lambda f:f['routing_table'].__setitem__('default_action','ROUTE')),('route_cross_allowed',lambda f:f['routing_table'].__setitem__('cross_tenant_allowed',True)),('route_duplicate',lambda f:f['routing_table']['routes'][1].__setitem__('route_id',f['routing_table']['routes'][0]['route_id']))]
# Rollout
M += [('rollout_auto',lambda f:f['rollout_policy'].__setitem__('automatic_live_promotion_allowed',True)),('rollout_target',lambda f:f['rollout_policy'].__setitem__('rollback_target','PRODUCTION')),('rollout_ordinal',lambda f:f['rollout_policy']['waves'][1].__setitem__('ordinal',9)),('rollout_threshold',lambda f:f['rollout_policy'].__setitem__('error_rate_threshold',2.0)),('rollout_canary',lambda f:f['rollout_policy'].__setitem__('minimum_canary_cells',1000))]
# Health
M += [('health_future',lambda f:f['health_samples'][0].__setitem__('last_heartbeat','2027-01-01T00:00:00Z')),('health_suffix',lambda f:f['health_samples'][0].__setitem__('future_suffix_used',True)),('health_duplicate',lambda f:f['health_samples'][1].__setitem__('cell_id',f['health_samples'][0]['cell_id'])),('health_missing',lambda f:f['health_samples'].pop()),('health_error',lambda f:f['health_samples'][0].__setitem__('error_rate',2.0))]
# Commands/reviews/upstream
M += [('command_unapproved',lambda f:f['commands'][0].__setitem__('approved',False)),('command_live',lambda f:f['commands'][0].__setitem__('action','LIVE_ORDER')),('command_real',lambda f:f['commands'][0].__setitem__('synthetic_fixture',False)),('review_missing',lambda f:f['reviews'].pop()),('review_not_independent',lambda f:f['reviews'][0].__setitem__('independent',False)),('review_role',lambda f:f['reviews'][0].__setitem__('role','UNKNOWN')),('upstream_prod',lambda f:f['upstream_certificate'].__setitem__('production_authorized',True)),('upstream_phase',lambda f:f['upstream_handoff'].__setitem__('next_phase','SAED_V4_41')),('upstream_hash',lambda f:f['upstream_handoff'].__setitem__('release_hash','0'*64))]
@pytest.mark.parametrize('name,mut',M,ids=[x[0] for x in M])
def test_mutations_fail(fixture,name,mut):
 mut(fixture)
 with pytest.raises(SAEDV440Error):run_reference(fixture)
