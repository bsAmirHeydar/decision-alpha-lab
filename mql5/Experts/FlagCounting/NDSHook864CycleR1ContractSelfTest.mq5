#property strict
#property version   "1.10"
#property description "No-order intrinsic plus Phase04 runtime contract diagnostic for NDS Hook 86.4 Cycle R1"

#include <FlagCountingPhoenix/FP_NDSHookTradeRules.mqh>

bool AssertCondition(const bool condition,const string code)
{
   if(condition)
      return true;
   Print("NDS_HOOK_864_SELFTEST_FAIL code=",code);
   return false;
}

void BuildPositiveSequence(FP_HookPhase02Sequence &seq)
{
   FP_ResetHookPhase02Sequence(seq);
   seq.sequence_id=55;
   seq.direction=FP_HOOK_P02_DIRECTION_POSITIVE;
   seq.state=FP_HOOK_P02_STATE_MATURE;
   seq.origin_node_id=1;
   seq.origin_time=(datetime)1000;
   seq.origin_price=100.0;
   seq.x_count=3;
   seq.cycle_crown_node_id=2;
   seq.cycle_crown_time=(datetime)1100;
   seq.cycle_crown_price=200.0;
   seq.cycle_crown_valid=true;
   seq.resolve_node_id=3;
   seq.resolve_time=(datetime)1200;
   seq.resolve_price=130.0;
   seq.resolve_confirmed=true;
   seq.retracement_ratio=0.90; // Must not own the post-Phase04 first-arrival gate.
   seq.death_boundary_price=100.0;
   seq.valid_after_hook=true;
   seq.valid_hook_family=true;
   seq.valid=true;
   seq.hook_failed=false;
}

void BuildClosedRecord(const FP_HookPhase02Sequence &seq,
                       FP_HookPhase04Record &record,
                       const bool x_closed,
                       const bool dead)
{
   FP_ResetHookPhase04Record(record);
   record.valid=true;
   record.p03.valid=true;
   record.p03.sequence=seq;
   record.lifecycle.state=(dead ? FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN :
                           (x_closed ? FP_HOOK_P04_LIFE_X_CLOSED :
                                       FP_HOOK_P04_LIFE_X_CLOSURE_CANDIDATE));
   record.lifecycle.state_reason=(dead ? "SELFTEST_DEAD" :
                                  (x_closed ? "SELFTEST_X_CLOSED" : "SELFTEST_X_OPEN"));
   record.lifecycle.has_required_x=true;
   record.lifecycle.has_required_y=true;
   record.lifecycle.x_closure_candidate=true;
   record.lifecycle.x_closed=x_closed;
   record.lifecycle.x_closure_time=(datetime)1300;
   record.lifecycle.x_closure_bar_index=1;
   record.lifecycle.x_closure_price=140.0;
   record.lifecycle.x_closure_threshold_price=150.0;
   record.lifecycle.x_closure_reference_y_price=100.0;
   record.lifecycle.x_closure_reference_y_time=(datetime)1250;
   record.lifecycle.closure_retrace_ratio=FP_NDS_HOOK_864_CLOSURE_RATIO;
   record.lifecycle.origin_return_penetrated=dead;
   record.lifecycle.death_time=(dead ? (datetime)1400 : 0);
   record.lifecycle.death_bar_index=(dead ? 2 : -1);
   record.lifecycle.death_price=(dead ? 99.0 : 0.0);
}

void BuildPositiveRates(MqlRates &rates[],const bool touch_on_closure)
{
   ArrayResize(rates,3);
   ZeroMemory(rates[0]);
   ZeroMemory(rates[1]);
   ZeroMemory(rates[2]);

   rates[0].time=(datetime)1200;
   rates[0].open=150.0;
   rates[0].high=160.0;
   rates[0].low=130.0;
   rates[0].close=145.0;

   rates[1].time=(datetime)1300;
   rates[1].open=150.0;
   rates[1].high=155.0;
   rates[1].low=(touch_on_closure ? 110.0 : 140.0);
   rates[1].close=145.0;

   rates[2].time=(datetime)1400;
   rates[2].open=140.0;
   rates[2].high=145.0;
   rates[2].low=120.0;
   rates[2].close=130.0;
}

int OnInit()
{
   FP_NDSHookTradeConfig cfg;
   FP_ResetNDSHookTradeConfig(cfg);
   cfg.profile=FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1;

   FP_HookPhase02Sequence seq;
   BuildPositiveSequence(seq);

   string reason;
   if(!AssertCondition(FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "intrinsic_x3_should_be_eligible_independent_of_terminal_ratio:"+reason))
      return INIT_FAILED;

   double entry=FP_NDSHook864CycleR1RawEntry(seq,cfg.hook_entry_ratio);
   if(!AssertCondition(MathAbs(entry-113.6)<1e-9,"positive_projection_should_equal_113_6"))
      return INIT_FAILED;

   seq.x_count=2;
   if(!AssertCondition(!FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "x2_should_be_rejected"))
      return INIT_FAILED;
   seq.x_count=3;

   FP_HookPhase04Record records[];
   ArrayResize(records,1);
   BuildClosedRecord(seq,records[0],true,false);

   MqlRates rates[];
   BuildPositiveRates(rates,false);
   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(_Symbol,_Period,
                                                rates,ArraySize(rates),records);
   FP_NDSHook864CycleR1Evidence evidence;
   if(!AssertCondition(FP_NDSHook864CycleR1RuntimeEligible(_Symbol,_Period,
                                                           seq,cfg,evidence,reason),
                       "phase04_closed_before_first_864_touch_should_be_runtime_eligible:"+reason))
      return INIT_FAILED;
   if(!AssertCondition(evidence.x_closed && !evidence.level_touched_after_closure,
                       "runtime_evidence_should_prove_closed_and_untouched"))
      return INIT_FAILED;

   BuildPositiveRates(rates,true);
   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(_Symbol,_Period,
                                                rates,ArraySize(rates),records);
   if(!AssertCondition(!FP_NDSHook864CycleR1RuntimeEligible(_Symbol,_Period,
                                                            seq,cfg,evidence,reason) &&
                       reason=="hook_864_first_arrival_already_consumed_after_closure",
                       "same_bar_closure_and_864_touch_should_fail_closed:"+reason))
      return INIT_FAILED;

   BuildClosedRecord(seq,records[0],false,false);
   BuildPositiveRates(rates,false);
   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(_Symbol,_Period,
                                                rates,ArraySize(rates),records);
   if(!AssertCondition(!FP_NDSHook864CycleR1RuntimeEligible(_Symbol,_Period,
                                                            seq,cfg,evidence,reason) &&
                       reason=="phase04_x_cycle_not_closed",
                       "unclosed_phase04_cycle_should_be_rejected:"+reason))
      return INIT_FAILED;

   BuildClosedRecord(seq,records[0],true,true);
   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(_Symbol,_Period,
                                                rates,ArraySize(rates),records);
   if(!AssertCondition(!FP_NDSHook864CycleR1RuntimeEligible(_Symbol,_Period,
                                                            seq,cfg,evidence,reason) &&
                       reason=="cycle_dead_by_origin_return_before_entry",
                       "origin_return_death_should_be_rejected:"+reason))
      return INIT_FAILED;

   // Negative geometry remains symmetric and uses the same canonical formula.
   seq.direction=FP_HOOK_P02_DIRECTION_NEGATIVE;
   seq.state=FP_HOOK_P02_STATE_CAPPED;
   seq.origin_price=200.0;
   seq.cycle_crown_price=100.0;
   seq.resolve_price=170.0;
   seq.death_boundary_price=200.0;
   seq.x_count=4;
   if(!AssertCondition(FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "golden_negative_x4_should_be_intrinsically_eligible:"+reason))
      return INIT_FAILED;
   entry=FP_NDSHook864CycleR1RawEntry(seq,cfg.hook_entry_ratio);
   if(!AssertCondition(MathAbs(entry-186.4)<1e-9,"negative_projection_should_equal_186_4"))
      return INIT_FAILED;

   cfg.hook_entry_ratio=0.860;
   if(!AssertCondition(!FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "noncanonical_ratio_should_be_rejected"))
      return INIT_FAILED;
   cfg.hook_entry_ratio=FP_NDS_HOOK_864_ENTRY_RATIO;

   FP_NDSHookTradeProfile recovered_profile;
   if(!AssertCondition(FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|S55|HH",
                                                               recovered_profile,reason) &&
                       recovered_profile==FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123,
                       "legacy_phase52_comment_should_recover_terminal_profile"))
      return INIT_FAILED;

   if(!AssertCondition(FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|864R1|S55|HH",
                                                               recovered_profile,reason) &&
                       recovered_profile==FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1,
                       "phase55_comment_should_recover_fixed_r_profile"))
      return INIT_FAILED;

   if(!AssertCondition(!FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|UNKNOWN|S55|HH",
                                                                recovered_profile,reason),
                       "unknown_profile_comment_should_fail_closed"))
      return INIT_FAILED;

   FP_NDSClearHook864CycleR1EvidenceSnapshot();
   Print("NDS_HOOK_864_SELFTEST_PASS authority_order=false ratio=",
         DoubleToString(FP_NDS_HOOK_864_ENTRY_RATIO,3),
         " closure=",DoubleToString(FP_NDS_HOOK_864_CLOSURE_RATIO,2),
         " nodes=3_or_4 reward_r=",
         DoubleToString(FP_NDS_HOOK_864_REWARD_R,1));
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Diagnostic only. No order, position, file, network, or chart authority.
}
