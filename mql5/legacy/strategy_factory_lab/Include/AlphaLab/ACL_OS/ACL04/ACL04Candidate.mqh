#ifndef AL_ACL04_CANDIDATE_MQH
#define AL_ACL04_CANDIDATE_MQH

struct AL_ACL04_SetupCandidate
  {
   string candidate_id;
   string setup_id;
   string candidate_digest;
   string canonical_behavior_digest;
   string policy_ir_digest;
   string lane;
   string lifecycle_state;
   string context_id;
   string context_version;
   bool   accepted_for_research_batch;
   bool   diagnostic_only;
   bool   execution_authority;
   bool   capital_authority;
  };

bool AL_ACL04_CandidateHasSafeAuthority(const AL_ACL04_SetupCandidate &candidate)
  {
   return(!candidate.execution_authority && !candidate.capital_authority &&
          StringFind(candidate.candidate_digest,"sha256:")==0 &&
          StringFind(candidate.canonical_behavior_digest,"sha256:")==0);
  }

#endif
