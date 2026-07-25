from .conftest import j
def test_hostile_review_attacks_required_failures():
 h=j("reports/hostile_review.json");assert h["hostile_review_passed"];assert {x["attack"] for x in h["attacks"]}=={"ROUTER_ADDS_FILTERS","STOP_TARGET_UNITS_MIXED","MISSING_LIMIT_BECOMES_MARKET","ADAPTER_DEFAULTS_LIVE","PORTFOLIO_RISK_SMUGGLED_INTO_TREATMENT"}
