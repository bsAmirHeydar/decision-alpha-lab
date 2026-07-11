#ifndef __ALPHA_LAB_SF2_PLUGIN_INTERFACES_MQH__
#define __ALPHA_LAB_SF2_PLUGIN_INTERFACES_MQH__

#include "SF2_Contracts.mqh"
#include "SF2_ContextFrame.mqh"

class ISF2_FeatureProvider
  {
public:
   virtual string    Id(void) const=0;
   virtual string    Version(void) const=0;
   virtual bool      IsFastPathSafe(void) const=0;
   virtual bool      Update(const SF2_AnatomyEvent &event,
                            const datetime decision_time_utc,
                            SF2_ContextFrame &context)=0;
  };

class ISF2_CandidateBuilder
  {
public:
   virtual string    Id(void) const=0;
   virtual bool      Build(const SF2_AnatomyEvent &event,
                           const SF2_ContextFrame &context,
                           SF2_TradeCandidate &candidate)=0;
  };

class ISF2_Model
  {
public:
   virtual string    Id(void) const=0;
   virtual string    Version(void) const=0;
   virtual bool      Predict(const SF2_ContextFrame &context,
                             const SF2_TradeCandidate &candidate,
                             SF2_CandidateScore &score)=0;
  };

class ISF2_PreDecisionGate
  {
public:
   virtual string    Id(void) const=0;
   virtual bool      Approve(const SF2_AnatomyEvent &event,
                             const SF2_ContextFrame &context,
                             string &reason_code)=0;
  };

#endif
