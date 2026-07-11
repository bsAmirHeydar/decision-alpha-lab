#ifndef __SF02_TYPED_EVENT_BUS_MQH__
#define __SF02_TYPED_EVENT_BUS_MQH__

#include "SF02_EventEnvelope.mqh"

class CSF02TypedEventBus
{
private:
   SF02_EventEnvelope m_buffer[];
   int m_capacity;
   int m_head;
   int m_tail;
   int m_count;
   long m_next_sequence;
   long m_dropped;
   ENUM_SF02_BUS_OVERFLOW_POLICY m_policy;

public:
   CSF02TypedEventBus(void)
   {
      m_capacity = 0;
      m_head = 0;
      m_tail = 0;
      m_count = 0;
      m_next_sequence = 1;
      m_dropped = 0;
      m_policy = SF02_BUS_REJECT_NEW;
   }

   bool Initialize(const int capacity,
                   const ENUM_SF02_BUS_OVERFLOW_POLICY policy,
                   string &error)
   {
      if(capacity < 8) { error = "event bus capacity below minimum"; return false; }
      ArrayResize(m_buffer, capacity);
      m_capacity = capacity;
      m_head = 0;
      m_tail = 0;
      m_count = 0;
      m_next_sequence = 1;
      m_dropped = 0;
      m_policy = policy;
      error = "";
      return true;
   }

   int Count(void) const { return m_count; }
   int Capacity(void) const { return m_capacity; }
   long Dropped(void) const { return m_dropped; }

   bool Publish(SF02_EventEnvelope value, string &error)
   {
      if(m_capacity <= 0) { error = "event bus not initialized"; return false; }
      if(!SF02_ValidateEventEnvelope(value, error)) return false;
      if(m_count >= m_capacity)
      {
         if(m_policy == SF02_BUS_REJECT_NEW)
         {
            m_dropped++;
            error = "event bus full";
            return false;
         }
         m_head = (m_head + 1) % m_capacity;
         m_count--;
         m_dropped++;
      }
      value.sequence = m_next_sequence++;
      m_buffer[m_tail] = value;
      m_tail = (m_tail + 1) % m_capacity;
      m_count++;
      error = "";
      return true;
   }

   bool Poll(SF02_EventEnvelope &out)
   {
      if(m_count <= 0) return false;
      out = m_buffer[m_head];
      m_head = (m_head + 1) % m_capacity;
      m_count--;
      return true;
   }
};

#endif
