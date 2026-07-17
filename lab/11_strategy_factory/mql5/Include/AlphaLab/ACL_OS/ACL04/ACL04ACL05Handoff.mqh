#ifndef AL_ACL04_ACL05_HANDOFF_MQH
#define AL_ACL04_ACL05_HANDOFF_MQH

struct AL_ACL04_ACL05Handoff
  {
   string handoff_type;
   string handoff_digest;
   string context_id;
   string context_version;
   string upstream_acl03_handoff_digest;
   string factory_receipt_digest;
   string output_manifest_digest;
   string canonical_candidate_set_digest;
   int    canonical_candidate_count;
   bool   immutable_batch_required;
   bool   live_order_submission_allowed;
   bool   capital_activation_allowed;
  };

bool AL_ACL04_ACL05HandoffIsResearchOnly(const AL_ACL04_ACL05Handoff &handoff)
  {
   return(handoff.handoff_type=="ACL04_TO_ACL05" &&
          handoff.immutable_batch_required &&
          handoff.canonical_candidate_count>=0 &&
          !handoff.live_order_submission_allowed &&
          !handoff.capital_activation_allowed &&
          StringFind(handoff.handoff_digest,"sha256:")==0);
  }

#endif
