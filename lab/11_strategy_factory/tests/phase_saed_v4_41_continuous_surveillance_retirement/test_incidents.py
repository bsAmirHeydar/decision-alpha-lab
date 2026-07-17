import pytest
@pytest.mark.parametrize('row',range(8))
def test_incident_has_hash_chained_events(output,row):
 e=output['incidents']['events'][row];assert len(e['event_hash'])==64 and len(e['previous_hash'])==64
def test_incidents_only_for_containment_actions(output):
 eligible=sum(x['action'] in {'RESTRICT','QUARANTINE','RETIRE_CANDIDATE'} for x in output['fusion']['rows']);assert output['incidents']['incident_count']==eligible
def test_no_cross_tenant_incidents(output):assert output['incidents']['cross_tenant_incidents']==0
def test_retirement_incidents_open(output):assert output['incidents']['open_count']==2
