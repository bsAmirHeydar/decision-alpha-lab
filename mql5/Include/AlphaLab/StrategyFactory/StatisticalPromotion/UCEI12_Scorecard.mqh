#ifndef __UCEI12_SCORECARD_MQH__
#define __UCEI12_SCORECARD_MQH__

#include "UCEI12_Contracts.mqh"

class CUCEI12Scorecard
  {
private:
   double m_weighted_sum;
   double m_weight_sum;
   int    m_critical_blockers;
   int    m_high_risks;

public:
   void Reset()
     {
      m_weighted_sum=0.0;
      m_weight_sum=0.0;
      m_critical_blockers=0;
      m_high_risks=0;
     }

   bool Add(const UCEI12_TestEvidence &evidence,const double weight)
     {
      if(!evidence.Valid() || weight<0.0)
         return false;
      double score=0.0;
      if(evidence.status==UCEI12_EVIDENCE_PASS) score=1.0;
      else if(evidence.status==UCEI12_EVIDENCE_WARN) score=0.65;
      else if(evidence.status==UCEI12_EVIDENCE_NOT_APPLICABLE) score=0.50;
      m_weighted_sum+=score*weight;
      m_weight_sum+=weight;
      if(evidence.severity==UCEI12_SEVERITY_CRITICAL &&
         (evidence.status==UCEI12_EVIDENCE_FAIL || evidence.status==UCEI12_EVIDENCE_MISSING))
         m_critical_blockers++;
      if(evidence.severity==UCEI12_SEVERITY_HIGH && evidence.status!=UCEI12_EVIDENCE_PASS)
         m_high_risks++;
      return true;
     }

   double Score() const
     {
      if(m_weight_sum<=0.0) return 0.0;
      return m_weighted_sum/m_weight_sum;
     }

   int CriticalBlockers() const { return m_critical_blockers; }
   int HighRisks() const { return m_high_risks; }
  };

#endif
