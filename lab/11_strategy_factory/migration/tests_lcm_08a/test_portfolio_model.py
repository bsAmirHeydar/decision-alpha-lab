from pathlib import Path
from tools.strategy_factory.lcm.lcm_08a.upstream import load
from tools.strategy_factory.lcm.lcm_08a.portfolio import build
from tools.strategy_factory.lcm.lcm_08a.pilot import select

ROOT=Path(__file__).resolve().parents[4]

def test_portfolio_accounts_for_all_context_identities():
    records,unresolved,deps=build(load(ROOT))
    assert len(records)==321
    assert len({r['identity_id'] for r in records})==321

def test_critical_dimensions_are_non_compensatory():
    records,_,_=build(load(ROOT))
    assert all(r['risk_class']=='CRITICAL' for r in records if r['critical_dimensions'])

def test_exactly_one_reference_pilot_is_selected():
    records,_,_=build(load(ROOT));evaluations,selected=select(records)
    assert selected is not None
    assert selected['identity_id']=='CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1'
    assert sum(e['selected'] for e in evaluations)==1

def test_embedded_fragments_cannot_be_pilot():
    records,_,_=build(load(ROOT));evaluations,_=select(records)
    by_id={r['identity_id']:r for r in records}
    assert all(not e['eligible'] for e in evaluations if by_id[e['identity_id']]['granularity_class']=='EMBEDDED_CONTEXT_FRAGMENT')
