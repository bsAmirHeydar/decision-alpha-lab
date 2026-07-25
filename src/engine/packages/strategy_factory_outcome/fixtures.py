from strategy_factory_candidate import *
from .models import PriceObservation,SimulationPolicy
from .enums import *
from .costs import *

def candidate(order_kind=OrderKind.MARKET,entry=100.0,stop=98.0,target=104.0,partial=0.0,direction=1,max_holding=10_000):
    ep=EntryPlan(order_kind,entry,1000,5000)
    sp=StopPlan(stop,abs(entry-stop))
    xp=ExitPlan(ExitKind.PRICE_OR_TIME,target,abs(target-entry),True,max_holding,partial)
    return TradeCandidate("sf09_fixture","ctpl_fixture","evt_sf09","snap_sf09","ctx_sf09","sf09_fixture","1.0.0","EURUSD",direction,9,1000,ep,sp,xp,"src_sf09")
def bar(seq,time,open,high,low,close,spread=0.0):return PriceObservation("EURUSD",ObservationKind.CLOSED_BAR,DataFidelity.BAR_APPROXIMATION,seq,time,time-1000,time,open,high,low,close,spread,None,None,"src_bar")
def registry(cost_r=0.0):
    r=CostRegistry();r.register(FixedCostModel("sf09.cost.fixture","1.0.0",False,commission_r=cost_r));return r.compile()
