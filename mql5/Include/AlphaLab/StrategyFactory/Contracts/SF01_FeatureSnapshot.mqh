#ifndef __SF01_FEATURE_SNAPSHOT_MQH__
#define __SF01_FEATURE_SNAPSHOT_MQH__

#include "SF01_SchemaIdentity.mqh"
#include "SF01_FeatureValue.mqh"
#include "SF01_Hash.mqh"


class CSF01FeatureSnapshot
{
private:
   SF01_FeatureValue m_values[];

public:
   SF01_SchemaIdentity schema;
   string snapshot_id;
   string event_id;
   string strategy_id;
   SF01_MarketTimestamp snapshot_time;
   string producer_id;
   string producer_version;
   string source_hash;
   long state_generation;

   CSF01FeatureSnapshot(void)
   {
      ArrayResize(m_values, 0);
      snapshot_id = "";
      event_id = "";
      strategy_id = "";
      producer_id = "";
      producer_version = "";
      source_hash = "";
      state_generation = 0;
   }

   int Size(void) const { return ArraySize(m_values); }

   bool Add(const SF01_FeatureValue &value, string &error)
   {
      if(!SF01_ValidateFeatureValue(value, snapshot_time, error)) return false;
      const int count = ArraySize(m_values);
      for(int i = 0; i < count; i++)
      {
         if(m_values[i].feature_id == value.feature_id)
         { error = "duplicate feature_id: " + value.feature_id; return false; }
      }
      ArrayResize(m_values, count + 1);
      m_values[count] = value;
      error = "";
      return true;
   }

   bool Get(const string feature_id, SF01_FeatureValue &out) const
   {
      const int count = ArraySize(m_values);
      for(int i = 0; i < count; i++)
      {
         if(m_values[i].feature_id == feature_id)
         {
            out = m_values[i];
            return true;
         }
      }
      return false;
   }

   bool At(const int index, SF01_FeatureValue &out) const
   {
      if(index < 0 || index >= ArraySize(m_values)) return false;
      out = m_values[index];
      return true;
   }

   string CanonicalIdentity(void) const
   {
      string payload = event_id + "|" + strategy_id + "|" +
                       IntegerToString(snapshot_time.utc_epoch_milliseconds) + "|" +
                       producer_id + "|" + producer_version + "|" +
                       IntegerToString(state_generation) + "|" + source_hash;
      const int count = ArraySize(m_values);
      for(int i = 0; i < count; i++) payload += "|" + SF01_FeatureCanonical(m_values[i]);
      return payload;
   }

   string DeriveId(void) const
   {
      return SF01_StableId("snap", CanonicalIdentity());
   }

   bool Validate(string &error) const
   {
      if(!SF01_ValidateSchemaIdentity(schema, error)) return false;
      if(!SF01_IsSafeIdentifier(event_id)) { error = "invalid event_id"; return false; }
      if(!SF01_IsSafeIdentifier(strategy_id)) { error = "invalid strategy_id"; return false; }
      if(!SF01_ValidateTimestamp(snapshot_time, error)) return false;
      if(!SF01_IsSafeIdentifier(producer_id)) { error = "invalid producer_id"; return false; }
      if(!SF01_IsSafeIdentifier(producer_version)) { error = "invalid producer_version"; return false; }
      if(state_generation < 0) { error = "negative state_generation"; return false; }
      const int count = ArraySize(m_values);
      for(int i = 0; i < count; i++)
      {
         if(!SF01_ValidateFeatureValue(m_values[i], snapshot_time, error)) return false;
         for(int j = i + 1; j < count; j++)
         {
            if(m_values[i].feature_id == m_values[j].feature_id)
            { error = "duplicate feature_id"; return false; }
         }
      }
      const string expected = DeriveId();
      if(snapshot_id != "" && snapshot_id != expected) { error = "snapshot_id mismatch"; return false; }
      error = "";
      return true;
   }
};

#endif
