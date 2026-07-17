#ifndef AL_ACL04_DEDUPLICATION_MQH
#define AL_ACL04_DEDUPLICATION_MQH

struct AL_ACL04_DeduplicationEntry
  {
   string canonical_behavior_digest;
   string canonical_setup_id;
   string source_candidate_ids_csv;
   int    source_candidate_count;
   bool   cross_lane_equivalence;
  };

bool AL_ACL04_DeduplicationEntryIsValid(const AL_ACL04_DeduplicationEntry &entry)
  {
   return(StringFind(entry.canonical_behavior_digest,"sha256:")==0 &&
          StringLen(entry.canonical_setup_id)>0 &&
          entry.source_candidate_count>0);
  }

#endif
