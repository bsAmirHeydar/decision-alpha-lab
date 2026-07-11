#ifndef __ALPHA_LAB_SF2_TELEMETRY_MQH__
#define __ALPHA_LAB_SF2_TELEMETRY_MQH__

struct SF2_TelemetryRow
  {
   datetime decision_time_utc;
   string   event_id;
   string   strategy_id;
   string   action;
   string   reason_code;
   int      candidate_count;
   long     total_latency_us;
   string   plan_hash;
  };

class SF2_TelemetryBuffer
  {
private:
   SF2_TelemetryRow m_rows[];
   int              m_capacity;
   int              m_count;
   int              m_cursor;

public:
                     SF2_TelemetryBuffer(void)
     {
      m_capacity=1024;
      m_count=0;
      m_cursor=0;
      ArrayResize(m_rows,m_capacity);
     }

   void              SetCapacity(const int capacity)
     {
      m_capacity=MathMax(1,capacity);
      m_count=0;
      m_cursor=0;
      ArrayResize(m_rows,m_capacity);
     }

   void              Push(const SF2_TelemetryRow &row)
     {
      m_rows[m_cursor]=row;
      m_cursor=(m_cursor+1)%m_capacity;
      if(m_count<m_capacity) m_count++;
     }

   int               Count(void) const { return(m_count); }
  };

#endif
