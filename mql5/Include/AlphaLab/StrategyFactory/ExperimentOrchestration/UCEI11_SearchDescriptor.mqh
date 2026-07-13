#ifndef __UCEI11_SEARCH_DESCRIPTOR_MQH__
#define __UCEI11_SEARCH_DESCRIPTOR_MQH__

#include "UCEI11_Enums.mqh"

struct UCEI11_SearchDescriptor
  {
   string              adapter_id;
   string              adapter_version;
   UCEI11_SEARCH_KIND  kind;
   bool                native_adapter;
   bool                deterministic;
   bool                supports_constraints;
   bool                supports_multi_objective;
   bool                supports_pruning;
   string              dependency_profile;
   string              limitations;

   string Key() const
     {
      return adapter_id+"@"+adapter_version;
     }

   bool Valid() const
     {
      if(adapter_id=="" || adapter_version=="")
         return false;
      if(native_adapter && dependency_profile!="")
         return false;
      return true;
     }
  };

#endif
