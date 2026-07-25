#property strict
#property indicator_chart_window
#property indicator_buffers 0
#property indicator_plots 0
#include <AlphaLab/EXP0019/FaerieProtocol/I11/FP_I11_All.mqh>
input bool InpRemoveOnExit=true;
FP_I11_VisualEngine g_v;
string H(string x){return FP_I10_StableId("H",x);}
int OnInit(){
 SFP_I11_Config c;c.instance_id="FP-I11-SELFTEST";c.object_namespace="FP19::FP-I11-SELFTEST::";c.mode=FP_I11_AUDIT;c.history_days=30;c.max_objects=500;c.lane_count=6;c.show_sessions=true;c.show_references=true;c.show_hunts=true;c.show_candidates=true;c.show_confirmed=true;c.show_ww=true;c.show_suppressed=true;c.show_health=false;string reason="";if(!g_v.Initialize(ChartID(),c,reason))return INIT_FAILED;
 datetime now=iTime(_Symbol,PERIOD_M1,1);double p=SymbolInfoDouble(_Symbol,SYMBOL_BID);double pt=SymbolInfoDouble(_Symbol,SYMBOL_POINT);if(now<=0||p<=0)return INIT_FAILED;
 g_v.BeginFrame();
 SFP_I11_WindowFact a;a.window_id="A-TEST";a.kind="A";a.state="COMPLETE";a.start_time=now-6*3600;a.end_time=now-2*3600;a.high_price=p+80*pt;a.low_price=p-80*pt;a.semantic_hash=H("A");g_v.ProjectWindow(a);
 SFP_I11_WindowFact n=a;n.window_id="N-TEST";n.kind="N";n.start_time=now-2*3600;n.end_time=now+2*3600;n.high_price=p+100*pt;n.low_price=p-100*pt;n.semantic_hash=H("N");g_v.ProjectWindow(n);
 SFP_I11_ReferenceFact r;r.reference_id="REF-H";r.symbol=_Symbol;r.side="HIGH";r.state="FRESH";r.start_time=now-2*3600;r.end_time=now+2*3600;r.price=p+60*pt;r.semantic_hash=H("RH");g_v.ProjectReference(r);
 SFP_I11_HuntFact h;h.hunt_id="HUNT-1";h.symbol=_Symbol;h.side="HIGH";h.role="HUNTER";h.hunt_time=now-900;h.price=r.price;h.semantic_hash=H("HUNT");g_v.ProjectHunt(h);
 SFP_I11_SignalFact s;s.signal_id="SIG-WINNER";s.relation="AL";s.direction="BEARISH";s.hunter_symbol=_Symbol;s.protected_symbol=_Symbol+".PAIR";s.state="CONFIRMED";s.semantic_hash=H("SIG1");s.reason_code="FP_VIS_SELFTEST";s.disposition=FP_I11_QUOTA_WINNER;s.first_hunt_time=now-900;s.confirmation_time=now-600;s.hunter_price=r.price;s.protected_price=p-30*pt;g_v.ProjectSignal(s);
 SFP_I11_SignalFact q=s;q.signal_id="SIG-SUPPRESSED";q.direction="BULLISH";q.state="CONFIRMED";q.semantic_hash=H("SIG2");q.disposition=FP_I11_SUPPRESSED_BY_WW;q.first_hunt_time=now-500;q.confirmation_time=now-300;q.hunter_price=p-50*pt;q.protected_price=p+20*pt;g_v.ProjectSignal(q);
 SFP_I11_WWFact ww;ww.context_id="WW-TEST";ww.direction="BEARISH";ww.state="CONFIRMED";ww.hunter_symbol=_Symbol;ww.protected_symbol=_Symbol+".PAIR";ww.start_time=now-5*86400;ww.end_time=now+2*86400;ww.semantic_hash=H("WW");g_v.ProjectWW(ww);
 g_v.EndFrame();Print("FP-I11 self-test objects=",g_v.ObjectCount());return INIT_SUCCEEDED;
}
int OnCalculate(const int rates_total,const int prev_calculated,const datetime &time[],const double &open[],const double &high[],const double &low[],const double &close[],const long &tick_volume[],const long &volume[],const int &spread[]){return rates_total;}
void OnDeinit(const int reason){g_v.Shutdown(InpRemoveOnExit);}
