#ifndef AL_ACL04_SEARCH_AUTHORITY_MQH
#define AL_ACL04_SEARCH_AUTHORITY_MQH

struct AL_ACL04_SearchAuthority
  {
   string authority_id;
   string authority_digest;
   string context_id;
   string context_version;
   string upstream_handoff_digest;
   int    max_candidates;
   int    max_compute_units;
   int    max_atoms_per_candidate;
   int    max_expression_depth;
   bool   decision_allow;
   bool   live_order_submission_allowed;
   bool   capital_activation_allowed;
  };

bool AL_ACL04_SearchAuthorityIsFailClosed(const AL_ACL04_SearchAuthority &authority)
  {
   return(authority.decision_allow &&
          authority.max_candidates>0 &&
          authority.max_compute_units>0 &&
          authority.max_atoms_per_candidate>0 &&
          authority.max_expression_depth>0 &&
          !authority.live_order_submission_allowed &&
          !authority.capital_activation_allowed &&
          StringFind(authority.authority_digest,"sha256:")==0);
  }

#endif
