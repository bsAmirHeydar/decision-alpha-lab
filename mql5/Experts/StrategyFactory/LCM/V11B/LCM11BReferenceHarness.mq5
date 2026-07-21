#property strict
#include <StrategyFactory/LCM/V11B/LCM11BVisualEvent.mqh>
#include <StrategyFactory/LCM/V11B/LCM11BStyle.mqh>
#include <StrategyFactory/LCM/V11B/LCM11BChartObjectVisualizer.mqh>
#include <StrategyFactory/LCM/V11B/LCM11BCompatibilityAdapter.mqh>
#include <StrategyFactory/LCM/V11B/LCM11BAuthorityBoundary.mqh>
input string InpInstanceId="LCM11B_REFERENCE";
CLCM11BChartObjectVisualizer g_visualizer;CLCM11BCompatibilityAdapter g_adapter;CLCM11BAuthorityBoundary g_authority;
int OnInit()
  {
   g_visualizer.Configure("ALPHA_LAB","LCM11B",InpInstanceId);
   if(g_authority.RuntimeAuthority()||g_authority.OrderAuthority()||g_authority.CapitalAuthority()||g_authority.DomainMutationAllowed())return INIT_FAILED;
   LCM11BVisualEvent event;g_adapter.FromLegacy("VISOBJ_REFERENCE","REFERENCE_EVENT",InpInstanceId,ChartID(),_Symbol,_Period,iTime(_Symbol,_Period,1),iClose(_Symbol,_Period,1),iTime(_Symbol,_Period,0),iClose(_Symbol,_Period,0),"LCM11B",event);LCM11BStyle style;LCM11BDefaultStyle(style);g_visualizer.EnsureTrend(event,"REFERENCE",style);return INIT_SUCCEEDED;
  }
void OnDeinit(const int reason){g_visualizer.Cleanup(ChartID());}
void OnTick(){}
