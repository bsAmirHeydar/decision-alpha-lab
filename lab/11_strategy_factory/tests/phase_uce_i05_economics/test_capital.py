from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from strategy_factory_economics_v3 import *
def test_fixed_cash_and_portfolio_cap():
    q,s,a,g,r,b,m=fixture(); assert b.approved_cash==Decimal('100')
def test_drawdown_scaling_reduces_budget():
    q,s,a,g,r,b,m=fixture(); reg=default_capital_registry(); eng=CapitalBudgetEngine(); normal=eng.evaluate((reg.resolve('capital.fixed_cash@1.0.0'),reg.resolve('capital.drawdown_guard@1.0.0')),a,r)
    from dataclasses import replace
    dd=replace(a,equity=Decimal('85000')); stressed=eng.evaluate((reg.resolve('capital.fixed_cash@1.0.0'),reg.resolve('capital.drawdown_guard@1.0.0')),dd,r)
    assert stressed.approved_cash<normal.approved_cash
def test_capped_kelly_is_bounded():
    q,s,a,g,r,b,m=fixture(); reg=default_capital_registry(); out=CapitalBudgetEngine().evaluate((reg.resolve('capital.capped_kelly@1.0.0'),),a,r); assert out.approved_cash<=a.equity*Decimal('0.01')
