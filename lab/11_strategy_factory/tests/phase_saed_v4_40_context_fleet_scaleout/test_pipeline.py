from copy import deepcopy
from saed_v4_context_fleet_scaleout import run_reference

def test_reference_deterministic(fixture):
 a=run_reference(deepcopy(fixture));b=run_reference(deepcopy(fixture));assert a==b

def test_scale_target(fixture):
 o=run_reference(fixture);assert o['release']['cell_count']==128;assert o['release']['replica_count']>=200;assert o['manifest']['fleet_merkle_root'];assert o['reconciliation']['reconciled'] is True

def test_authority_closed(fixture):
 o=run_reference(fixture);assert o['authority']['may_submit_live_order'] is False;assert o['release']['live_order_submission_allowed'] is False;assert o['certificate']['production_authorized'] is False;assert o['control_journal']['live_order_side_effects']==0

def test_future_suffix_invariant(fixture):
 a=run_reference(deepcopy(fixture));x=deepcopy(fixture);x['occurrences'].append({**x['occurrences'][-1],'occurrence_id':'FUTURE_SUFFIX','known_time':'2026-07-16T23:59:59Z'});b=run_reference(x);assert a['route_ledger']['events']==b['route_ledger']['events'][:-1];assert b['route_ledger']['future_suffix_used'] is False

def test_health_and_quarantine(fixture):
 o=run_reference(fixture);assert o['health']['unhealthy_count']==3;assert len(o['rollout']['quarantined_cells'])>=8

def test_idempotent_command(fixture):
 o=run_reference(fixture);assert o['control_journal']['deduplicated_count']==1

def test_cross_tenant_denied(fixture):
 from saed_v4_context_fleet_scaleout.isolation import assert_route_isolated
 from saed_v4_context_fleet_scaleout.errors import IsolationError
 import pytest
 with pytest.raises(IsolationError):assert_route_isolated(fixture['registry']['cells'][0],fixture['registry']['cells'][1])
