from strategy_factory.decision import AbstentionPolicy, CandidateScore, UtilityWeights, score_candidates
from strategy_factory.contracts import TradeCandidate, Direction, CandidateState
from datetime import datetime, timedelta, timezone


def candidate(cid, target):
    t = datetime(2026,1,1,tzinfo=timezone.utc)
    return TradeCandidate(cid,"e","X",Direction.LONG,"en","st","ex",t,t,t+timedelta(hours=1),"market",100,99,target,1,None,"c",{},CandidateState.ELIGIBLE)


def test_candidate_scoring_is_deterministic():
    c1, c2 = candidate("a", 102), candidate("b", 103)
    outputs = {"a": {"expected_net_r": .2, "probability_positive": .6}, "b": {"expected_net_r": .5, "probability_positive": .55}}
    scores = score_candidates([c1,c2], outputs, weights=UtilityWeights(expected_r=1, probability_positive=.1))
    assert scores[0].candidate_id == "b"


def test_abstention_requires_thresholds():
    policy = AbstentionPolicy(minimum_probability=.6, minimum_expected_r=.1)
    abstain, reasons = policy.evaluate([CandidateScore("x",.05,.55,utility=.1)], {})
    assert abstain
    assert "probability_below_threshold" in reasons
    assert "expected_r_below_threshold" in reasons
