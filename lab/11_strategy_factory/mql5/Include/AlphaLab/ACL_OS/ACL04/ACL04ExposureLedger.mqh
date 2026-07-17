#ifndef AL_ACL04_EXPOSURE_LEDGER_MQH
#define AL_ACL04_EXPOSURE_LEDGER_MQH

struct AL_ACL04_SearchExposureLedger
  {
   string ledger_id;
   string ledger_digest;
   string context_id;
   string context_version;
   int    requested_candidates;
   int    materialized_candidates;
   int    canonical_candidates;
   int    rejected_candidates;
   int    diagnostic_candidates;
   int    compute_units;
   bool   complete_enumeration;
   bool   baseline_budget_exempt;
  };

bool AL_ACL04_ExposureIsBounded(const AL_ACL04_SearchExposureLedger &ledger,const int max_candidates,const int max_compute_units)
  {
   return(ledger.requested_candidates>=0 &&
          ledger.materialized_candidates>=0 &&
          ledger.materialized_candidates<=max_candidates &&
          ledger.compute_units>=0 &&
          ledger.compute_units<=max_compute_units &&
          StringFind(ledger.ledger_digest,"sha256:")==0);
  }

#endif
