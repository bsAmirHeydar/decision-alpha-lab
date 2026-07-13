#ifndef __EXP0019_FP_I01_SELF_TEST_MQH__
#define __EXP0019_FP_I01_SELF_TEST_MQH__

#include "FP_I01_CGAdapters.mqh"
#include "FP_I01_DAYEAdapters.mqh"
#include "FP_I01_Registry.mqh"

void FP_I01_RecordCheck(FP_I01_SelfTestResult &result,const bool passed,const string check_id)
  {
   result.check_count++;
   if(passed) result.pass_count++;
   else { result.fail_count++; result.latest_failed_check=check_id; }
  }

bool FP_I01_RunSelfTest(FP_I01_SelfTestResult &result)
  {
   ZeroMemory(result);
   result.evidence_key="FP-I01-MQL5-SELFTEST-V1";
   FP_I01_RecordCheck(result,FP_I01_RegistryValid(),"REGISTRY_VALID");
   FP_I01_RecordCheck(result,FP_I01_AdapterCount()==8,"REGISTRY_COUNT_8");

   SCGTTimeSnapshot time_source;
   time_source.broker_now=1000; time_source.utc_now=900; time_source.new_york_now=500;
   time_source.trading_day_start_ny=0; time_source.trading_day_end_ny=1380;
   time_source.inside_trading_day=true; time_source.new_york_utc_offset_hours=-4; time_source.trading_day_label="2026-07-13";
   string time_before=FP_I01_CGTTimeFingerprint(time_source);
   FP_I01_TimeSnapshot time_target;
   FP_I01_RecordCheck(result,FP_I01_AdaptCGTTime(time_source,time_target),"CGT_ADAPT");
   FP_I01_RecordCheck(result,time_before==FP_I01_CGTTimeFingerprint(time_source),"CGT_SOURCE_UNCHANGED");
   FP_I01_RecordCheck(result,time_target.trading_day_key=="2026-07-13","CGT_OUTPUT");

   SCGRReferencePair ref_source;
   ref_source.group_name="CG60M"; ref_source.reference_cycle_index=4; ref_source.cycle_start_ny=100; ref_source.cycle_end_ny=160;
   ref_source.complete_cycle=true; ref_source.ready=true;
   ref_source.symbol_a.symbol="US500"; ref_source.symbol_a.data_ok=true; ref_source.symbol_a.high=6300; ref_source.symbol_a.low=6280;
   ref_source.symbol_a.high_time_broker=101; ref_source.symbol_a.low_time_broker=120;
   ref_source.symbol_b.symbol="USTEC"; ref_source.symbol_b.data_ok=true; ref_source.symbol_b.high=23100; ref_source.symbol_b.low=23000;
   ref_source.symbol_b.high_time_broker=104; ref_source.symbol_b.low_time_broker=130;
   string ref_before=FP_I01_CGRReferenceFingerprint(ref_source);
   FP_I01_ReferencePair ref_target;
   FP_I01_RecordCheck(result,FP_I01_AdaptCGRReference(ref_source,ref_target),"CGR_ADAPT");
   FP_I01_RecordCheck(result,ref_before==FP_I01_CGRReferenceFingerprint(ref_source),"CGR_SOURCE_UNCHANGED");
   FP_I01_RecordCheck(result,ref_target.symbol_a=="US500" && ref_target.symbol_b=="USTEC","CGR_OUTPUT");

   SCGHReferenceHuntState hunt_source;
   hunt_source.group_name="CG60M"; hunt_source.reference_cycle_index=4; hunt_source.reference_cycle_start_ny=100; hunt_source.current_cycle_start_ny=160;
   hunt_source.reference_ready=true; hunt_source.current_range_ready=true;
   hunt_source.symbol_a.symbol="US500"; hunt_source.symbol_a.reference_high=6300; hunt_source.symbol_a.reference_low=6280; hunt_source.symbol_a.current_high=6301; hunt_source.symbol_a.current_low=6285; hunt_source.symbol_a.high_hunted=true;
   hunt_source.symbol_b.symbol="USTEC"; hunt_source.symbol_b.reference_high=23100; hunt_source.symbol_b.reference_low=23000; hunt_source.symbol_b.current_high=23099; hunt_source.symbol_b.current_low=23020;
   string hunt_before=FP_I01_CGHHuntFingerprint(hunt_source);
   FP_I01_HuntObservation hunt_target;
   FP_I01_RecordCheck(result,FP_I01_AdaptCGHHunt(hunt_source,hunt_target),"CGH_ADAPT");
   FP_I01_RecordCheck(result,hunt_before==FP_I01_CGHHuntFingerprint(hunt_source),"CGH_SOURCE_UNCHANGED");
   FP_I01_RecordCheck(result,hunt_target.pair_state==FP_I01_PAIR_A_ONLY && hunt_target.hunter_symbol=="US500","CGH_OUTPUT");

   return result.fail_count==0;
  }

#endif
