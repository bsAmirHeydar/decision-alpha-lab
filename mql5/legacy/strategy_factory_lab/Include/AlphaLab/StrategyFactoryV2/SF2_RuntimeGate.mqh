#ifndef __ALPHA_LAB_SF2_RUNTIME_GATE_MQH__
#define __ALPHA_LAB_SF2_RUNTIME_GATE_MQH__

class SF2_RuntimeGate
  {
private:
   bool   m_kill_switch;
   bool   m_model_ready;
   bool   m_context_ready;
   bool   m_paper_mode;
   string m_last_reason;

public:
         SF2_RuntimeGate(void)
     {
      m_kill_switch=false;
      m_model_ready=false;
      m_context_ready=false;
      m_paper_mode=true;
      m_last_reason="not_initialized";
     }

   void  SetKillSwitch(const bool value) { m_kill_switch=value; }
   void  SetModelReady(const bool value) { m_model_ready=value; }
   void  SetContextReady(const bool value) { m_context_ready=value; }
   void  SetPaperMode(const bool value) { m_paper_mode=value; }

   bool  Approve(string &reason)
     {
      if(m_kill_switch) { reason="kill_switch"; m_last_reason=reason; return(false); }
      if(!m_model_ready) { reason="model_not_ready"; m_last_reason=reason; return(false); }
      if(!m_context_ready) { reason="context_not_ready"; m_last_reason=reason; return(false); }
      reason="approved";
      m_last_reason=reason;
      return(true);
     }

   bool  PaperMode(void) const { return(m_paper_mode); }
   string LastReason(void) const { return(m_last_reason); }
  };

#endif
