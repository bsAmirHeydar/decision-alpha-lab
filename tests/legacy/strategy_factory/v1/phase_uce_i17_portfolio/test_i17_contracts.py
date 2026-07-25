import pytest
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.contracts import *
from strategy_factory_portfolio_v3.enums import *
from strategy_factory_portfolio_v3.errors import PortfolioError

def test_candidate_identity_is_stable():
    a=golden_batch().candidates[0];assert a.candidate_hash==a.candidate_hash and len(a.candidate_hash)==64
@pytest.mark.parametrize('field,value', [('novelty',1.1),('liquidity_score',-0.1),('requested_risk',-1)])
def test_invalid_candidate_numeric_fields_fail(field,value):
    from dataclasses import replace
    with pytest.raises(PortfolioError): replace(golden_batch().candidates[0],**{field:value})
def test_non_promoted_candidate_fails():
    from dataclasses import replace
    c=golden_batch().candidates[0];p=replace(c.promotion,status=PromotionStatus.REJECT,prospective_complete=False)
    with pytest.raises(PortfolioError):replace(c,promotion=p)
def test_future_candidate_fails_batch():
    from dataclasses import replace
    b=golden_batch();c=replace(b.candidates[0],known_time_ms=3000,expires_at_ms=4000)
    with pytest.raises(PortfolioError):replace(b,candidates=(c,)+b.candidates[1:])
def test_limits_sub_limit_cannot_exceed_total():
    from dataclasses import replace
    with pytest.raises(PortfolioError):replace(golden_limits(),per_symbol_risk=99)
