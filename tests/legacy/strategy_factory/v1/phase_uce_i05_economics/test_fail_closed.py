from decimal import Decimal
from dataclasses import replace
import pytest
from strategy_factory_economics_v3 import *
def test_missing_conversion_rejects():
    q,s,a,g,r,b,m=fixture(); s=replace(s,profit_currency='JPY');
    with pytest.raises(Exception): MaximumLossSolver().solve(g,q,s,a,m,b)
def test_stale_quote_rejects():
    q,s,a,g,r,b,m=fixture(); q=replace(q,source_time_ms=q.source_time_ms-100000,known_time_ms=q.known_time_ms-100000)
    with pytest.raises(Exception): MaximumLossSolver().solve(g,q,s,a,m,b)
def test_zero_budget_rejects():
    q,s,a,g,r,b,m=fixture(); b=CapitalBudget(r.request_id,(),Decimal('0'),Decimal('0'),{},False,'zero')
    with pytest.raises(Exception): MaximumLossSolver().solve(g,q,s,a,m,b)
