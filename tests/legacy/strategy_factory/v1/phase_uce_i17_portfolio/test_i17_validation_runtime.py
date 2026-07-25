import pytest
from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.allocator import allocate
from strategy_factory_portfolio_v3.stress import run_stress
from strategy_factory_portfolio_v3.validation import validate_portfolio
from strategy_factory_portfolio_v3.runtime import compile_runtime_bundle
from strategy_factory_portfolio_v3.enums import ValidationStatus,RuntimeState
from strategy_factory_portfolio_v3.errors import PortfolioError

def setup():
 b=golden_batch();m=golden_model();l=golden_limits();q={c.candidate_id:estimate_capacity(c,b.as_of_ms) for c in b.candidates};p,ledger=allocate(b,m,l,q);s=run_stress(p,golden_stress(),l);v=validate_portfolio(p,s,{x.context_id:x.adjusted_score for x in p.selected});return p,ledger,m,l,v

def test_validation_requires_oos_and_nested():
 p,ledger,m,l,v=setup();assert v.status is ValidationStatus.PASS;v2=validate_portfolio(p,v.stress_results,{},out_of_sample=False);assert v2.status is ValidationStatus.FAIL
def test_runtime_has_no_order_authority():
 p,ledger,m,l,v=setup();b=compile_runtime_bundle(p,l,m,v,ledger);assert not b.order_authority and not b.broker_authority and b.state is RuntimeState.SHADOW
def test_runtime_rejects_failed_validation():
 p,ledger,m,l,v=setup();v=replace(v,status=ValidationStatus.FAIL)
 with pytest.raises(PortfolioError):compile_runtime_bundle(p,l,m,v,ledger)
def test_runtime_requires_two_contexts():
 p,ledger,m,l,v=setup();p=replace(p,selected=(p.selected[0],),context_count=1,status=p.status)
 with pytest.raises(PortfolioError):compile_runtime_bundle(p,l,m,v,ledger)
