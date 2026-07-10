#ifndef __EXP0018_DAYE_LIFECYCLE_SELF_TEST_MQH__
#define __EXP0018_DAYE_LIFECYCLE_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleAudit.mqh>

void DAYE_P07BuildTestResult(const string result_id,const string opportunity_id,const string current_id,
                             const string reference_id,const string hunter,const string protected,
                             const DAYE_HuntSide side,const datetime t,DAYE_ConfirmationResult &r)
{
   ZeroMemory(r); r.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION; r.status=DAYE_CONFIRM_STATUS_READY;
   r.outcome=DAYE_CONFIRM_OUTCOME_CONFIRMED; r.is_final=true; r.is_confirmed=true; r.is_immutable=true; r.is_replay_safe=true;
   r.result_id=result_id; r.candidate_id="C_"+result_id; r.observation_id="O_"+result_id; r.opportunity_id=opportunity_id;
   r.relationship_id="LN"; r.source_alias="LN"; r.is_major=true; r.chart_label="LN"; r.side=side;
   r.close_pair_state=hunter=="SPX"?DAYE_HUNT_PAIR_A_ONLY:DAYE_HUNT_PAIR_B_ONLY;
   r.hunter_broker_symbol=hunter; r.hunter_canonical_symbol=hunter; r.protected_broker_symbol=protected; r.protected_canonical_symbol=protected;
   r.current_period_instance_id=current_id; r.reference_period_instance_id=reference_id;
   r.hunter_reference_price=100.0; r.protected_reference_price=200.0; r.host_bar_open_utc=t-300; r.host_bar_close_utc=t;
   r.host_bar_id="HB_"+IntegerToString((int)t); r.hunter_host_open=99; r.hunter_host_high=101; r.hunter_host_low=98; r.hunter_host_close=100;
   r.confirmation_endpoint_price=side==DAYE_HUNT_SIDE_HIGH?101:98; r.event_time_utc=t; r.availability_time_utc=t; r.processing_time_utc=t;
}

bool DAYE_RunLifecycleSelfTests(string &report)
{
   report="";
   DAYE_LifecycleConfig cfg; ZeroMemory(cfg); cfg.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   cfg.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a="SPX";
   cfg.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b="NDX";
   cfg.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a="SPX";
   cfg.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b="NDX";
   cfg.retire_on_protected_touch=true; cfg.retire_on_double_hunt=true; cfg.retire_on_role_switch=true;

   DAYE_ConfirmationResult first; DAYE_P07BuildTestResult("R1","OP1","CUR1","REF1","SPX","NDX",DAYE_HUNT_SIDE_HIGH,1000,first);
   DAYE_ReferenceLifecycleRecord ref; string reason="";
   if(!DAYE_InitializeReferenceRecord(cfg,first,ref,reason)) { report="initialize_reference_failed_"+reason; return false; }
   if(ref.state!=DAYE_REF_STATE_PROTECTED_SURVIVES || ref.protected_canonical_symbol!="NDX") { report="initial_state_wrong"; return false; }

   DAYE_ReferenceUseRecord use; DAYE_BuildUseRecord(first,ref.reference_id,DAYE_USE_STATUS_ACCEPTED,"accepted",1000,use);
   if(!use.is_accepted || use.exact_opportunity_use_key=="") { report="accepted_use_wrong"; return false; }

   DAYE_HuntObservation obs; ZeroMemory(obs); obs.schema_version=DAYE_HUNT_SCHEMA_VERSION; obs.status=DAYE_HUNT_STATUS_READY;
   obs.reference_period_instance_id="REF1"; obs.side=DAYE_HUNT_SIDE_HIGH; obs.observation_id="OBS_BREACH";
   obs.event_time_utc=1100; obs.availability_time_utc=1100; obs.pair_state=DAYE_HUNT_PAIR_B_ONLY; obs.is_one_sided=true;
   obs.hunter_canonical_symbol="NDX"; obs.symbol_a.canonical_symbol="SPX"; obs.symbol_a.is_available=true; obs.symbol_a.is_hunted=false;
   obs.symbol_b.canonical_symbol="NDX"; obs.symbol_b.is_available=true; obs.symbol_b.is_hunted=true;
   DAYE_ReferenceLifecycleState before; DAYE_LifecycleEventType et; string rr="";
   if(!DAYE_ApplyObservationToReference(cfg,obs,ref,before,et,rr)) { report="protected_breach_not_applied"; return false; }
   if(ref.state!=DAYE_REF_STATE_RETIRED_ROLE_SWITCH || !ref.is_retired) { report="role_switch_not_retired"; return false; }

   DAYE_ReferenceLifecycleState retired=ref.state;
   DAYE_HuntObservation later=obs; later.observation_id="OBS_LATER"; later.availability_time_utc=1200;
   DAYE_ApplyObservationToReference(cfg,later,ref,before,et,rr);
   if(ref.state!=retired) { report="retired_reference_reentered"; return false; }

   report="EXP0018 P07 lifecycle self-tests PASS"; return true;
}

#endif
