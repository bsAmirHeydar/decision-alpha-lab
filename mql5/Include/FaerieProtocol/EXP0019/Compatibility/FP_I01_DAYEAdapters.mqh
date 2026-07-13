#ifndef __EXP0019_FP_I01_DAYE_ADAPTERS_MQH__
#define __EXP0019_FP_I01_DAYE_ADAPTERS_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntTypes.mqh>
#include <DayeTrader/EXP0018/DAYE_ConfirmationTypes.mqh>
#include <DayeTrader/EXP0018/DAYE_LifecycleTypes.mqh>
#include "FP_I01_Types.mqh"
#include "FP_I01_Fingerprint.mqh"

FP_I01_HuntSide FP_I01_FromDAYESide(const DAYE_HuntSide side)
  {
   if(side==DAYE_HUNT_SIDE_HIGH) return FP_I01_SIDE_HIGH;
   if(side==DAYE_HUNT_SIDE_LOW) return FP_I01_SIDE_LOW;
   return FP_I01_SIDE_NONE;
  }

FP_I01_PairState FP_I01_FromDAYEPairState(const DAYE_HuntPairState state)
  {
   if(state==DAYE_HUNT_PAIR_A_ONLY) return FP_I01_PAIR_A_ONLY;
   if(state==DAYE_HUNT_PAIR_B_ONLY) return FP_I01_PAIR_B_ONLY;
   if(state==DAYE_HUNT_PAIR_BOTH) return FP_I01_PAIR_BOTH;
   if(state==DAYE_HUNT_PAIR_NONE) return FP_I01_PAIR_NONE;
   return FP_I01_PAIR_UNAVAILABLE;
  }

bool FP_I01_AdaptDAYEHunt(const DAYE_HuntObservation &source,FP_I01_HuntObservation &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0018;
   target.source_type="DAYE_HuntObservation";
   target.source_fingerprint=FP_I01_DAYEHuntFingerprint(source);
   target.observation_id=source.observation_id;
   target.reference_id=source.reference_period_instance_id;
   target.opportunity_id=source.opportunity_id;
   target.side=FP_I01_FromDAYESide(source.side);
   target.pair_state=FP_I01_FromDAYEPairState(source.pair_state);
   target.hunter_symbol=source.hunter_canonical_symbol;
   target.protected_symbol=source.protected_canonical_symbol;
   target.reference_price_a=source.symbol_a.reference_price;
   target.reference_price_b=source.symbol_b.reference_price;
   target.current_extreme_a=source.symbol_a.current_extreme;
   target.current_extreme_b=source.symbol_b.current_extreme;
   target.event_time_utc=source.event_time_utc;
   target.availability_time_utc=source.availability_time_utc;
   target.replay_safe=source.is_replay_safe;
   bool ready=(source.status==DAYE_HUNT_STATUS_READY);
   target.health=ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=source.reason_code;
   return ready;
  }

bool FP_I01_AdaptDAYEConfirmation(const DAYE_ConfirmationResult &source,FP_I01_ConfirmationResult &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0018;
   target.source_type="DAYE_ConfirmationResult";
   target.source_fingerprint=FP_I01_DAYEConfirmationFingerprint(source);
   target.result_id=source.result_id;
   target.candidate_id=source.candidate_id;
   target.observation_id=source.observation_id;
   target.opportunity_id=source.opportunity_id;
   if(source.outcome==DAYE_CONFIRM_OUTCOME_CONFIRMED) target.outcome=FP_I01_CONFIRM_CONFIRMED;
   else if(source.outcome==DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT) target.outcome=FP_I01_CONFIRM_INVALIDATED_DOUBLE_HUNT;
   else if(source.outcome==DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE) target.outcome=FP_I01_CONFIRM_NO_SIGNAL_AT_CLOSE;
   else if(source.outcome==DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED) target.outcome=FP_I01_CONFIRM_ROLE_CHANGED;
   else if(source.outcome==DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED) target.outcome=FP_I01_CONFIRM_MISSED_CLOSE;
   else target.outcome=FP_I01_CONFIRM_UNAVAILABLE;
   target.side=FP_I01_FromDAYESide(source.side);
   target.direction=(target.side==FP_I01_SIDE_HIGH ? FP_I01_DIRECTION_BEARISH : (target.side==FP_I01_SIDE_LOW ? FP_I01_DIRECTION_BULLISH : FP_I01_DIRECTION_NONE));
   target.hunter_symbol=source.hunter_canonical_symbol;
   target.protected_symbol=source.protected_canonical_symbol;
   target.host_timeframe_seconds=(int)(source.host_bar_close_utc-source.host_bar_open_utc);
   target.host_bar_open_utc=source.host_bar_open_utc;
   target.host_bar_close_utc=source.host_bar_close_utc;
   target.confirmation_price=source.confirmation_endpoint_price;
   target.is_final=source.is_final;
   target.is_immutable=source.is_immutable;
   target.is_replay_safe=source.is_replay_safe;
   bool ready=(source.status==DAYE_CONFIRM_STATUS_READY);
   target.health=ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=source.reason_code;
   return ready;
  }

bool FP_I01_AdaptDAYELifecycle(const DAYE_ReferenceLifecycleRecord &source,FP_I01_LifecycleRecord &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0018;
   target.source_type="DAYE_ReferenceLifecycleRecord";
   target.source_fingerprint=FP_I01_DAYELifecycleFingerprint(source);
   target.reference_id=source.reference_id;
   target.side=FP_I01_FromDAYESide(source.side);
   target.protected_symbol=source.protected_canonical_symbol;
   target.first_hunter_symbol=source.first_hunter_canonical_symbol;
   target.state=DAYE_ReferenceLifecycleStateToString(source.state);
   target.retired=source.is_retired;
   target.accepted_use_count=source.accepted_use_count;
   target.duplicate_use_count=source.duplicate_use_count;
   target.rejected_use_count=source.rejected_use_count;
   target.activation_time_utc=source.activation_event_time_utc;
   target.retirement_time_utc=source.retirement_event_time_utc;
   target.immutable=source.is_immutable;
   target.replay_safe=source.is_replay_safe;
   bool ready=(source.status==DAYE_LIFECYCLE_STATUS_READY);
   target.health=ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=source.reason_code;
   return ready;
  }

#endif
