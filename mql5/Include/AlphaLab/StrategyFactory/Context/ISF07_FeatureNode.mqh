#ifndef __ISF07_FEATURE_NODE_MQH__
#define __ISF07_FEATURE_NODE_MQH__

#include "SF07_FeatureDescriptor.mqh"

class CSF07ContextState;

class ISF07FeatureNode
{
public:
   virtual void GetDescriptor(SF07_FeatureDescriptor &descriptor) const = 0;
   virtual bool Compute(const SF01_AnatomyEvent &event,
                        const CSF07ContextState &state,
                        SF01_FeatureValue &value,
                        string &error) = 0;
};

#endif
