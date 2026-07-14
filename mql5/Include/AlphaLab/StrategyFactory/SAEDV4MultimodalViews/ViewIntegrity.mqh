#ifndef ALPHA_LAB_SAED_V4_VIEW_INTEGRITY_MQH
#define ALPHA_LAB_SAED_V4_VIEW_INTEGRITY_MQH
bool SAEDViewHashPresent(const string value){ return StringLen(value)==64; }
bool SAEDViewHeaderValid(const SAEDViewHeader &header){ return header.view_id!="" && header.specification_id!="" && header.twin_id!="" && SAEDViewHashPresent(header.view_hash) && SAEDViewHashPresent(header.lineage_root); }
#endif
