#ifndef __FP_I12_OPERATOR_UX_MQH__
#define __FP_I12_OPERATOR_UX_MQH__
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_Contracts.mqh>
#include "FP_IndicatorPanel.mqh"
#include "FP_AlertRouter.mqh"
#include "FP_AuditExporter.mqh"
#include "FP_I12_Filters.mqh"
#include "FP_I12_Preferences.mqh"
#include "FP_I12_ActionRouter.mqh"
#include "FP_I12_Diagnostics.mqh"
class FP_I12_OperatorUX {
 private:SFP_I12_Config m_cfg;FP_I12_IndicatorPanel m_panel;FP_I12_AlertRouter m_alerts;FP_I12_AuditExporter m_exporter;FP_I12_FilterEngine m_filters;FP_I12_Preferences m_prefs;FP_I12_ActionRouter m_actions;SFP_I10_EngineSnapshot m_last;bool m_has_last;bool m_ready;
 void RouteHealth(const SFP_I10_EngineSnapshot &s){if(!m_cfg.alerts_enabled)return;if(m_has_last&&m_last.health.overall==s.health.overall&&m_last.health.data_readiness==s.health.data_readiness)return;SFP_I12_AlertCandidate c;c.event_time=TimeCurrent();c.historical=false;c.type=FP_I12_ALERT_HEALTH;c.alert_id="HEALTH-"+IntegerToString((int)s.health.overall)+"-"+IntegerToString((int)s.sequence);c.title="Faerie Protocol health";c.message=(s.health.overall==FP_I10_HEALTH_READY?"READY":s.health.overall==FP_I10_HEALTH_DEGRADED?"DEGRADED":"BLOCKED");m_alerts.Route(c);}
 int FilterMask(const SFP_I12_Filter &f)const{int m=0;if(f.show_al)m|=1;if(f.show_an)m|=2;if(f.show_ln)m|=4;if(f.show_na)m|=8;if(f.show_nl)m|=16;if(f.show_nn)m|=32;if(f.show_ww)m|=64;if(f.show_bullish)m|=128;if(f.show_bearish)m|=256;if(f.show_suppressed)m|=512;if(f.show_historical)m|=1024;return m;}
 void ApplyMask(const int m){SFP_I12_Filter f=m_filters.Current();f.show_al=(m&1)>0;f.show_an=(m&2)>0;f.show_ln=(m&4)>0;f.show_na=(m&8)>0;f.show_nl=(m&16)>0;f.show_nn=(m&32)>0;f.show_ww=(m&64)>0;f.show_bullish=(m&128)>0;f.show_bearish=(m&256)>0;f.show_suppressed=(m&512)>0;f.show_historical=(m&1024)>0;m_filters.Set(f);}
 void ToggleFilter(const string key){SFP_I12_Filter f=m_filters.Current();if(key=="al")f.show_al=!f.show_al;else if(key=="an")f.show_an=!f.show_an;else if(key=="ln")f.show_ln=!f.show_ln;else if(key=="na")f.show_na=!f.show_na;else if(key=="nl")f.show_nl=!f.show_nl;else if(key=="nn")f.show_nn=!f.show_nn;else if(key=="ww")f.show_ww=!f.show_ww;else if(key=="bull")f.show_bullish=!f.show_bullish;else if(key=="bear")f.show_bearish=!f.show_bearish;else if(key=="supp")f.show_suppressed=!f.show_suppressed;else if(key=="hist")f.show_historical=!f.show_historical;m_filters.Set(f);m_prefs.SaveFilterMask(FilterMask(f));}
 public:
  FP_I12_OperatorUX(){m_has_last=false;m_ready=false;}
  bool Initialize(const long chart,const SFP_I12_Config &cfg){m_cfg=cfg;m_filters.Defaults();m_prefs.Initialize(cfg.instance_id);ApplyMask(m_prefs.LoadFilterMask(2047));m_alerts.Initialize(cfg);m_exporter.Initialize(cfg);m_ready=m_panel.Initialize(chart,cfg);return m_ready;}
  void OnSnapshot(const SFP_I10_EngineSnapshot &s){if(!m_ready)return;RouteHealth(s);m_panel.Render(s,m_filters.Current());if(m_cfg.auto_export)m_exporter.ExportSnapshot(s);m_last=s;m_has_last=true;}
  bool OnChartEvent(const int id,const long lparam,const double dparam,const string sparam){if(!m_ready)return false;ENUM_FP_I12_ACTION a=m_panel.Handle(id,sparam);if(a==FP_I12_ACTION_NONE)return false;if(a==FP_I12_ACTION_FILTER){string key="";if(m_panel.FilterKey(sparam,key))ToggleFilter(key);}if(a==FP_I12_ACTION_EXPORT&&m_has_last)m_exporter.ExportSnapshot(m_last);if(a==FP_I12_ACTION_ACK)m_alerts.AcknowledgeAll();m_actions.Record(a);if(m_has_last)m_panel.Render(m_last,m_filters.Current());return true;}
  bool AllowRelation(const string relation)const{return m_filters.RelationVisible(relation);}bool AllowDirection(const string direction)const{return m_filters.DirectionVisible(direction);}SFP_I12_Filter Filters()const{return m_filters.Current();}
  SFP_I12_Diagnostic Diagnostic()const{return FP_I12_BuildDiagnostic(m_ready,m_panel.Updates(),m_alerts.Delivered(),m_alerts.Suppressed(),m_exporter.Records(),m_ready?"FP_UX_READY":"FP_UX_BLOCKED");}
  void Shutdown(const bool remove=true){m_panel.Shutdown(remove);m_ready=false;}
};
#endif
