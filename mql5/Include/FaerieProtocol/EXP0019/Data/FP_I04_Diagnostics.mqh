#ifndef __EXP0019_FP_I04_DIAGNOSTICS_MQH__
#define __EXP0019_FP_I04_DIAGNOSTICS_MQH__
#include "FP_I04_Synchronizer.mqh"
string FP_I04_HealthText(const FP_I04_SyncHealth h){if(h==FP_I04_SYNC_READY)return "READY";if(h==FP_I04_SYNC_DEGRADED)return "DEGRADED";return "BLOCKED";}
void FP_I04_PrintResult(const FP_I04_SyncResult &r){PrintFormat("FP-I04 result=%s pair=%s rows=%d both=%d gaps=%d conflicts=%d health=%s revision=%s",r.result_id,r.pair_id,r.row_count,r.both_present_count,r.gap_count,r.conflict_count,FP_I04_HealthText(r.health),r.revision_id);}
#endif
