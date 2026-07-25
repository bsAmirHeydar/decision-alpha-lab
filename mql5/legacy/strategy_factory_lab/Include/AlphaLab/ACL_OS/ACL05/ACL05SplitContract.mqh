#ifndef ALPHALAB_ACL05_SPLIT_CONTRACT_MQH
#define ALPHALAB_ACL05_SPLIT_CONTRACT_MQH
struct ACL05SplitContract { string split_id; string method; string split_digest; datetime train_end; datetime validation_start; datetime validation_end; datetime test_start; long purge_seconds; long embargo_seconds; bool train_only_fit; };
bool ACL05SplitValid(const ACL05SplitContract &x){ return x.method=="PURGED_WALK_FORWARD" && x.train_end<x.validation_start && x.validation_end<x.test_start && x.purge_seconds>0 && x.embargo_seconds>0 && x.train_only_fit; }
#endif
