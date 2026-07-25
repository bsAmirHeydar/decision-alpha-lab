from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.queue import rank_batch
from strategy_factory_portfolio_v3.dependence import correlation,marginal_risk
from strategy_factory_portfolio_v3.enums import OpportunityStatus

def test_ranking_is_deterministic(): assert rank_batch(golden_batch())==rank_batch(golden_batch())
def test_ranking_prefers_higher_adjusted_utility(): assert rank_batch(golden_batch())[0].candidate.candidate_id=='cand-1'
def test_expired_candidate_rejected():
    b=golden_batch();c=replace(b.candidates[0],expires_at_ms=1500);b=replace(b,candidates=(c,)+b.candidates[1:]);assert any(x.status is OpportunityStatus.REJECTED for x in rank_batch(b))
def test_unknown_dependence_is_conservative(): assert correlation(golden_batch().candidates[0],golden_batch().candidates[2],golden_model())==golden_model().fallback_correlation
def test_same_currency_uses_currency_floor(): assert correlation(golden_batch().candidates[0],golden_batch().candidates[1],golden_model())>=golden_model().currency_correlation
def test_marginal_risk_increases_with_existing_selection():
    c=golden_batch().candidates;assert marginal_risk(c[1],[c[0]],golden_model())>c[1].requested_risk
