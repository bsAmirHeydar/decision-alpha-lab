#ifndef __SF01_FEATURE_VALUE_MQH__
#define __SF01_FEATURE_VALUE_MQH__

#include "SF01_MarketTimestamp.mqh"
#include "SF01_StringCodec.mqh"


struct SF01_FeatureValue
{
   string feature_id;
   string feature_version;
   ENUM_SF01_FEATURE_TYPE value_type;
   ENUM_SF01_FEATURE_QUALITY quality;
   SF01_MarketTimestamp known_time;
   string source_event_id;
   string source_hash;
   double double_value;
   long integer_value;
   bool boolean_value;
   string string_value;
   SF01_MarketTimestamp timestamp_value;
};

SF01_FeatureValue SF01_MakeDoubleFeature(const string feature_id,
                                          const string feature_version,
                                          const double value,
                                          const SF01_MarketTimestamp &known_time,
                                          const string source_event_id,
                                          const string source_hash)
{
   SF01_FeatureValue out;
   out.feature_id = feature_id;
   out.feature_version = feature_version;
   out.value_type = SF01_FEATURE_DOUBLE;
   out.quality = SF01_QUALITY_VALID;
   out.known_time = known_time;
   out.source_event_id = source_event_id;
   out.source_hash = source_hash;
   out.double_value = value;
   out.integer_value = 0;
   out.boolean_value = false;
   out.string_value = "";
   out.timestamp_value = known_time;
   return out;
}

SF01_FeatureValue SF01_MakeIntegerFeature(const string feature_id,
                                           const string feature_version,
                                           const long value,
                                           const SF01_MarketTimestamp &known_time,
                                           const string source_event_id,
                                           const string source_hash)
{
   SF01_FeatureValue out;
   out.feature_id = feature_id;
   out.feature_version = feature_version;
   out.value_type = SF01_FEATURE_INTEGER;
   out.quality = SF01_QUALITY_VALID;
   out.known_time = known_time;
   out.source_event_id = source_event_id;
   out.source_hash = source_hash;
   out.double_value = 0.0;
   out.integer_value = value;
   out.boolean_value = false;
   out.string_value = "";
   out.timestamp_value = known_time;
   return out;
}

SF01_FeatureValue SF01_MakeBooleanFeature(const string feature_id,
                                           const string feature_version,
                                           const bool value,
                                           const SF01_MarketTimestamp &known_time,
                                           const string source_event_id,
                                           const string source_hash)
{
   SF01_FeatureValue out;
   out.feature_id = feature_id;
   out.feature_version = feature_version;
   out.value_type = SF01_FEATURE_BOOLEAN;
   out.quality = SF01_QUALITY_VALID;
   out.known_time = known_time;
   out.source_event_id = source_event_id;
   out.source_hash = source_hash;
   out.double_value = 0.0;
   out.integer_value = 0;
   out.boolean_value = value;
   out.string_value = "";
   out.timestamp_value = known_time;
   return out;
}

SF01_FeatureValue SF01_MakeStringFeature(const string feature_id,
                                          const string feature_version,
                                          const string value,
                                          const SF01_MarketTimestamp &known_time,
                                          const string source_event_id,
                                          const string source_hash)
{
   SF01_FeatureValue out;
   out.feature_id = feature_id;
   out.feature_version = feature_version;
   out.value_type = SF01_FEATURE_STRING;
   out.quality = SF01_QUALITY_VALID;
   out.known_time = known_time;
   out.source_event_id = source_event_id;
   out.source_hash = source_hash;
   out.double_value = 0.0;
   out.integer_value = 0;
   out.boolean_value = false;
   out.string_value = value;
   out.timestamp_value = known_time;
   return out;
}

bool SF01_ValidateFeatureValue(const SF01_FeatureValue &value,
                               const SF01_MarketTimestamp &snapshot_time,
                               string &error)
{
   if(!SF01_IsSafeIdentifier(value.feature_id)) { error = "invalid feature_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.feature_version)) { error = "invalid feature_version"; return false; }
   if(!SF01_ValidateTimestamp(value.known_time, error)) return false;
   if(SF01_CompareTimestamp(value.known_time, snapshot_time) > 0)
   { error = "feature known_time after snapshot_time"; return false; }
   if(value.quality == SF01_QUALITY_VALID)
   {
      if(value.value_type == SF01_FEATURE_DOUBLE && !MathIsValidNumber(value.double_value))
      { error = "invalid double feature"; return false; }
      if(value.value_type == SF01_FEATURE_STRING && StringLen(value.string_value) > 2048)
      { error = "string feature too long"; return false; }
   }
   error = "";
   return true;
}

string SF01_FeatureCanonical(const SF01_FeatureValue &value)
{
   string encoded_value = "null";
   if(value.value_type == SF01_FEATURE_DOUBLE) encoded_value = SF01_CanonicalDouble(value.double_value, 10);
   else if(value.value_type == SF01_FEATURE_INTEGER) encoded_value = IntegerToString(value.integer_value);
   else if(value.value_type == SF01_FEATURE_BOOLEAN) encoded_value = SF01_CanonicalBool(value.boolean_value);
   else if(value.value_type == SF01_FEATURE_STRING) encoded_value = value.string_value;
   else if(value.value_type == SF01_FEATURE_TIMESTAMP) encoded_value = IntegerToString(value.timestamp_value.utc_epoch_milliseconds);
   return value.feature_id + "|" + value.feature_version + "|" +
          SF01_FeatureTypeToString(value.value_type) + "|" +
          SF01_FeatureQualityToString(value.quality) + "|" +
          IntegerToString(value.known_time.utc_epoch_milliseconds) + "|" + encoded_value + "|" + value.source_hash;
}

#endif
