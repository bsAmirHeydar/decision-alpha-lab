#ifndef __UCEI10_DEPENDENCY_TRANSFER_CONTRACTS_MQH__
#define __UCEI10_DEPENDENCY_TRANSFER_CONTRACTS_MQH__

#include "UCEI10_Enums.mqh"

struct UCEI10_DependencyProbe
  {
   string                    profile;
   string                    module;
   UCEI10_DEPENDENCY_STATUS status;
   string                    detected_version;
   string                    minimum_version;
   string                    reason;
   string                    evidence_hash;

   bool Available() const
     {
      return profile!="" && module!="" &&
             status==UCEI10_DEP_AVAILABLE && evidence_hash!="";
     }
  };

struct UCEI10_TransferBoundary
  {
   string                  boundary_id;
   string                  source_dataset_manifest_hash;
   string                  target_dataset_manifest_hash;
   string                  source_row_ids_hash;
   string                  target_train_row_ids_hash;
   string                  target_final_test_row_ids_hash;
   bool                    representation_frozen;
   UCEI10_TRANSFER_DECISION decision;
   string                  blockers;
   string                  evidence_hash;

   bool Accepted() const
     {
      return boundary_id!="" && source_dataset_manifest_hash!="" &&
             target_dataset_manifest_hash!="" &&
             source_row_ids_hash!="" && target_train_row_ids_hash!="" &&
             target_final_test_row_ids_hash!="" &&
             decision==UCEI10_TRANSFER_ACCEPT && blockers=="" &&
             evidence_hash!="";
     }
  };

#endif
