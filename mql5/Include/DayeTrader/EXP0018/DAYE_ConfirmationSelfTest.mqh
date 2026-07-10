#ifndef __EXP0018_DAYE_CONFIRMATION_SELF_TEST_MQH__
#define __EXP0018_DAYE_CONFIRMATION_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationAudit.mqh>

void DAYE_MakeSyntheticCandidate(const DAYE_HuntPairState initial_state,
                                 const DAYE_HuntPairState last_state,
                                 const DAYE_HuntSide side,
                                 DAYE_ConfirmationCandidate &candidate)
{
   ZeroMemory(candidate);
   candidate.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   candidate.state=DAYE_CONFIRM_CANDIDATE_PENDING;
   candidate.status=DAYE_CONFIRM_STATUS_READY;
   candidate.candidate_id="candidate_test";
   candidate.observation_id="observation_test";
   candidate.opportunity_id="opportunity_test";
   candidate.relationship_id="DAYE_LN";
   candidate.source_alias="LN";
   candidate.is_major=true;
   candidate.chart_label="LN";
   candidate.side=side;
   candidate.initial_pair_state=initial_state;
   candidate.last_pair_state=last_state;
   candidate.hunter_canonical_symbol=(initial_state == DAYE_HUNT_PAIR_A_ONLY ? "SPX" : "NDX");
   candidate.protected_canonical_symbol=(initial_state == DAYE_HUNT_PAIR_A_ONLY ? "NDX" : "SPX");
   candidate.hunter_reference_price=100.0;
   candidate.protected_reference_price=200.0;
   candidate.first_seen_availability_time_utc=1000;
   candidate.last_seen_availability_time_utc=1800;
   candidate.target_host_open_utc=1500;
   candidate.target_host_close_utc=1800;
   candidate.target_host_bar_id="host_test";
   candidate.is_replay_safe=true;
}

void DAYE_MakeSyntheticHostPair(DAYE_HostBarPair &pair)
{
   ZeroMemory(pair);
   pair.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   pair.status=DAYE_HOST_CLOCK_READY;
   pair.is_ready=true;
   pair.is_replay_safe=true;
   pair.host_bar_id="host_test";
   pair.open_time_utc=1500;
   pair.close_time_utc=1800;
   pair.symbol_a.canonical_symbol="SPX";
   pair.symbol_a.open=101.0;
   pair.symbol_a.high=105.0;
   pair.symbol_a.low=99.0;
   pair.symbol_a.close=103.0;
   pair.symbol_b.canonical_symbol="NDX";
   pair.symbol_b.open=201.0;
   pair.symbol_b.high=205.0;
   pair.symbol_b.low=198.0;
   pair.symbol_b.close=202.0;
}

bool DAYE_RunEmbeddedConfirmationSelfTests(void)
{
   bool ok=true;
   DAYE_HostBarPair host;
   DAYE_MakeSyntheticHostPair(host);

   DAYE_ConfirmationCandidate candidate;
   DAYE_ConfirmationResult result;

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_SIDE_HIGH,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_CONFIRMED || !result.is_confirmed || result.confirmation_endpoint_price != 105.0)
   {
      Print("EXP0018 P06 self-test failed: one-sided through close must confirm with hunter HIGH endpoint.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_BOTH,DAYE_HUNT_SIDE_HIGH,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT || result.is_confirmed)
   {
      Print("EXP0018 P06 self-test failed: BOTH at close must invalidate.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_B_ONLY,DAYE_HUNT_PAIR_B_ONLY,DAYE_HUNT_SIDE_LOW,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_CONFIRMED || result.confirmation_endpoint_price != 198.0)
   {
      Print("EXP0018 P06 self-test failed: B-only LOW must use symbol B host low.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_NONE,DAYE_HUNT_SIDE_HIGH,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE)
   {
      Print("EXP0018 P06 self-test failed: NONE at close must be no-signal.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_B_ONLY,DAYE_HUNT_SIDE_HIGH,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED)
   {
      Print("EXP0018 P06 self-test failed: role change must invalidate.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_SIDE_HIGH,candidate);
   candidate.last_seen_availability_time_utc=1799;
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,false,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE)
   {
      Print("EXP0018 P06 self-test failed: source not available through close must fail closed.");
      ok=false;
   }

   DAYE_MakeSyntheticCandidate(DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_PAIR_A_ONLY,DAYE_HUNT_SIDE_HIGH,candidate);
   DAYE_FinalizeCandidateAtClose(candidate,host,1801,true,result);
   if(result.outcome != DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED)
   {
      Print("EXP0018 P06 self-test failed: missed close must require replay.");
      ok=false;
   }

   string a=DAYE_BuildConfirmationResultId("obs",1800);
   string b=DAYE_BuildConfirmationResultId("obs",1800);
   if(a != b)
   {
      Print("EXP0018 P06 self-test failed: result identity must be deterministic.");
      ok=false;
   }

   if(ok) Print("EXP0018 P06 embedded close-confirmation self-tests: PASS");
   return ok;
}

#endif
