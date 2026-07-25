import json
from tools.strategy_factory.acl_os.acl_14.schema_validation import validate_instance
def test_request_schema(root): validate_instance('pilot_request',json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/pilot_request.json').read_text()))
def test_decision_schema(root): validate_instance('pilot_readiness_decision',json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/decision/pilot_readiness_decision.json').read_text()))
def test_handoff_schema(root): validate_instance('acl15_handoff',json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot/handoff/acl15_handoff.json').read_text()))
