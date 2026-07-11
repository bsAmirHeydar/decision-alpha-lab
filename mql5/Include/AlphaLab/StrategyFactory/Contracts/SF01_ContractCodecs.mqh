#ifndef __SF01_CONTRACT_CODECS_MQH__
#define __SF01_CONTRACT_CODECS_MQH__

#include "SF01_BarRecord.mqh"
#include "SF01_AnatomyEvent.mqh"
#include "SF01_FeatureSnapshot.mqh"
#include "SF01_ArtifactIdentity.mqh"


string SF01_SchemaToJson(const SF01_SchemaIdentity &value)
{
   return "{\"namespace\":\"" + SF01_JsonEscape(value.schema_namespace) +
          "\",\"name\":\"" + SF01_JsonEscape(value.schema_name) +
          "\",\"major\":" + IntegerToString(value.major) +
          ",\"minor\":" + IntegerToString(value.minor) +
          ",\"patch\":" + IntegerToString(value.patch) + "}";
}

string SF01_TimestampToJson(const SF01_MarketTimestamp &value)
{
   return "{\"utc_epoch_milliseconds\":" + IntegerToString(value.utc_epoch_milliseconds) +
          ",\"source_timezone_id\":\"" + SF01_JsonEscape(value.source_timezone_id) +
          "\",\"source_utc_offset_minutes\":" + IntegerToString(value.source_utc_offset_minutes) +
          ",\"source_clock_id\":\"" + SF01_JsonEscape(value.source_clock_id) +
          "\",\"precision\":" + IntegerToString((int)value.precision) + "}";
}

string SF01_BarRecordToJson(const SF01_BarRecord &value)
{
   return "{\"schema\":" + SF01_SchemaToJson(value.schema) +
          ",\"bar_id\":\"" + SF01_BarId(value) +
          "\",\"symbol\":\"" + SF01_JsonEscape(value.symbol) +
          "\",\"timeframe_seconds\":" + IntegerToString(value.timeframe_seconds) +
          ",\"open_time\":" + SF01_TimestampToJson(value.open_time) +
          ",\"close_time\":" + SF01_TimestampToJson(value.close_time) +
          ",\"open\":" + SF01_CanonicalDouble(value.open_price, 10) +
          ",\"high\":" + SF01_CanonicalDouble(value.high_price, 10) +
          ",\"low\":" + SF01_CanonicalDouble(value.low_price, 10) +
          ",\"close\":" + SF01_CanonicalDouble(value.close_price, 10) +
          ",\"tick_volume\":" + IntegerToString(value.tick_volume) +
          ",\"real_volume\":" + IntegerToString(value.real_volume) +
          ",\"bid_close\":" + SF01_CanonicalDouble(value.bid_close, 10) +
          ",\"ask_close\":" + SF01_CanonicalDouble(value.ask_close, 10) +
          ",\"spread_points\":" + SF01_CanonicalDouble(value.spread_points, 10) +
          ",\"source_id\":\"" + SF01_JsonEscape(value.source_id) +
          "\",\"source_bar_id\":\"" + SF01_JsonEscape(value.source_bar_id) + "\"}";
}

string SF01_AnatomyEventToJson(const SF01_AnatomyEvent &value)
{
   const string event_id = value.event_id == "" ? SF01_DeriveAnatomyEventId(value) : value.event_id;
   return "{\"schema\":" + SF01_SchemaToJson(value.schema) +
          ",\"event_id\":\"" + event_id +
          "\",\"strategy_id\":\"" + SF01_JsonEscape(value.strategy_id) +
          "\",\"strategy_version\":\"" + SF01_JsonEscape(value.strategy_version) +
          "\",\"producer_id\":\"" + SF01_JsonEscape(value.producer_id) +
          "\",\"producer_version\":\"" + SF01_JsonEscape(value.producer_version) +
          "\",\"symbol\":\"" + SF01_JsonEscape(value.symbol) +
          "\",\"reference_symbol\":\"" + SF01_JsonEscape(value.reference_symbol) +
          "\",\"direction\":\"" + SF01_DirectionToString(value.direction) +
          "\",\"event_time\":" + SF01_TimestampToJson(value.event_time) +
          ",\"known_time\":" + SF01_TimestampToJson(value.known_time) +
          ",\"confirmation_time\":" + SF01_TimestampToJson(value.confirmation_time) +
          ",\"reference_price\":" + SF01_CanonicalDouble(value.reference_price, 10) +
          ",\"invalidation_price\":" + SF01_CanonicalDouble(value.invalidation_price, 10) +
          ",\"timeframe_seconds\":" + IntegerToString(value.timeframe_seconds) +
          ",\"session_id\":\"" + SF01_JsonEscape(value.session_id) +
          "\",\"parent_event_id\":\"" + SF01_JsonEscape(value.parent_event_id) +
          "\",\"market_event_cluster_id\":\"" + SF01_JsonEscape(value.market_event_cluster_id) +
          "\",\"source_hash\":\"" + SF01_JsonEscape(value.source_hash) +
          "\",\"anatomy_state\":\"" + SF01_JsonEscape(value.anatomy_state) + "\"}";
}

string SF01_FeatureValueToJson(const SF01_FeatureValue &value)
{
   string encoded = "null";
   if(value.value_type == SF01_FEATURE_DOUBLE) encoded = SF01_CanonicalDouble(value.double_value, 10);
   else if(value.value_type == SF01_FEATURE_INTEGER) encoded = IntegerToString(value.integer_value);
   else if(value.value_type == SF01_FEATURE_BOOLEAN) encoded = SF01_CanonicalBool(value.boolean_value);
   else if(value.value_type == SF01_FEATURE_STRING) encoded = "\"" + SF01_JsonEscape(value.string_value) + "\"";
   else if(value.value_type == SF01_FEATURE_TIMESTAMP) encoded = SF01_TimestampToJson(value.timestamp_value);
   return "{\"feature_id\":\"" + SF01_JsonEscape(value.feature_id) +
          "\",\"feature_version\":\"" + SF01_JsonEscape(value.feature_version) +
          "\",\"value_type\":\"" + SF01_FeatureTypeToString(value.value_type) +
          "\",\"quality\":\"" + SF01_FeatureQualityToString(value.quality) +
          "\",\"known_time\":" + SF01_TimestampToJson(value.known_time) +
          ",\"source_event_id\":\"" + SF01_JsonEscape(value.source_event_id) +
          "\",\"source_hash\":\"" + SF01_JsonEscape(value.source_hash) +
          "\",\"value\":" + encoded + "}";
}

string SF01_ArtifactIdentityToJson(const SF01_ArtifactIdentity &value)
{
   const string artifact_id = value.artifact_id == "" ? SF01_DeriveArtifactId(value) : value.artifact_id;
   return "{\"schema\":" + SF01_SchemaToJson(value.schema) +
          ",\"artifact_id\":\"" + artifact_id +
          "\",\"artifact_type\":\"" + SF01_JsonEscape(value.artifact_type) +
          "\",\"run_id\":\"" + SF01_JsonEscape(value.run_id) +
          "\",\"producer_id\":\"" + SF01_JsonEscape(value.producer_id) +
          "\",\"producer_version\":\"" + SF01_JsonEscape(value.producer_version) +
          "\",\"git_commit\":\"" + SF01_JsonEscape(value.git_commit) +
          "\",\"strategy_id\":\"" + SF01_JsonEscape(value.strategy_id) +
          "\",\"strategy_version\":\"" + SF01_JsonEscape(value.strategy_version) +
          "\",\"manifest_hash\":\"" + SF01_JsonEscape(value.manifest_hash) +
          "\",\"source_hash\":\"" + SF01_JsonEscape(value.source_hash) +
          "\",\"created_at\":" + SF01_TimestampToJson(value.created_at) + "}";
}

#endif
