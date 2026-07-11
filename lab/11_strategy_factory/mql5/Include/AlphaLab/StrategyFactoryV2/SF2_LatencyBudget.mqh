#ifndef __ALPHA_LAB_SF2_LATENCY_BUDGET_MQH__
#define __ALPHA_LAB_SF2_LATENCY_BUDGET_MQH__

struct SF2_LatencyBudget
  {
   long context_us;
   long candidates_us;
   long models_us;
   long ranking_us;
   long total_us;
   bool abstain_on_breach;
  };

class SF2_LatencyTracker
  {
private:
   ulong m_total_start;
   ulong m_stage_start;
   long  m_context_us;
   long  m_candidates_us;
   long  m_models_us;
   long  m_ranking_us;

public:
         SF2_LatencyTracker(void)
     {
      Reset();
     }

   void  Reset(void)
     {
      m_total_start=GetMicrosecondCount();
      m_stage_start=m_total_start;
      m_context_us=0;
      m_candidates_us=0;
      m_models_us=0;
      m_ranking_us=0;
     }

   void  StartStage(void) { m_stage_start=GetMicrosecondCount(); }
   void  StopContext(void) { m_context_us=(long)(GetMicrosecondCount()-m_stage_start); }
   void  StopCandidates(void) { m_candidates_us=(long)(GetMicrosecondCount()-m_stage_start); }
   void  StopModels(void) { m_models_us=(long)(GetMicrosecondCount()-m_stage_start); }
   void  StopRanking(void) { m_ranking_us=(long)(GetMicrosecondCount()-m_stage_start); }
   long  TotalUs(void) const { return((long)(GetMicrosecondCount()-m_total_start)); }

   bool  Breached(const SF2_LatencyBudget &budget,string &stage) const
     {
      if(budget.context_us>0 && m_context_us>budget.context_us) { stage="context"; return(true); }
      if(budget.candidates_us>0 && m_candidates_us>budget.candidates_us) { stage="candidates"; return(true); }
      if(budget.models_us>0 && m_models_us>budget.models_us) { stage="models"; return(true); }
      if(budget.ranking_us>0 && m_ranking_us>budget.ranking_us) { stage="ranking"; return(true); }
      if(budget.total_us>0 && TotalUs()>budget.total_us) { stage="total"; return(true); }
      stage="";
      return(false);
     }
  };

#endif
