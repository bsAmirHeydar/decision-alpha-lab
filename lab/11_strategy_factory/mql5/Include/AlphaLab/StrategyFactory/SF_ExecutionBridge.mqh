#ifndef __ALPHA_LAB_STRATEGY_FACTORY_EXECUTION_BRIDGE_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_EXECUTION_BRIDGE_MQH__

#include "SF_Contracts.mqh"
#include "SF_RiskGate.mqh"

// This interface deliberately separates decision authority from broker I/O.
// A live implementation must be promoted and reviewed independently.
class ISF_ExecutionBridge
  {
public:
   virtual string BridgeId(void) const=0;
   virtual bool   Preview(const SF_ExecutionIntent &intent,string &reason)=0;
   virtual bool   Submit(const SF_ExecutionIntent &intent,string &broker_reference,string &reason)=0;
   virtual bool   Cancel(const string intent_id,string &reason)=0;
   virtual bool   Reconcile(string &reason)=0;
  };

#endif
