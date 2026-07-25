import json
from tools.strategy_factory.acl_os.acl_12.verify import verify_output
def test_event_tamper_detected(ACL12,tmp_path):
    import shutil; dst=tmp_path/'x'; shutil.copytree(ACL12,dst); p=dst/'events/security_hardening_event_ledger.json'; d=json.loads(p.read_text()); d['events'][0]['event_type']='TAMPER'; p.write_text(json.dumps(d)); assert not verify_output(dst)['passed']
def test_no_production_key_material(ACL12): assert json.loads((ACL12/'custody/key_custody_interface.json').read_text())['production_key_material_present'] is False
def test_no_signature_authority(ACL12): assert json.loads((ACL12/'custody/key_custody_interface.json').read_text())['signature_creation_allowed'] is False
def test_no_runtime_candidate_in_provenance(ACL12): assert json.loads((ACL12/'lineage/security_hardening_provenance_graph.json').read_text())['runtime_candidate_invented'] is False
def test_handoff_denies_keys(ACL12): assert json.loads((ACL12/'handoff/acl13_handoff.json').read_text())['production_key_access_allowed'] is False
