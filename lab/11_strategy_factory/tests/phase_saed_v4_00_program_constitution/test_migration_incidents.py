import pytest
from saed_v4_constitution.migration import migrate_contract
from saed_v4_constitution.errors import ContractError
from saed_v4_constitution.incidents import Incident,qualify_incident

def test_current_migration_identity():
 d={'schema_version':'4.0.0','x':1}; assert migrate_contract(d)==d and migrate_contract(d) is not d

def test_v3_constitution_migrates():
 d={'schema_version':'3.0.0','contract_type':'research_constitution'}; x=migrate_contract(d); assert x['schema_version']=='4.0.0' and x['complete_exposure_accounting']

def test_unknown_migration_rejected():
 with pytest.raises(ContractError): migrate_contract({'schema_version':'2.0.0'})

def test_incident_mapping():
 i=Incident('i','p','protected_evidence_access','critical','2026-07-13T00:00:00Z',('a'*64,),'risk'); assert qualify_incident(i)['required_response']=='quarantine_program'

def test_unknown_incident_pauses():
 i=Incident('i','p','other','high','2026-07-13T00:00:00Z',(),'risk'); assert qualify_incident(i)['required_response']=='manual_investigation_and_pause'
