from strategy_factory_execution import *

def mk(kind,direction=1):
    entry=100; stop=98 if direction==1 else 102; target=104 if direction==1 else 96
    return ExecutionIntentRecord("i"+str(int(kind))+str(direction),"h","b","c","ch","ctx","s","1","X","g",direction,17,"rel","dp","rp","ap",kind,entry,stop,target,True,1,100,80,1,1000,10000,True)

def pol(): return PaperExecutionPolicy("p","1",ExecutionMode.PAPER,.01,0,0,0,1000,False,True,True,1)

def test_market_fills_next_quote():
    e=PaperExecutionEngine("r",pol()); o=e.submit(mk(OrderKind.MARKET),1000)
    e.on_quote(QuoteObservation("X",100,100.1,1100,1)); assert o.state==OrderState.FILLED

def test_stop_waits_for_trigger():
    e=PaperExecutionEngine("r",pol()); o=e.submit(mk(OrderKind.STOP),1000)
    e.on_quote(QuoteObservation("X",99,99.1,1100,1)); assert o.state==OrderState.WORKING
    e.on_quote(QuoteObservation("X",100,100.1,1200,2)); assert o.state==OrderState.FILLED
