#property strict
#property description "EXP0019 Faerie Protocol non-trading differential diagnostic EA"
#include <AlphaLab/EXP0019/FaerieProtocol/I14/FP_I14_All.mqh>
input string InpPrimarySymbol="";
input string InpSecondarySymbol="";
input ENUM_TIMEFRAMES InpResolvedHostTimeframe=PERIOD_M5;
input int InpTimerSeconds=1;
input bool InpEnableTraceExport=false;
input string InpTraceFile="EXP0019_FP_I14_DiagnosticTrace.csv";
input bool InpEnableDashboard=true;
input int InpMaxTraceEvents=100000;
CFP_I14_IndicatorProbe g_probe; CFP_I14_TraceLedger *g_indicator=NULL; CFP_I14_TraceLedger *g_ea=NULL; long g_sequence=0; string g_config_hash=""; string g_reason="";
int OnInit(){
 string primary=(InpPrimarySymbol==""?_Symbol:InpPrimarySymbol); if(InpSecondarySymbol==""||InpSecondarySymbol==primary)return INIT_PARAMETERS_INCORRECT;
 g_config_hash=FP_I14_HashText(primary+"|"+InpSecondarySymbol+"|"+(string)InpResolvedHostTimeframe);
 g_indicator=new CFP_I14_TraceLedger(); g_ea=new CFP_I14_TraceLedger();
 if(!g_probe.Open(primary,InpSecondarySymbol,InpResolvedHostTimeframe)){Print("FP-I14 indicator probe unavailable");return INIT_FAILED;}
 EventSetTimer(MathMax(1,InpTimerSeconds));Print("FP-I14 diagnostic initialized. Runtime authority NONE.");return INIT_SUCCEEDED;
}
void OnTimer(){
 if(g_sequence>=InpMaxTraceEvents)return;g_sequence++;
 double health=0.0;if(!g_probe.ReadBufferValue(0,0,health))return;
 FP_I14_TraceEvent a;a.sequence=g_sequence;a.event_time=TimeCurrent();a.product=FP_I14_PRODUCT_INDICATOR;a.event_type=FP_I14_EVENT_BUFFER;a.semantic_id="BUFFER-0-"+(string)g_sequence;a.payload_hash=FP_I14_HashText(DoubleToString(health,10));a.config_hash=g_config_hash;a.source_revision_id="REV-RUNTIME";a.state="BUFFER";a.buffer_index=0;a.numeric_value=health;
 FP_I14_TraceEvent b=a;b.product=FP_I14_PRODUCT_DIAGNOSTIC_EA;
 string r;if(!g_indicator.Append(a,r)||!g_ea.Append(b,r)){Print(r);return;}
 FP_I14_DifferentialSummary d;FP_I14_CompareLedgers(g_indicator,g_ea,d);
 if(InpEnableDashboard)Comment("FP-I14 Diagnostic EA\nEvents: ",d.compared_events,"\nMismatches: ",d.mismatches,"\nAuthority: NONE\nFP-DEC-012: UNSET");
 if(InpEnableTraceExport && g_sequence%60==0){FP_I14_ExportLedger(g_ea,InpTraceFile,r);}
}
void OnDeinit(const int reason){EventKillTimer();g_probe.Close();if(g_indicator!=NULL){delete g_indicator;g_indicator=NULL;}if(g_ea!=NULL){delete g_ea;g_ea=NULL;}Comment("");}
void OnTick(){}
