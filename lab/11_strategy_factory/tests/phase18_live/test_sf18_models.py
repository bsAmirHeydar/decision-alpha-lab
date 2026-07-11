from strategy_factory_live import *
from strategy_factory_live.examples import reference_bundle

def test_reference_contracts_validate_and_hash():
    release,auth,policy,intent,account,quote=reference_bundle()
    release.validate(); auth.validate(); policy.validate(); intent.validate(); account.validate(); quote.validate()
    assert release.release_hash==release.derived_hash()
    assert auth.authorization_hash==auth.derived_hash()
    assert policy.policy_hash==policy.derived_hash()
    assert account.snapshot_hash==account.derived_hash()

def test_quote_spread_points():
    *_,q=reference_bundle(); assert abs(q.spread_points-10.0)<1e-9
