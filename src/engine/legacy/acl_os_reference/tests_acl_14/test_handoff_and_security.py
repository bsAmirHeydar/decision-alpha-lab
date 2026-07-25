import json
def test_reference_handoff(root):
    d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/handoff/acl15_handoff.json').read_text()); assert d['handoff_type']=='ACL14_TO_ACL15'
def test_handoff_no_execution(root):
    d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/handoff/acl15_handoff.json').read_text()); assert d['pilot_execution_materialized'] is False
def test_handoff_no_prospective_claim(root):
    d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/handoff/acl15_handoff.json').read_text()); assert d['prospective_evidence_present'] is False
def test_security_no_runtime(root):
    d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/security/security_boundary_report.json').read_text()); assert d['runtime_activation_allowed'] is False
def test_security_not_production_ready(root):
    d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/security/security_boundary_report.json').read_text()); assert d['production_security_ready'] is False
