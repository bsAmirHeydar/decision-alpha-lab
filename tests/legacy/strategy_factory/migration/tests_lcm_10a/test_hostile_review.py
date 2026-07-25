from .conftest import j
def test_hostile_review_attempts_required_attacks():
 d=j('reports/hostile_review.json');names={x['attack'] for x in d['attacks']};assert d['hostile_review_passed'];assert {'WRAPPER_HIDING_BROKER_SUBMISSION','FILE_LEDGER_AS_ENTITLEMENT_AUTHORITY','VOLUME_DEFAULT_DIFFERS_BY_SYMBOL','LONG_SHORT_ASYMMETRY','TESTER_MODE_BYPASSES_SAFETY'}<=names
