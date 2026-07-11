#property strict
#include <AlphaLab/StrategyFactory/Live/SF18_AllLive.mqh>
input bool InpEnableMicroLive=false;
input bool InpStartWithKillSwitchEngaged=true;
input ulong InpMagicNumber=180018;
input double InpMaximumVolume=0.01;
input int InpMaximumOrdersPerSession=1;
input string InpReleaseHash="";
input string InpAuthorizationHash="";
CSF18Mql5BrokerAdapter g_live_broker;
int OnInit()
{
 if(!InpEnableMicroLive){Print("SF18 micro-live host is DISABLED. No broker mutation can occur.");return INIT_SUCCEEDED;}
 if(InpStartWithKillSwitchEngaged){Print("SF18 kill switch is ENGAGED. Host remains observation-only.");return INIT_SUCCEEDED;}
 if(InpReleaseHash==""||InpAuthorizationHash==""){Print("SF18 missing governed release or authorization hash. Failing closed.");return INIT_FAILED;}
 Print("SF18 authority prerequisites supplied, but this host never synthesizes or submits an intent. Integration must provide a governed Phase 16 intent and call the coordinator explicitly.");return INIT_SUCCEEDED;
}
void OnTradeTransaction(const MqlTradeTransaction &trans,const MqlTradeRequest &request,const MqlTradeResult &result)
{
 Print("SF18 broker transaction observed type=",IntegerToString((int)trans.type)," order=",IntegerToString((long)trans.order)," deal=",IntegerToString((long)trans.deal)," retcode=",IntegerToString((long)result.retcode));
}
