#ifndef __EXP0019_FP_I02_SELF_TEST_MQH__
#define __EXP0019_FP_I02_SELF_TEST_MQH__

#include "FP_I02_Identity.mqh"
#include "FP_I02_Validation.mqh"

void FP_I02_RecordCheck(FP_I02_SelfTestResult &result,const bool passed,const string check_id)
  {
   result.check_count++;
   if(passed) result.pass_count++;
   else { result.fail_count++; result.latest_failed_check=check_id; }
  }

bool FP_I02_RunSelfTest(FP_I02_SelfTestResult &result)
  {
   ZeroMemory(result);
   result.evidence_key="FP-I02-MQL5-SELFTEST-V1";
   FP_I02_RecordCheck(result,FP_I02_RelationCount()==7,"RELATION_COUNT_7");
   FP_I02_RecordCheck(result,FP_I02_RelationRegistryValid(),"RELATION_REGISTRY_VALID");
   FP_I02_RecordCheck(result,FP_I02_ReasonCodeCount()==35,"REASON_COUNT_35");
   FP_I02_RecordCheck(result,FP_I02_IsKnownReasonCode(FP_RC_QUOTA_POLICY_UNSET),"REASON_RESOLVE");
   FP_I02_RecordCheck(result,FP_I02_CandidateTransitionAllowed(FP_CAND_OBSERVED,FP_CAND_RAW),"CANDIDATE_LEGAL_TRANSITION");
   FP_I02_RecordCheck(result,!FP_I02_CandidateTransitionAllowed(FP_CAND_CONFIRMED,FP_CAND_RAW),"CANDIDATE_TERMINAL");
   FP_I02_RecordCheck(result,FP_I02_ReferenceTransitionAllowed(FP_REF_HUNTER_SEEN,FP_REF_CONSUMED_BY_PROTECTED_TOUCH),"REFERENCE_LIFECYCLE");
   FP_I02_RecordCheck(result,FP_I02_WWTransitionAllowed(FP_WW_CONFIRMED,FP_WW_NEUTRALIZED),"WW_NEUTRALIZATION");
   FP_I02_RecordCheck(result,!FP_I02_QuotaTransitionAllowed(FP_QUOTA_RESERVED,FP_QUOTA_CONSUMED,FP_QUOTA_POLICY_UNSET),"Q12_BLOCKS_CONSUMPTION");
   FP_I02_RecordCheck(result,FP_I02_QuotaTransitionAllowed(FP_QUOTA_RESERVED,FP_QUOTA_CONSUMED,FP_QUOTA_FILLED),"QUOTA_FROZEN_PATH");

   FP_I02_SymbolPair pair;
   pair.primary_symbol="SPXUSD"; pair.secondary_symbol="NDXUSD"; pair.pair_version="1.0.0";
   pair.pair_id=FP_I02_BuildPairId(pair.primary_symbol,pair.secondary_symbol,pair.pair_version);
   string reverse=FP_I02_BuildPairId(pair.secondary_symbol,pair.primary_symbol,pair.pair_version);
   FP_I02_RecordCheck(result,pair.pair_id!="" && pair.pair_id==reverse,"PAIR_ID_ORDER_INVARIANT");

   FP_I02_WindowKey window;
   window.context_id=FP_I02_CONTEXT_ID; window.pair_id=pair.pair_id; window.kind=FP_WINDOW_A; window.scope=FP_SCOPE_SAME_TRADING_DAY;
   window.trading_day_id="NYDAY-2026-07-13"; window.start_utc_ms=1783900800000; window.end_utc_ms=1783936800000;
   window.timezone="America/New_York"; window.calendar_offset=0; window.week_id=""; window.data_revision="FIXTURE-DATA-REV-001";
   string reason="";
   FP_I02_RecordCheck(result,FP_I02_ValidateWindowKey(window,reason) && reason==FP_RC_READY,"WINDOW_VALID");
   window.window_id=FP_I02_BuildWindowId(window);
   FP_I02_RecordCheck(result,window.window_id!="","WINDOW_ID");

   string projection_a=FP_I02_BuildProjectionId("FPSIG_TEST","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","SIGNAL_LINE","CHART-A");
   string projection_b=FP_I02_BuildProjectionId("FPSIG_TEST","bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","SIGNAL_LINE","CHART-A");
   FP_I02_RecordCheck(result,projection_a!="" && projection_a!=projection_b,"PROJECTION_ID_CHANGES");

   return result.fail_count==0;
  }

#endif
