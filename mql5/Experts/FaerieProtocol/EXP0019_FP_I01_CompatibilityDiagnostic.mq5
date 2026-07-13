#property strict
#property version   "1.00"
#property description "EXP0019 FP-I01 compatibility registry diagnostic"

#include <FaerieProtocol/EXP0019/Compatibility/FP_I01_All.mqh>

int OnInit()
  {
   PrintFormat("FP-I01 adapter registry version=%s count=%d valid=%s",FP_I01_ADAPTER_VERSION,FP_I01_AdapterCount(),FP_I01_RegistryValid() ? "true" : "false");
   for(int i=0;i<FP_I01_AdapterCount();i++)
     {
      FP_I01_AdapterDescriptor d;
      if(FP_I01_GetAdapterDescriptor(i,d))
         PrintFormat("adapter[%d]=%s@%s source=%s type=%s family=%s dependency=%s read_only=%s",
                     i,d.adapter_id,d.adapter_version,d.source_context,d.source_type,d.family,d.dependency_id,d.read_only ? "true" : "false");
     }
   return FP_I01_RegistryValid() ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick() {}
