#ifndef FP_I07_REVISION_INVALIDATION_MQH
#define FP_I07_REVISION_INVALIDATION_MQH
bool FP_I07_RevisionOverlapsPending(const datetime revision_start,const datetime revision_end,const datetime hunt_time,const datetime target_close) { return revision_start<target_close && revision_end>hunt_time; }
bool FP_I07_ConfirmedEvidenceIsImmutable() { return true; }
#endif
