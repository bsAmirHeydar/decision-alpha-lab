#ifndef __EXP0019_FP_I01_REGISTRY_MQH__
#define __EXP0019_FP_I01_REGISTRY_MQH__

#include "FP_I01_Types.mqh"

int FP_I01_AdapterCount() { return 8; }

bool FP_I01_GetAdapterDescriptor(const int index,FP_I01_AdapterDescriptor &out)
  {
   out.adapter_version=FP_I01_ADAPTER_VERSION;
   out.read_only=true;
   out.broker_authority=false;
   out.order_authority=false;
   out.network_authority=false;
   out.reuse_mode="ADAPTER_REUSE";
   switch(index)
     {
      case 0: out.adapter_id="FP_CGT_TIME_ADAPTER"; out.source_context="EXP0017"; out.source_type="SCGTTimeSnapshot"; out.family="TIME"; out.dependency_id="CGT_TIME_CORE"; return true;
      case 1: out.adapter_id="FP_CGR_REFERENCE_ADAPTER"; out.source_context="EXP0017"; out.source_type="SCGRReferencePair"; out.family="REFERENCE"; out.dependency_id="CGR_REFERENCE_CORE"; return true;
      case 2: out.adapter_id="FP_CGH_HUNT_ADAPTER"; out.source_context="EXP0017"; out.source_type="SCGHReferenceHuntState"; out.family="HUNT"; out.dependency_id="CGH_HUNT_CORE"; return true;
      case 3: out.adapter_id="FP_CGD_DIVERGENCE_ADAPTER"; out.source_context="EXP0017"; out.source_type="SCGDDivergenceCandidate"; out.family="DIVERGENCE"; out.dependency_id="CGD_DIVERGENCE_CORE"; return true;
      case 4: out.adapter_id="FP_CGC_CONFIRMATION_ADAPTER"; out.source_context="EXP0017"; out.source_type="SCGCFinalSignal"; out.family="CONFIRMATION"; out.dependency_id="CGC_CONFIRMATION_CORE"; return true;
      case 5: out.adapter_id="FP_DAYE_HUNT_ADAPTER"; out.source_context="EXP0018"; out.source_type="DAYE_HuntObservation"; out.family="HUNT"; out.dependency_id="DAYE_HUNT_CORE"; return true;
      case 6: out.adapter_id="FP_DAYE_CONFIRMATION_ADAPTER"; out.source_context="EXP0018"; out.source_type="DAYE_ConfirmationResult"; out.family="CONFIRMATION"; out.dependency_id="DAYE_CONFIRMATION_CORE"; return true;
      case 7: out.adapter_id="FP_DAYE_LIFECYCLE_ADAPTER"; out.source_context="EXP0018"; out.source_type="DAYE_ReferenceLifecycleRecord"; out.family="LIFECYCLE"; out.dependency_id="DAYE_LIFECYCLE_CORE"; return true;
     }
   return false;
  }

bool FP_I01_RegistryValid()
  {
   for(int i=0;i<FP_I01_AdapterCount();i++)
     {
      FP_I01_AdapterDescriptor d;
      if(!FP_I01_GetAdapterDescriptor(i,d)) return false;
      if(d.adapter_id=="" || d.adapter_version=="" || d.source_type=="" || d.dependency_id=="") return false;
      if(!d.read_only || d.broker_authority || d.order_authority || d.network_authority) return false;
     }
   return true;
  }

#endif
