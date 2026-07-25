from .conftest import j
def test_acceptance_is_non_compensatory_and_authority_negative():
 a=j("reports/acceptance_report.json");assert a["acceptance_gate_passed"] and all(x["result"]=="PASS" for x in a["non_compensatory_gates"]);assert not a["runtime_authority_created"] and not a["live_order_authority_created"] and not a["capital_authority_created"]
