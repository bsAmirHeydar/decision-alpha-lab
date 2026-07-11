#ifndef __SF20_EXP0017_PLUGIN_MQH__
#define __SF20_EXP0017_PLUGIN_MQH__
#include "SF20_EXP0017LegacyProbe.mqh"
#include "SF20_EXP0017Mapper.mqh"
#include "SF20_EXP0017DedupRegistry.mqh"
#include "SF20_EXP0017DifferentialLedger.mqh"
#include "../../Plugins/SF04_AnatomyPluginBase.mqh"
class CSF20EXP0017Plugin:public CSF04AnatomyPluginBase
{
private:SF20_EXP0017Config m_config;CSF20EXP0017LegacyProbe m_probe;CSF20EXP0017DedupRegistry m_dedup;CSF20EXP0017DifferentialLedger m_differential;SF20_EXP0017Telemetry m_pilot_telemetry;
 bool RefreshSharedBoundary(string &error){if(m_market.RefreshSeries(m_config.symbol_a,60,m_config.m1_lookback_bars,error)<=0)return false;if(m_market.RefreshSeries(m_config.symbol_b,60,m_config.m1_lookback_bars,error)<=0)return false;return true;}
protected:
 bool OnPluginInitialize(string &error){SF20_ResetTelemetry(m_pilot_telemetry);if(!m_probe.Configure(m_config,error)||!m_dedup.Configure(4096,error)||!m_differential.Configure(8192,error))return false;return true;}
 bool OnPluginStart(string &error){if(m_config.live_authority){error="live authority forbidden";return false;}error="";return true;}void OnPluginStop(){}void OnPluginShutdown(){m_dedup.Clear();}void OnPluginTick(const MqlTick &tick){}
 void OnPluginTimer(const long now_utc_msc)
 {
  m_pilot_telemetry.pulses++;string error;if(!RefreshSharedBoundary(error)){m_pilot_telemetry.mapping_failures++;return;}SCGDDivergenceCandidate legacy[];SF20_EXP0017GroupEvidence groups[];int count=m_probe.Observe(TimeCurrent(),now_utc_msc,legacy,groups,error);m_pilot_telemetry.legacy_candidates_seen+=count;m_dedup.BeginPulse();
  for(int i=0;i<count;i++){SF01_AnatomyEvent event;SF20_EXP0017MappingRecord mapping;if(!SF20_MapEXP0017Candidate(legacy[i],m_config,now_utc_msc,m_runtime_config.strategy_id,m_runtime_config.strategy_version,event,mapping,error)){m_pilot_telemetry.mapping_failures++;continue;}bool is_new=false;SF20_EXP0017LifecycleRecord lifecycle;if(!m_dedup.Observe(event.event_id,now_utc_msc,is_new,lifecycle,error)){m_pilot_telemetry.mapping_failures++;continue;}if(!m_differential.AppendMapping(mapping,error)||!m_differential.AppendMatch(legacy[i],event,now_utc_msc,error)){m_pilot_telemetry.differential_mismatches++;continue;}if(!is_new){m_pilot_telemetry.duplicate_events_suppressed++;continue;}if(!EmitEvent(event,error)){m_pilot_telemetry.mapping_failures++;continue;}m_pilot_telemetry.canonical_events_emitted++;}
  SF20_EXP0017LifecycleRecord retired[];int retired_count=m_dedup.RetireMissing(now_utc_msc,retired);m_pilot_telemetry.events_retired+=retired_count;
 }
public:
 CSF20EXP0017Plugin(const SF20_EXP0017Config &config){m_config=config;m_descriptor=SF04_DefaultAnatomyDescriptor();m_descriptor.plugin_id=SF20_EXP0017_PLUGIN_ID;m_descriptor.display_name="EXP0017 Temporal Intermarket Divergence Adapter";m_descriptor.version=SF20_EXP0017_PLUGIN_VERSION;m_descriptor.provider_id="alpha_lab.strategy_factory";m_descriptor.provider_version="1.0.0";m_descriptor.capability_mask=SF04_CAP_CLOSED_BAR_INPUT|SF04_CAP_MULTI_SYMBOL|SF04_CAP_MULTI_TIMEFRAME|SF04_CAP_TIMER_INPUT|SF04_CAP_REPLAY_SAFE|SF04_CAP_DETERMINISTIC|SF04_CAP_STATEFUL|SF04_CAP_EMITS_PARENT_LINKS|SF04_CAP_EMITS_CLUSTER_ID|SF04_CAP_REQUIRES_SYNCHRONIZATION;m_descriptor.update_scope_mask=SF04_UPDATE_TIMER|SF04_UPDATE_REPLAY|SF04_UPDATE_HISTORY_REBUILD;m_descriptor.event_queue_capacity=512;m_descriptor.queue_overflow_policy=SF04_QUEUE_FAIL_PLUGIN;m_descriptor.deterministic=true;m_descriptor.replay_safe=true;m_descriptor.fast_path_safe=false;m_descriptor.stateful=true;m_descriptor.description="Compatibility-preserving EXP0017 pilot adapter. Emits raw divergence anatomy only; no trade confirmation or broker authority.";m_descriptor.configuration_schema_hash=SF20_EXP0017ConfigHash(config);string ignored="";SF04_DataRequirement a;a.requirement_id="exp0017_symbol_a_m1";a.kind=SF04_REQUIREMENT_CLOSED_BARS;a.strength=SF04_REQUIREMENT_REQUIRED;a.symbol=config.symbol_a;a.timeframe_seconds=60;a.lookback_bars=config.m1_lookback_bars;a.max_staleness_msc=120000;a.max_close_skew_msc=60000;a.synchronization_group_id="exp0017_pair_m1";a.purpose="legacy parity and divergence anatomy";AddRequirement(a,ignored);SF04_DataRequirement b=a;b.requirement_id="exp0017_symbol_b_m1";b.symbol=config.symbol_b;AddRequirement(b,ignored);}
 virtual bool ValidatePluginConfiguration(string &error)const{if(!CSF04AnatomyPluginBase::ValidatePluginConfiguration(error))return false;return SF20_ValidateEXP0017Config(m_config,error);}SF20_EXP0017Telemetry PilotTelemetry()const{return m_pilot_telemetry;}int DifferentialRecordCount()const{return m_differential.RecordCount();}
};
#endif
