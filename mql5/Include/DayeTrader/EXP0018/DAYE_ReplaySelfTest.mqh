#ifndef __EXP0018_DAYE_REPLAY_SELF_TEST_MQH__
#define __EXP0018_DAYE_REPLAY_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplayAudit.mqh>

bool DAYE_RunReplaySelfTests(string &report)
{
   report="";
   string a=DAYE_ReplayHashText("same"); string b=DAYE_ReplayHashText("same");
   if(a!=b) { report="P11 self-test failed: deterministic hash"; return false; }
   if(DAYE_ReplayHashText("left")==DAYE_ReplayHashText("right")) { report="P11 self-test failed: hash separation"; return false; }

   DAYE_ConfirmationCandidate candidate; ZeroMemory(candidate);
   candidate.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION; candidate.state=DAYE_CONFIRM_CANDIDATE_PENDING;
   candidate.status=DAYE_CONFIRM_STATUS_READY; candidate.is_replay_safe=true; candidate.observation_id="OBS";
   candidate.candidate_id=DAYE_BuildConfirmationCandidateId(candidate.observation_id); candidate.opportunity_id="OPP";
   candidate.relationship_id="REL"; candidate.side=DAYE_HUNT_SIDE_HIGH; candidate.initial_pair_state=DAYE_HUNT_PAIR_A_ONLY;
   candidate.last_pair_state=DAYE_HUNT_PAIR_A_ONLY; candidate.hunter_canonical_symbol="SPX"; candidate.protected_canonical_symbol="NDX";
   candidate.hunter_broker_symbol="SPXUSD"; candidate.protected_broker_symbol="NDXUSD";
   candidate.current_period_instance_id="CURRENT"; candidate.reference_period_instance_id="REF";
   candidate.hunter_reference_price=100; candidate.protected_reference_price=200;
   candidate.target_host_open_utc=1000; candidate.target_host_close_utc=1060;
   candidate.target_host_bar_id=DAYE_BuildHostBarId(PERIOD_M1,1000,"SPX","NDX"); candidate.last_seen_availability_time_utc=1060;

   DAYE_HostBarPair host; ZeroMemory(host); host.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION; host.is_ready=true; host.is_replay_safe=true;
   host.open_time_utc=1000; host.close_time_utc=1060; host.host_bar_id=candidate.target_host_bar_id;
   host.symbol_a.is_available=true; host.symbol_a.canonical_symbol="SPX"; host.symbol_a.open=100; host.symbol_a.high=110; host.symbol_a.low=95; host.symbol_a.close=108;
   host.symbol_b.is_available=true; host.symbol_b.canonical_symbol="NDX"; host.symbol_b.open=200; host.symbol_b.high=210; host.symbol_b.low=190; host.symbol_b.close=205;
   DAYE_ConfirmationResult result;
   if(!DAYE_FinalizeCandidateAtClose(candidate,host,1060,false,result) || !result.is_confirmed || result.confirmation_endpoint_price!=110)
   { report="P11 self-test failed: pure confirmation reducer"; return false; }
   candidate.last_pair_state=DAYE_HUNT_PAIR_BOTH;
   if(!DAYE_FinalizeCandidateAtClose(candidate,host,1060,false,result) || result.outcome!=DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT)
   { report="P11 self-test failed: double hunt close"; return false; }

   report="EXP0018 P11 embedded replay self-tests: PASS"; return true;
}

#endif
