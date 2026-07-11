#ifndef __SF07_CONTEXT_STATE_MQH__
#define __SF07_CONTEXT_STATE_MQH__

#include "../Contracts/SF01_AllContracts.mqh"
#include "SF07_ContextEnums.mqh"

struct SF07_ContextEntry
{
   string feature_id;
   SF01_FeatureValue value;
   long computed_generation;
   long expires_at_utc_msc;
   bool dirty;
   ENUM_SF07_INVALIDATION_REASON invalidation_reason;
};

class CSF07ContextState
{
private:
   SF07_ContextEntry m_entries[];
   int m_capacity;
   long m_generation;
   string m_event_id;
   SF01_MarketTimestamp m_snapshot_time;

   int FindIndex(const string feature_id) const
   {
      const int count = ArraySize(m_entries);
      for(int i = 0; i < count; i++)
         if(m_entries[i].feature_id == feature_id) return i;
      return -1;
   }

public:
   CSF07ContextState(void)
   {
      ArrayResize(m_entries, 0);
      m_capacity = 128;
      m_generation = 0;
      m_event_id = "";
   }

   bool Initialize(const int capacity, string &error)
   {
      if(capacity < 1 || capacity > 4096)
      { error = "invalid context capacity"; return false; }
      m_capacity = capacity;
      ArrayResize(m_entries, 0);
      m_generation = 0;
      m_event_id = "";
      error = "";
      return true;
   }

   bool BeginGeneration(const long generation,
                        const string event_id,
                        const SF01_MarketTimestamp &snapshot_time,
                        string &error)
   {
      if(generation < 0)
      { error = "negative context generation"; return false; }
      if(!SF01_IsSafeIdentifier(event_id, 128))
      { error = "invalid context event id"; return false; }
      if(!SF01_ValidateTimestamp(snapshot_time, error)) return false;
      m_generation = generation;
      m_event_id = event_id;
      m_snapshot_time = snapshot_time;
      error = "";
      return true;
   }

   long Generation(void) const { return m_generation; }
   string EventId(void) const { return m_event_id; }
   SF01_MarketTimestamp SnapshotTime(void) const { return m_snapshot_time; }
   int Count(void) const { return ArraySize(m_entries); }

   bool Put(const SF01_FeatureValue &value,
            const long max_age_milliseconds,
            string &error)
   {
      if(!SF01_ValidateFeatureValue(value, m_snapshot_time, error)) return false;
      int index = FindIndex(value.feature_id);
      if(index < 0)
      {
         const int count = ArraySize(m_entries);
         if(count >= m_capacity)
         { error = "context state capacity exceeded"; return false; }
         ArrayResize(m_entries, count + 1);
         index = count;
      }
      m_entries[index].feature_id = value.feature_id;
      m_entries[index].value = value;
      m_entries[index].computed_generation = m_generation;
      m_entries[index].expires_at_utc_msc = (max_age_milliseconds <= 0)
         ? m_snapshot_time.utc_epoch_milliseconds
         : value.known_time.utc_epoch_milliseconds + max_age_milliseconds;
      m_entries[index].dirty = false;
      m_entries[index].invalidation_reason = SF07_INVALIDATE_NONE;
      error = "";
      return true;
   }

   bool Get(const string feature_id, SF01_FeatureValue &value) const
   {
      const int index = FindIndex(feature_id);
      if(index < 0) return false;
      value = m_entries[index].value;
      return true;
   }

   bool IsDirty(const string feature_id) const
   {
      const int index = FindIndex(feature_id);
      return index < 0 || m_entries[index].dirty;
   }

   bool IsFresh(const string feature_id, const long at_utc_msc) const
   {
      const int index = FindIndex(feature_id);
      if(index < 0 || m_entries[index].dirty) return false;
      if(m_entries[index].expires_at_utc_msc <= 0) return true;
      return at_utc_msc <= m_entries[index].expires_at_utc_msc;
   }

   bool MarkDirty(const string feature_id,
                  const ENUM_SF07_INVALIDATION_REASON reason)
   {
      const int index = FindIndex(feature_id);
      if(index < 0) return false;
      m_entries[index].dirty = true;
      m_entries[index].invalidation_reason = reason;
      return true;
   }

   void MarkAllDirty(const ENUM_SF07_INVALIDATION_REASON reason)
   {
      const int count = ArraySize(m_entries);
      for(int i = 0; i < count; i++)
      {
         m_entries[i].dirty = true;
         m_entries[i].invalidation_reason = reason;
      }
   }

   bool EntryAt(const int index, SF07_ContextEntry &entry) const
   {
      if(index < 0 || index >= ArraySize(m_entries)) return false;
      entry = m_entries[index];
      return true;
   }
};

#endif
