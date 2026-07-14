#property strict
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots 1
#property indicator_type1 DRAW_NONE
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_All.mqh>
double TestBuffer[];
int OnInit(){ SetIndexBuffer(0,TestBuffer,INDICATOR_DATA); SFP_I10_Config cfg; cfg.context_id="FP-CONTEXT-001";cfg.context_epoch="SELFTEST";cfg.primary_symbol="ES";cfg.secondary_symbol="NQ";cfg.host_timeframe_minutes=5;cfg.timer_seconds=1;cfg.history_days=30;cfg.max_incremental_minutes=1440;cfg.enable_state_buffers=true;cfg.enable_diagnostics=true; string reason=""; if(!FP_I10_ValidateConfig(cfg,reason)) return INIT_FAILED; if(!FP_I10_ValidateComposition(reason)) return INIT_FAILED; SFP_I10_Instance a=FP_I10_BuildInstance(cfg,ChartID()); if(a.instance_id==""||a.object_namespace=="") return INIT_FAILED; Print("FP-I10 indicator self-test PASS instance=",a.instance_id," version=",FP_I10_PHASE_VERSION); return INIT_SUCCEEDED; }
int OnCalculate(const int rates_total,const int prev_calculated,const datetime &time[],const double &open[],const double &high[],const double &low[],const double &close[],const long &tick_volume[],const long &volume[],const int &spread[]){ if(rates_total>0) TestBuffer[0]=1.0; return rates_total; }
