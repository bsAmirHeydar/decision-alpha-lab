#ifndef __ISF02_RESULT_SINK_MQH__
#define __ISF02_RESULT_SINK_MQH__

#include "ISF02_LifecycleService.mqh"
#include "../Contracts/SF01_AnatomyEvent.mqh"
#include "../Contracts/SF01_FeatureSnapshot.mqh"

class ISF02ResultSink : public ISF02LifecycleService
{
public:
   virtual bool WriteEvent(const SF01_AnatomyEvent &event, string &error) = 0;
   virtual bool WriteSnapshot(const CSF01FeatureSnapshot &snapshot, string &error) = 0;
   virtual bool Flush(string &error) = 0;
};

#endif
