#property strict
#include <AlphaLab/StrategyFactory/Execution/SF17_AllExecution.mqh>
input bool InpShadowMode=false;
CSF17PaperExecutionEngine g_engine;
int OnInit(){SF17_ExecutionPolicy p=SF17_ReferencePolicy();p.mode=InpShadowMode?SF17_MODE_SHADOW:SF17_MODE_PAPER;string error;if(!g_engine.Configure("sf17-host",p,error)){Print("SF17 configure failed: ",error);return INIT_FAILED;}Print("SF17 paper/shadow host initialized; no broker send authority");return INIT_SUCCEEDED;}
void OnTick(){MqlTick t;if(!SymbolInfoTick(_Symbol,t))return;SF17_QuoteObservation q;q.symbol=_Symbol;q.bid=t.bid;q.ask=t.ask;q.time_utc_msc=(long)t.time_msc;q.sequence=(long)t.time_msc;q.source="terminal";string error;g_engine.OnQuote(q,(long)t.time_msc,error);}
