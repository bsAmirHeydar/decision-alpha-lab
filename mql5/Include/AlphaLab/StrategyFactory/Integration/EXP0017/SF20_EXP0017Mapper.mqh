#ifndef __SF20_EXP0017_MAPPER_MQH__
#define __SF20_EXP0017_MAPPER_MQH__
#include "SF20_EXP0017Contracts.mqh"
#include "../../Anatomy/SF06_EventBuilder.mqh"
string SF20_EXP0017ClusterId(const SCGDDivergenceCandidate &c)
{return SF01_StableId("cluster",c.group_name+"|"+IntegerToString(c.group_minutes)+"|"+IntegerToString((long)c.trading_day_start_ny)+"|"+IntegerToString((long)c.current_cycle_start_ny)+"|"+IntegerToString((long)c.reference_cycle_start_ny)+"|"+IntegerToString((int)c.direction)+"|"+IntegerToString((int)c.side));}
string SF20_EXP0017ParentId(const SCGDDivergenceCandidate &c)
{return SF01_StableId("parent",c.group_name+"|"+IntegerToString((long)c.trading_day_start_ny)+"|"+IntegerToString((long)c.reference_cycle_start_ny));}
string SF20_EXP0017SourceHash(const SCGDDivergenceCandidate &c){return SF01_StableId("src",SF20_LegacyCandidateIdentity(c));}
bool SF20_MapEXP0017Candidate(const SCGDDivergenceCandidate &c,const SF20_EXP0017Config &config,const long known_time_utc_msc,const string strategy_id,const string strategy_version,SF01_AnatomyEvent &event,SF20_EXP0017MappingRecord &mapping,string &error)
{
 if(c.status!=CGD_STATUS_CANDIDATE||!c.one_sided_hunt||!c.data_ready){error="legacy candidate is not ready one-sided divergence";return false;}
 if(c.clean_symbol==""||c.hunter_symbol==""||c.clean_symbol==c.hunter_symbol){error="invalid hunter clean symbols";return false;}
 if(c.group_minutes<=0||known_time_utc_msc<=0){error="invalid group or known time";return false;}
 ENUM_SF01_DIRECTION direction=SF01_DIRECTION_NONE;if(c.direction==CGD_DIRECTION_BUY&&c.side==CGD_SIDE_LOW)direction=SF01_DIRECTION_LONG;else if(c.direction==CGD_DIRECTION_SELL&&c.side==CGD_SIDE_HIGH)direction=SF01_DIRECTION_SHORT;else{error="legacy direction side mismatch";return false;}
 SF01_MarketTimestamp known=SF01_MakeUtcMilliseconds(known_time_utc_msc,"UTC",0,"sf20_exp0017_adapter",SF01_TIME_MILLISECONDS);
 SF06_EventBuildInput input;input.strategy_id=strategy_id;input.strategy_version=strategy_version;input.producer_id=SF20_EXP0017_PLUGIN_ID;input.producer_version=SF20_EXP0017_PLUGIN_VERSION;input.symbol=c.clean_symbol;input.reference_symbol=c.hunter_symbol;input.direction=direction;input.timeframe_seconds=c.group_minutes*60;input.event_time=known;input.known_time=known;input.confirmation_time=known;input.reference_price=c.clean_reference_price;input.invalidation_price=c.clean_stop_reference_price;input.session_id=SF01_StableId("nytd",IntegerToString((long)c.trading_day_start_ny));input.parent_event_id=SF20_EXP0017ParentId(c);input.market_event_cluster_id=SF20_EXP0017ClusterId(c);input.source_hash=SF20_EXP0017SourceHash(c);input.anatomy_state="exp0017_raw_divergence_candidate_unconfirmed_trade";
 if(!SF06_BuildCanonicalEvent(input,event,error))return false;
 mapping.legacy_divergence_id=c.divergence_id;mapping.legacy_payload_hash=SF01_StableId("sf20lp",SF20_LegacyCandidatePayload(c));mapping.canonical_event_id=event.event_id;mapping.canonical_source_hash=event.source_hash;mapping.cluster_id=event.market_event_cluster_id;mapping.mapped_at_utc_msc=known_time_utc_msc;mapping.adapter_config_hash=SF20_EXP0017ConfigHash(config);mapping.adapter_version=SF20_EXP0017_PLUGIN_VERSION;mapping.reasons="legacy_raw_candidate|trade_confirmation_not_inferred|clean_symbol_is_trade_symbol";mapping.mapping_id=SF01_StableId("sf20map",c.divergence_id+"|"+event.event_id+"|"+IntegerToString(known_time_utc_msc)+"|"+mapping.adapter_config_hash);error="";return true;
}
#endif
