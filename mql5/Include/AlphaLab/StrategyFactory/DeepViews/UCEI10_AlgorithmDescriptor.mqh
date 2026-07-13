#ifndef __UCEI10_ALGORITHM_DESCRIPTOR_MQH__
#define __UCEI10_ALGORITHM_DESCRIPTOR_MQH__

#include "UCEI10_Enums.mqh"

struct UCEI10_AlgorithmDescriptor
  {
   string                    algorithm_id;
   string                    algorithm_version;
   UCEI10_DEEP_FAMILY        family;
   string                    formulation;
   bool                      native_algorithm;
   string                    determinism;
   string                    dependency_profile;
   string                    view_kinds;
   string                    tasks;
   string                    export_paths;
   string                    limitations;

   string Key() const
     {
      return algorithm_id+"@"+algorithm_version;
     }

   bool Valid() const
     {
      if(algorithm_id=="" || algorithm_version=="" || formulation=="")
         return false;
      if(determinism=="" || view_kinds=="" || tasks=="" || export_paths=="")
         return false;
      if(native_algorithm && dependency_profile!="")
         return false;
      return true;
     }
  };

#endif
