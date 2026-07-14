#property strict
#property indicator_chart_window
#property indicator_buffers 12
#property indicator_plots 12
#property indicator_type1 DRAW_NONE
#property indicator_type2 DRAW_NONE
#property indicator_type3 DRAW_NONE
#property indicator_type4 DRAW_NONE
#property indicator_type5 DRAW_NONE
#property indicator_type6 DRAW_NONE
#property indicator_type7 DRAW_NONE
#property indicator_type8 DRAW_NONE
#property indicator_type9 DRAW_NONE
#property indicator_type10 DRAW_NONE
#property indicator_type11 DRAW_NONE
#property indicator_type12 DRAW_NONE
#property indicator_label1 "FP Health"
#property indicator_label2 "FP Lifecycle"
#property indicator_label3 "FP Data Readiness"
#property indicator_label4 "FP Active WW"
#property indicator_label5 "FP Confirmed"
#property indicator_label6 "FP Allowed"
#property indicator_label7 "FP Suppressed WW"
#property indicator_label8 "FP Suppressed Quota"
#property indicator_label9 "FP Quota Winner"
#property indicator_label10 "FP Ledger Events"
#property indicator_label11 "FP Revision Sequence"
#property indicator_label12 "FP Heartbeat UTC Minute"
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_All.mqh>

input string InpPrimarySymbol="ES";
input string InpSecondarySymbol="NQ";
input string InpContextEpoch="FP-EPOCH-1";
input int InpHostTimeframeMinutes=5;
input int InpTimerSeconds=1;
input int InpHistoryDays=90;
input int InpMaxIncrementalMinutes=1440;
input bool InpEnableStateBuffers=true;
input bool InpEnableDiagnostics=true;

double B0[],B1[],B2[],B3[],B4[],B5[],B6[],B7[],B8[],B9[],B10[],B11[];
FP_I10_Engine g_engine;

void FP_I10_WriteBuffers(const int index,const SFP_I10_Output &o){
 if(!InpEnableStateBuffers){B0[index]=EMPTY_VALUE;B1[index]=EMPTY_VALUE;B2[index]=EMPTY_VALUE;B3[index]=EMPTY_VALUE;B4[index]=EMPTY_VALUE;B5[index]=EMPTY_VALUE;B6[index]=EMPTY_VALUE;B7[index]=EMPTY_VALUE;B8[index]=EMPTY_VALUE;B9[index]=EMPTY_VALUE;B10[index]=EMPTY_VALUE;B11[index]=EMPTY_VALUE;return;}
 B0[index]=o.health_code;B1[index]=o.lifecycle_code;B2[index]=o.data_readiness_code;B3[index]=o.active_ww_direction;B4[index]=o.confirmed_signal_count;B5[index]=o.allowed_signal_count;B6[index]=o.suppressed_by_ww_count;B7[index]=o.suppressed_by_quota_count;B8[index]=o.quota_winner_present;B9[index]=o.ledger_event_count;B10[index]=o.source_revision_sequence;B11[index]=o.heartbeat_utc_minute;
}
int OnInit(){
 SetIndexBuffer(0,B0,INDICATOR_DATA);SetIndexBuffer(1,B1,INDICATOR_DATA);SetIndexBuffer(2,B2,INDICATOR_DATA);SetIndexBuffer(3,B3,INDICATOR_DATA);SetIndexBuffer(4,B4,INDICATOR_DATA);SetIndexBuffer(5,B5,INDICATOR_DATA);SetIndexBuffer(6,B6,INDICATOR_DATA);SetIndexBuffer(7,B7,INDICATOR_DATA);SetIndexBuffer(8,B8,INDICATOR_DATA);SetIndexBuffer(9,B9,INDICATOR_DATA);SetIndexBuffer(10,B10,INDICATOR_DATA);SetIndexBuffer(11,B11,INDICATOR_DATA);
 ArraySetAsSeries(B0,true);ArraySetAsSeries(B1,true);ArraySetAsSeries(B2,true);ArraySetAsSeries(B3,true);ArraySetAsSeries(B4,true);ArraySetAsSeries(B5,true);ArraySetAsSeries(B6,true);ArraySetAsSeries(B7,true);ArraySetAsSeries(B8,true);ArraySetAsSeries(B9,true);ArraySetAsSeries(B10,true);ArraySetAsSeries(B11,true);
 SFP_I10_Config cfg; cfg.context_id="FP-CONTEXT-001";cfg.context_epoch=InpContextEpoch;cfg.primary_symbol=InpPrimarySymbol;cfg.secondary_symbol=InpSecondarySymbol;cfg.host_timeframe_minutes=InpHostTimeframeMinutes;cfg.timer_seconds=InpTimerSeconds;cfg.history_days=InpHistoryDays;cfg.max_incremental_minutes=InpMaxIncrementalMinutes;cfg.enable_state_buffers=InpEnableStateBuffers;cfg.enable_diagnostics=InpEnableDiagnostics;
 string reason=""; if(!SymbolSelect(InpPrimarySymbol,true)||!SymbolSelect(InpSecondarySymbol,true)){Print("FP-I10 symbol subscription failed");return INIT_FAILED;} if(!g_engine.Initialize(cfg,ChartID(),reason)){Print("FP-I10 init blocked reason=",reason);return INIT_FAILED;} EventSetTimer(InpTimerSeconds); IndicatorSetString(INDICATOR_SHORTNAME,"FP Context ["+g_engine.InstanceId()+"]"); if(InpEnableDiagnostics) Print("FP-I10 ready instance=",g_engine.InstanceId()); return INIT_SUCCEEDED;
}
int OnCalculate(const int rates_total,const int prev_calculated,const datetime &time[],const double &open[],const double &high[],const double &low[],const double &close[],const long &tick_volume[],const long &volume[],const int &spread[]){
 if(rates_total<=0||!g_engine.IsInitialized()) return 0;
 const datetime primary_closed=iTime(InpPrimarySymbol,PERIOD_M1,1);
 const datetime secondary_closed=iTime(InpSecondarySymbol,PERIOD_M1,1);
 if(primary_closed<=0||secondary_closed<=0) return prev_calculated;
 const datetime newest_closed=(primary_closed<secondary_closed?primary_closed:secondary_closed);
 if(!g_engine.OnCalculate(newest_closed,rates_total,prev_calculated)) return prev_calculated;
 const SFP_I10_EngineSnapshot s=g_engine.Snapshot();
 int start=(prev_calculated>0?0:rates_total-1); if(start<0)start=0;
 for(int i=start;i>=0;i--) FP_I10_WriteBuffers(i,s.output);
 return rates_total;
}
void OnTimer(){
 g_engine.OnTimer();
 if(!g_engine.IsInitialized()||ArraySize(B0)<=0) return;
 const SFP_I10_EngineSnapshot s=g_engine.Snapshot();
 FP_I10_WriteBuffers(0,s.output);
}
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam){g_engine.OnChartEvent(id,lparam,dparam,sparam);}
void OnDeinit(const int reason){EventKillTimer();g_engine.Shutdown();}
