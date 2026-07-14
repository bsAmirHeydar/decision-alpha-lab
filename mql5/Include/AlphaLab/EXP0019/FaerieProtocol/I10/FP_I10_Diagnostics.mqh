#ifndef __FP_I10_DIAGNOSTICS_MQH__
#define __FP_I10_DIAGNOSTICS_MQH__
#include "FP_I10_Contracts.mqh"
void FP_I10_PrintHealth(const SFP_I10_EngineSnapshot &s){ Print("FP-I10 instance=",s.instance.instance_id," health=",EnumToString(s.health.overall)," lifecycle=",EnumToString(s.health.lifecycle)," data=",EnumToString(s.health.data_readiness)," last_m1=",TimeToString(s.last_processed_m1,TIME_DATE|TIME_MINUTES)," snapshot=",s.snapshot_hash); }
#endif
