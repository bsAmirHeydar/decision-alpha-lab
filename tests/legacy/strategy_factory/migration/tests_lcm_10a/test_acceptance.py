from .conftest import j
def test_acceptance_is_reference_only():
 a=j('reports/acceptance_report.json');c=j('reports/portfolio_closure_report.json');assert a['acceptance_gate_passed'] and c['closure_status']=='CLOSED_REFERENCE_INVENTORY';assert not a['runtime_authority_created'] and not a['live_order_authority_created'] and not a['capital_authority_created']
