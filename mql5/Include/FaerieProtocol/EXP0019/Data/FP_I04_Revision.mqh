#ifndef __EXP0019_FP_I04_REVISION_MQH__
#define __EXP0019_FP_I04_REVISION_MQH__
#include "FP_I04_Coverage.mqh"
void FP_I04_BuildRevision(const string pair_id,const string parent,const FP_I04_RevisionKind kind,const datetime start_utc,const datetime end_utc,const string previous_hash,const string current_hash,FP_I04_DataRevision &r)
  { r.pair_id=pair_id;r.parent_revision_id=parent;r.kind=kind;r.affected_start_utc=start_utc;r.affected_end_utc=end_utc;r.previous_payload_hash=previous_hash;r.current_payload_hash=current_hash;r.created_utc=TimeCurrent();r.reason_code=(kind==FP_I04_REV_INITIAL?"FP_DRC_REVISION_INITIAL":kind==FP_I04_REV_APPEND?"FP_DRC_REVISION_APPEND":kind==FP_I04_REV_LATE_INSERT?"FP_DRC_REVISION_LATE_INSERT":kind==FP_I04_REV_VALUE_CORRECTION?"FP_DRC_REVISION_VALUE_CORRECTION":kind==FP_I04_REV_DELETE?"FP_DRC_REVISION_DELETE":"FP_DRC_REVISION_NO_CHANGE");r.revision_id=FP_I02_CompactId("FPREV",pair_id+"|"+parent+"|"+IntegerToString((int)kind)+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+previous_hash+"|"+current_hash); }
#endif
