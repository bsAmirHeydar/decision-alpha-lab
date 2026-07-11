from strategy_factory_research import *
def o(i,r,filled=True):return OutcomeView(f"out_{i}",f"cand_{i}",f"evt_{i}",f"cl_{i}",filled,False,r,max(r,0),max(-r,0),60)
def test_metrics():
 a=ResearchAccumulator();a.observe(o(1,1.5));a.observe(o(2,-1));a.observe(o(3,0,False));m=a.snapshot();assert m.outcome_count==3 and m.filled_count==2;assert abs(m.expectancy_r-.25)<1e-12;assert m.metrics_hash.startswith("rmet_")
def test_drawdown_and_streak():
 a=ResearchAccumulator();[a.observe(o(i,r)) for i,r in enumerate([1,-1,-1,.5],1)];m=a.snapshot();assert m.maximum_drawdown_r==2 and m.maximum_consecutive_losses==2
