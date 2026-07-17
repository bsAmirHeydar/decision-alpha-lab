#ifndef ALPHALAB_ACL05_DATASET_SNAPSHOT_MQH
#define ALPHALAB_ACL05_DATASET_SNAPSHOT_MQH
struct ACL05DatasetSnapshot { string snapshot_id; string snapshot_digest; string content_digest; datetime cut_at; datetime available_through; long row_count; bool known_time_verified; };
bool ACL05DatasetSnapshotValid(const ACL05DatasetSnapshot &x){ return StringLen(x.snapshot_id)>0 && StringLen(x.snapshot_digest)==71 && StringLen(x.content_digest)==71 && x.row_count>0 && x.available_through<=x.cut_at && x.known_time_verified; }
#endif
