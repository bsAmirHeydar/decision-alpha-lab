from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from .contracts import *
from .enums import *
from .costs import default_cost_registry
from .capital import default_capital_registry,CapitalBudgetEngine
from .solver import MaximumLossSolver

def fixture(side=TradeSide.LONG,broker='fx'):
    now=1_700_000_000_000
    quote=QuoteSnapshot('EURUSD',Decimal('1.10000'),Decimal('1.10010'),now,now)
    if broker=='fx':
        spec=SymbolEconomicsSpec('EURUSD','EUR','USD','EUR',5,Decimal('0.00001'),Decimal('0.00001'),Decimal('1'),Decimal('1'),Decimal('100000'),Decimal('0.01'),Decimal('100'),Decimal('0.01'),20,10,TradeStatus.ENABLED,(OrderKind.MARKET,OrderKind.LIMIT,OrderKind.STOP),('fok','ioc'),MarginMode.LEVERAGE,Decimal('100'),Decimal('0'),Decimal('0'),now,now,'fixture','1.0.0')
    else:
        spec=SymbolEconomicsSpec('EURUSD','EUR','USD','EUR',5,Decimal('0.00001'),Decimal('0.00005'),Decimal('5'),Decimal('5'),Decimal('100000'),Decimal('0.1'),Decimal('20'),Decimal('0.1'),10,5,TradeStatus.ENABLED,(OrderKind.MARKET,OrderKind.LIMIT,OrderKind.STOP),('ioc',),MarginMode.FIXED_PER_LOT,Decimal('1'),Decimal('0'),Decimal('500'),now,now,'fixture2','1.0.0')
    account=AccountEconomicSnapshot('acct.fixture','USD',Decimal('100000'),Decimal('100000'),Decimal('50000'),Decimal('0'),Decimal('100000'),known_time_ms=now)
    entry=Decimal('1.10010') if side is TradeSide.LONG else Decimal('1.10000'); stop=Decimal('1.09810') if side is TradeSide.LONG else Decimal('1.10200'); target=Decimal('1.10410') if side is TradeSide.LONG else Decimal('1.09600')
    geo=RiskGeometry('ucet_fixture',side,OrderKind.MARKET,entry,stop,target,1,1,Decimal('1'),Decimal('5'),Decimal('10'))
    req=CapitalRequest('request.fixture','acct.fixture','ucet_fixture','strategy.fixture','EURUSD','fx_major',now,Decimal('0.7'),Decimal('0.55'),Decimal('2'),Decimal('0.01'))
    cr=default_capital_registry(); budget=CapitalBudgetEngine().evaluate((cr.resolve('capital.fixed_cash@1.0.0'),cr.resolve('capital.portfolio_guard@1.0.0')),account,req)
    model=default_cost_registry().resolve('cost.fx_standard@1.0.0')
    return quote,spec,account,geo,req,budget,model

def golden_envelopes():
    solver=MaximumLossSolver(); out=[]
    for side in (TradeSide.LONG,TradeSide.SHORT):
        for broker in ('fx','coarse'):
            q,s,a,g,r,b,m=fixture(side,broker); out.append(solver.solve(g,q,s,a,m,b))
    return tuple(out)
