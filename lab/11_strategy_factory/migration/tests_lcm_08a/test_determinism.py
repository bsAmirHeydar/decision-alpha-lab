from pathlib import Path
from tools.strategy_factory.lcm.lcm_08a.upstream import load
from tools.strategy_factory.lcm.lcm_08a.portfolio import build
from tools.strategy_factory.lcm.lcm_08a.canonical import digest_object

ROOT=Path(__file__).resolve().parents[4]

def test_portfolio_build_is_deterministic():
    a,ua,da=build(load(ROOT));b,ub,db=build(load(ROOT))
    assert [r['record_digest'] for r in a]==[r['record_digest'] for r in b]
    assert [r['unresolved_digest'] for r in ua]==[r['unresolved_digest'] for r in ub]
