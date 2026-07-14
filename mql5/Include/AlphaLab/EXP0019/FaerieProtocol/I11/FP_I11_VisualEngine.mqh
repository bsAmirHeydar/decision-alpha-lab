#ifndef __FP_I11_VISUAL_ENGINE_MQH__
#define __FP_I11_VISUAL_ENGINE_MQH__
#include "FP_I11_Projection.mqh"
#include <AlphaLab/EXP0019/FaerieProtocol/I10/FP_I10_Contracts.mqh>
class FP_I11_VisualEngine {
private: long m_chart_id;SFP_I11_Config m_config;FP_I11_ObjectManager m_manager;bool m_initialized;
 bool SuppressedVisible(ENUM_FP_I11_SIGNAL_DISPOSITION d){return d!=FP_I11_SUPPRESSED_BY_WW&&d!=FP_I11_SUPPRESSED_BY_QUOTA ? true : (m_config.show_suppressed||m_config.mode==FP_I11_AUDIT);}
public:
 FP_I11_VisualEngine(){m_initialized=false;m_chart_id=0;}
 bool Initialize(long chart_id,SFP_I11_Config &cfg,string &reason){m_chart_id=chart_id;m_config=cfg;if(StringFind(cfg.object_namespace,"FP19::")!=0||cfg.max_objects<100||cfg.lane_count<1){reason="FP_VIS_CONFIG_INVALID";return false;}if(!m_manager.Initialize(chart_id,cfg.object_namespace,cfg.max_objects)){reason="FP_VIS_NAMESPACE_INVALID";return false;}m_initialized=true;reason="FP_VIS_READY";return true;}
 void BeginFrame(){if(m_initialized)m_manager.BeginFrame();}
 bool ProjectWindow(const SFP_I11_WindowFact &f){if(!m_initialized||!m_config.show_sessions)return false;SFP_I11_ObjectSpec s=FP_I11_Projection::Window(m_config.object_namespace,f);return m_manager.Upsert(s);}
 bool ProjectReference(const SFP_I11_ReferenceFact &f){if(!m_initialized||!m_config.show_references)return false;SFP_I11_ObjectSpec a=FP_I11_Projection::ReferenceLine(m_config.object_namespace,f),b=FP_I11_Projection::ReferenceLabel(m_config.object_namespace,f);return m_manager.Upsert(a)&&m_manager.Upsert(b);}
 bool ProjectHunt(const SFP_I11_HuntFact &f){if(!m_initialized||!m_config.show_hunts)return false;SFP_I11_ObjectSpec a=FP_I11_Projection::Hunt(m_config.object_namespace,f,m_chart_id,m_config.lane_count),b=FP_I11_Projection::Role(m_config.object_namespace,f,m_chart_id,m_config.lane_count);return m_manager.Upsert(a)&&m_manager.Upsert(b);}
 bool ProjectSignal(const SFP_I11_SignalFact &f){if(!m_initialized)return false;if(f.state=="CANDIDATE"&&!m_config.show_candidates)return false;if(f.state=="CONFIRMED"&&!m_config.show_confirmed)return false;if(!SuppressedVisible(f.disposition))return false;SFP_I11_ObjectSpec s=FP_I11_Projection::Signal(m_config.object_namespace,f,m_chart_id,m_config.lane_count);bool ok=m_manager.Upsert(s);if(f.disposition==FP_I11_SUPPRESSED_BY_WW||f.disposition==FP_I11_SUPPRESSED_BY_QUOTA){SFP_I11_ObjectSpec x=FP_I11_Projection::Suppression(m_config.object_namespace,f,m_chart_id,m_config.lane_count);ok=m_manager.Upsert(x)&&ok;}if(f.disposition==FP_I11_QUOTA_WINNER){SFP_I11_ObjectSpec x=FP_I11_Projection::Winner(m_config.object_namespace,f,m_chart_id,m_config.lane_count);ok=m_manager.Upsert(x)&&ok;}return ok;}
 bool ProjectWW(const SFP_I11_WWFact &f){if(!m_initialized||!m_config.show_ww)return false;double hi=ChartGetDouble(m_chart_id,CHART_PRICE_MAX,0),lo=ChartGetDouble(m_chart_id,CHART_PRICE_MIN,0);SFP_I11_ObjectSpec s=FP_I11_Projection::WW(m_config.object_namespace,f,hi,lo);return m_manager.Upsert(s);}
 bool ProjectHealth(const SFP_I10_EngineSnapshot &snapshot){if(!m_initialized||!m_config.show_health)return false;int hs=(int)snapshot.health.overall;string txt="FP "+(hs==0?"READY":(hs==1?"DEGRADED":"BLOCKED"))+" | "+snapshot.instance.pair_id;SFP_I11_ObjectSpec s=FP_I11_Projection::Health(m_config.object_namespace,"HEALTH-"+snapshot.instance.instance_id,hs,txt,snapshot.snapshot_hash);return m_manager.Upsert(s);}
 void EndFrame(){if(m_initialized)m_manager.EndFrame();}
 void Shutdown(bool remove_all=false){if(!m_initialized)return;m_manager.CleanupOwnNamespace(remove_all);m_initialized=false;}
 SFP_I11_ProjectionStats Stats()const{return m_manager.Stats();} int ObjectCount()const{return m_manager.Count();} bool IsInitialized()const{return m_initialized;}
};
#endif
