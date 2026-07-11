#ifndef __SF06_EVENT_BUILDER_MQH__
#define __SF06_EVENT_BUILDER_MQH__
#include "SF06_EventLifecycle.mqh"
struct SF06_EventBuildInput
{
   string strategy_id;string strategy_version;string producer_id;string producer_version;string symbol;string reference_symbol;ENUM_SF01_DIRECTION direction;int timeframe_seconds;SF01_MarketTimestamp event_time;SF01_MarketTimestamp known_time;SF01_MarketTimestamp confirmation_time;double reference_price;double invalidation_price;string session_id;string parent_event_id;string market_event_cluster_id;string source_hash;string anatomy_state;
};
bool SF06_BuildCanonicalEvent(const SF06_EventBuildInput &i,SF01_AnatomyEvent &e,string &error){e.schema=SF01_AnatomyEventSchema();e.event_id="";e.strategy_id=i.strategy_id;e.strategy_version=i.strategy_version;e.producer_id=i.producer_id;e.producer_version=i.producer_version;e.symbol=i.symbol;e.reference_symbol=i.reference_symbol;e.direction=i.direction;e.event_time=i.event_time;e.known_time=i.known_time;e.confirmation_time=i.confirmation_time;e.reference_price=i.reference_price;e.invalidation_price=i.invalidation_price;e.timeframe_seconds=i.timeframe_seconds;e.session_id=i.session_id;e.parent_event_id=i.parent_event_id;e.market_event_cluster_id=i.market_event_cluster_id;e.source_hash=i.source_hash;e.anatomy_state=i.anatomy_state;e.event_id=SF01_DeriveAnatomyEventId(e);return SF01_ValidateAnatomyEvent(e,error);}
#endif
