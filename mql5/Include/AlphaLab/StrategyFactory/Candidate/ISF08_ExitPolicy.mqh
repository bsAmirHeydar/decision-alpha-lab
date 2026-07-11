#ifndef __ISF08_EXIT_POLICY_MQH__
#define __ISF08_EXIT_POLICY_MQH__
#include "SF08_TradeCandidate.mqh"

class ISF08ExitPolicy
{
public:
   virtual void Describe(SF08_PolicyDescriptor &descriptor) const=0;
   virtual ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &event,
                                                            const CSF01FeatureSnapshot &snapshot,
                                                            const SF07_ContextFrame &frame,
                                                            const SF08_PolicyParameters &parameters,
                                                            string &reason) const=0;
   virtual bool Build(const SF01_AnatomyEvent &event,
                      const CSF01FeatureSnapshot &snapshot,
                      const SF07_ContextFrame &frame,
                      const SF08_PolicyParameters &parameters,
                      SF08_ExitPlan &plan,
                      string &error) const=0;
};

#endif
