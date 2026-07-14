#property strict
#property indicator_chart_window
#property indicator_plots 0
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I12/FP_I12_All.mqh>
FP_I12_OperatorUX g_ux;SFP_I10_EngineSnapshot g_s;
int OnInit(){SFP_I12_Config c;c.instance_id="FP-I12-SELFTEST";c.object_namespace="FP19::FP-I12-SELFTEST::";c.panel_enabled=true;c.dock=FP_I12_TOP_LEFT;c.mode=FP_I12_AUDIT;c.page_size=12;c.alerts_enabled=false;c.alert_popup=false;c.alert_sound=false;c.alert_push=false;c.alert_email=false;c.suppress_historical=true;c.startup_watermark=(int)TimeCurrent();c.max_alerts_per_minute=20;c.export_enabled=false;c.export_format=FP_I12_EXPORT_BOTH;c.export_prefix="FP_I12_SELFTEST";c.auto_export=false;c.open_decision_state="UNSET";if(!g_ux.Initialize(ChartID(),c))return INIT_FAILED;g_s.sequence=1;g_s.instance.instance_id=c.instance_id;g_s.health.overall=FP_I10_HEALTH_READY;g_s.health.data_readiness=FP_I10_DATA_READY;g_s.output.active_ww_direction=1;g_s.output.confirmed_signal_count=8;g_s.output.allowed_signal_count=5;g_s.output.suppressed_by_ww_count=2;g_s.output.suppressed_by_quota_count=1;g_s.output.quota_winner_present=1;g_s.output.source_revision_sequence=7;g_s.snapshot_hash="SELFTEST";g_ux.OnSnapshot(g_s);return INIT_SUCCEEDED;}
int OnCalculate(const int rates_total,const int prev_calculated,const datetime &time[],const double &open[],const double &high[],const double &low[],const double &close[],const long &tick_volume[],const long &volume[],const int &spread[]){return rates_total;}
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam){g_ux.OnChartEvent(id,lparam,dparam,sparam);}
void OnDeinit(const int reason){g_ux.Shutdown(true);}
