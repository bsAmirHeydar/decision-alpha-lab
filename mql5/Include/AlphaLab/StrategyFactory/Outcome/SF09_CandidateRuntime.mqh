#ifndef __SF09_CANDIDATE_RUNTIME_MQH__
#define __SF09_CANDIDATE_RUNTIME_MQH__
#include "../Candidate/SF08_AllCandidate.mqh"
#include "SF09_OutcomeRecord.mqh"
#include "SF09_SimulationPolicy.mqh"

class CSF09CandidateRuntime
{
public:
   SF08_TradeCandidate candidate;
   ENUM_SF09_RUNTIME_STATE state;
   SF01_MarketTimestamp registered_at;
   long last_observation_sequence;
   SF01_MarketTimestamp last_observation_time;
   bool filled;
   SF01_MarketTimestamp fill_time;
   double fill_price;
   double entry_spread_points;
   double remaining_fraction;
   double realized_weighted_points;
   bool target_consumed;
   bool ambiguity_seen;
   ENUM_SF09_DATA_FIDELITY fidelity;
   CSF09PathTracker path;

   CSF09CandidateRuntime(void){Reset();}
   void Reset(void)
   {
      state=SF09_STATE_EMPTY;
      last_observation_sequence=-1;
      filled=false;
      fill_price=0.0;
      entry_spread_points=0.0;
      remaining_fraction=1.0;
      realized_weighted_points=0.0;
      target_consumed=false;
      ambiguity_seen=false;
      fidelity=SF09_FIDELITY_UNKNOWN;
      path.Reset();
   }
};

#endif
