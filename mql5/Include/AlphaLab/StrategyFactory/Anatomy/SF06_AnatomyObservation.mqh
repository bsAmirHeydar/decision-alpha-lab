#ifndef __SF06_ANATOMY_OBSERVATION_MQH__
#define __SF06_ANATOMY_OBSERVATION_MQH__
#include "../Contracts/SF01_AllContracts.mqh"
#include "SF06_AnatomyEnums.mqh"
struct SF06_AnatomyObservation
{
   string schema;
   string observation_id;
   string plugin_id;
   string plugin_version;
   string symbol;
   int timeframe_seconds;
   ENUM_SF06_OBSERVATION_KIND kind;
   SF01_MarketTimestamp occurred_at;
   SF01_MarketTimestamp known_at;
   double reference_price;
   double extreme_price;
   double close_price;
   string source_bar_id;
   string source_hash;
   string market_event_cluster_id;
};
string SF06_ObservationCanonical(const SF06_AnatomyObservation &v){return v.schema+"|"+v.plugin_id+"|"+v.plugin_version+"|"+v.symbol+"|"+IntegerToString(v.timeframe_seconds)+"|"+IntegerToString((int)v.kind)+"|"+IntegerToString(v.occurred_at.utc_epoch_milliseconds)+"|"+IntegerToString(v.known_at.utc_epoch_milliseconds)+"|"+SF01_CanonicalDouble(v.reference_price)+"|"+SF01_CanonicalDouble(v.extreme_price)+"|"+SF01_CanonicalDouble(v.close_price)+"|"+v.source_bar_id+"|"+v.source_hash+"|"+v.market_event_cluster_id;}
string SF06_DeriveObservationId(const SF06_AnatomyObservation &v){return SF01_StableId("obs",SF06_ObservationCanonical(v));}
bool SF06_ValidateObservation(const SF06_AnatomyObservation &v,string &e){if(v.schema!="alpha_lab.strategy_factory/anatomy_observation@1.0.0"){e="unsupported observation schema";return false;}if(!SF01_IsSafeIdentifier(v.plugin_id,128)||!SF01_IsSafeIdentifier(v.plugin_version,64)){e="invalid plugin identity";return false;}if(!SF01_IsSafeTerminalSymbol(v.symbol,64)){e="invalid symbol";return false;}if(v.timeframe_seconds<=0){e="invalid timeframe";return false;}if(v.kind==SF06_OBS_UNKNOWN){e="unknown observation kind";return false;}if(!SF01_ValidateTimestamp(v.occurred_at,e)||!SF01_ValidateTimestamp(v.known_at,e))return false;if(SF01_CompareTimestamp(v.occurred_at,v.known_at)>0){e="observation known before occurrence";return false;}if(!MathIsValidNumber(v.reference_price)||!MathIsValidNumber(v.extreme_price)||!MathIsValidNumber(v.close_price)){e="invalid price";return false;}if(!SF01_IsSafeIdentifier(v.source_bar_id,128)||!SF01_IsSafeIdentifier(v.source_hash,128)||!SF01_IsSafeIdentifier(v.market_event_cluster_id,128)){e="invalid lineage";return false;}string id=SF06_DeriveObservationId(v);if(v.observation_id!=""&&v.observation_id!=id){e="observation id mismatch";return false;}e="";return true;}
#endif
