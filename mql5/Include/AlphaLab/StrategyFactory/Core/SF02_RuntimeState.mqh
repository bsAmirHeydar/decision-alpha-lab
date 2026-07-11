#ifndef __SF02_RUNTIME_STATE_MQH__
#define __SF02_RUNTIME_STATE_MQH__

#include "SF02_RuntimeEnums.mqh"

class CSF02RuntimeStateMachine
{
private:
   ENUM_SF02_RUNTIME_STATE m_state;
   ENUM_SF02_RUNTIME_STATE m_previous;
   long m_last_transition_utc_msc;
   string m_reason;

   bool CanTransition(const ENUM_SF02_RUNTIME_STATE from,
                      const ENUM_SF02_RUNTIME_STATE to) const
   {
      if(from == SF02_STATE_CREATED && to == SF02_STATE_INITIALIZING) return true;
      if(from == SF02_STATE_INITIALIZING && (to == SF02_STATE_READY || to == SF02_STATE_FAILED)) return true;
      if(from == SF02_STATE_READY && (to == SF02_STATE_RUNNING || to == SF02_STATE_STOPPING || to == SF02_STATE_FAILED)) return true;
      if(from == SF02_STATE_RUNNING && (to == SF02_STATE_DEGRADED || to == SF02_STATE_STOPPING || to == SF02_STATE_FAILED)) return true;
      if(from == SF02_STATE_DEGRADED && (to == SF02_STATE_RUNNING || to == SF02_STATE_STOPPING || to == SF02_STATE_FAILED)) return true;
      if(from == SF02_STATE_STOPPING && (to == SF02_STATE_STOPPED || to == SF02_STATE_FAILED)) return true;
      if(from == SF02_STATE_STOPPED && to == SF02_STATE_INITIALIZING) return true;
      return false;
   }

public:
   CSF02RuntimeStateMachine(void)
   {
      m_state = SF02_STATE_CREATED;
      m_previous = SF02_STATE_CREATED;
      m_last_transition_utc_msc = 0;
      m_reason = "created";
   }

   ENUM_SF02_RUNTIME_STATE State(void) const { return m_state; }
   ENUM_SF02_RUNTIME_STATE Previous(void) const { return m_previous; }
   long LastTransitionUtcMsc(void) const { return m_last_transition_utc_msc; }
   string Reason(void) const { return m_reason; }

   bool Transition(const ENUM_SF02_RUNTIME_STATE next,
                   const long now_utc_msc,
                   const string reason,
                   string &error)
   {
      if(!CanTransition(m_state, next))
      {
         error = "illegal runtime state transition: " +
                 SF02_RuntimeStateToString(m_state) + " -> " +
                 SF02_RuntimeStateToString(next);
         return false;
      }
      m_previous = m_state;
      m_state = next;
      m_last_transition_utc_msc = now_utc_msc;
      m_reason = reason;
      error = "";
      return true;
   }
};

#endif
