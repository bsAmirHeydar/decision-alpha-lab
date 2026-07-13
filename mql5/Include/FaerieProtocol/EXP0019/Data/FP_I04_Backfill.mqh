#ifndef __EXP0019_FP_I04_BACKFILL_MQH__
#define __EXP0019_FP_I04_BACKFILL_MQH__
#include "FP_I04_Cursor.mqh"
void FP_I04_PlanBackfill(const string symbol,const datetime start_utc,const datetime end_utc,const FP_I04_GapReason reason,const int max_minutes,FP_I04_BackfillRequest &r)
  { r.canonical_symbol=symbol;r.start_utc=start_utc;r.end_utc=end_utc;r.requested_minutes=(int)((end_utc-start_utc)/60);if(reason==FP_I04_GAP_DUPLICATE_CONFLICT){r.action=FP_I04_BACKFILL_BLOCK;r.reason_code="FP_DRC_BACKFILL_BLOCKED_CONFLICT";r.priority=0;}else if(r.requested_minutes>max_minutes){r.action=FP_I04_BACKFILL_FULL_REBUILD;r.reason_code="FP_DRC_BACKFILL_LIMIT_EXCEEDED";r.priority=10;}else{r.action=FP_I04_BACKFILL_FETCH_RANGE;r.reason_code="FP_DRC_BACKFILL_RANGE_PLANNED";r.priority=10;}r.request_id=FP_I02_CompactId("FPBACKFILL",symbol+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+IntegerToString((int)r.action)); }
#endif
