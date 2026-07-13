#ifndef __EXP0019_FP_I01_CG_ADAPTERS_MQH__
#define __EXP0019_FP_I01_CG_ADAPTERS_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGR_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGH_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGD_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>
#include "FP_I01_Types.mqh"
#include "FP_I01_Fingerprint.mqh"

bool FP_I01_AdaptCGTTime(const SCGTTimeSnapshot &source,FP_I01_TimeSnapshot &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0017;
   target.source_type="SCGTTimeSnapshot";
   target.source_fingerprint=FP_I01_CGTTimeFingerprint(source);
   target.broker_time=source.broker_now;
   target.utc_time=source.utc_now;
   target.new_york_time=source.new_york_now;
   target.trading_day_start_ny=source.trading_day_start_ny;
   target.trading_day_end_ny=source.trading_day_end_ny;
   target.inside_trading_day=source.inside_trading_day;
   target.ny_utc_offset_hours=source.new_york_utc_offset_hours;
   target.trading_day_key=source.trading_day_label;
   target.health=FP_I01_HEALTH_READY;
   target.reason_code="CGT_SNAPSHOT_ADAPTED";
   return true;
  }

bool FP_I01_AdaptCGRReference(const SCGRReferencePair &source,FP_I01_ReferencePair &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0017;
   target.source_type="SCGRReferencePair";
   target.source_fingerprint=FP_I01_CGRReferenceFingerprint(source);
   target.reference_id=StringFormat("CGR:%s:%d:%I64d",source.group_name,source.reference_cycle_index,(long)source.cycle_start_ny);
   target.window_code=source.group_name;
   target.window_start=source.cycle_start_ny;
   target.window_end=source.cycle_end_ny;
   target.complete=source.complete_cycle;
   target.ready=(source.ready && source.symbol_a.data_ok && source.symbol_b.data_ok);
   target.symbol_a=source.symbol_a.symbol;
   target.symbol_b=source.symbol_b.symbol;
   target.high_a=source.symbol_a.high;
   target.low_a=source.symbol_a.low;
   target.high_b=source.symbol_b.high;
   target.low_b=source.symbol_b.low;
   target.high_time_a=source.symbol_a.high_time_broker;
   target.low_time_a=source.symbol_a.low_time_broker;
   target.high_time_b=source.symbol_b.high_time_broker;
   target.low_time_b=source.symbol_b.low_time_broker;
   target.data_ready_a=source.symbol_a.data_ok;
   target.data_ready_b=source.symbol_b.data_ok;
   target.health=target.ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=target.ready ? "CGR_REFERENCE_ADAPTED" : "CGR_REFERENCE_NOT_READY";
   return target.ready;
  }

bool FP_I01_AdaptCGHHunt(const SCGHReferenceHuntState &source,FP_I01_HuntObservation &target)
  {
   bool high_a=source.symbol_a.high_hunted;
   bool high_b=source.symbol_b.high_hunted;
   bool low_a=source.symbol_a.low_hunted;
   bool low_b=source.symbol_b.low_hunted;
   target.side=(high_a || high_b) ? FP_I01_SIDE_HIGH : ((low_a || low_b) ? FP_I01_SIDE_LOW : FP_I01_SIDE_NONE);
   bool hunt_a=(target.side==FP_I01_SIDE_HIGH ? high_a : (target.side==FP_I01_SIDE_LOW ? low_a : false));
   bool hunt_b=(target.side==FP_I01_SIDE_HIGH ? high_b : (target.side==FP_I01_SIDE_LOW ? low_b : false));
   target.pair_state=(hunt_a && hunt_b) ? FP_I01_PAIR_BOTH : (hunt_a ? FP_I01_PAIR_A_ONLY : (hunt_b ? FP_I01_PAIR_B_ONLY : FP_I01_PAIR_NONE));
   target.source_context=FP_I01_SOURCE_EXP0017;
   target.source_type="SCGHReferenceHuntState";
   target.source_fingerprint=FP_I01_CGHHuntFingerprint(source);
   target.reference_id=StringFormat("CGR:%s:%d:%I64d",source.group_name,source.reference_cycle_index,(long)source.reference_cycle_start_ny);
   target.opportunity_id=StringFormat("%I64d",(long)source.current_cycle_start_ny);
   target.observation_id=StringFormat("CGH:%s:%s:%d",target.reference_id,target.opportunity_id,(int)target.side);
   target.hunter_symbol=(target.pair_state==FP_I01_PAIR_A_ONLY ? source.symbol_a.symbol : (target.pair_state==FP_I01_PAIR_B_ONLY ? source.symbol_b.symbol : ""));
   target.protected_symbol=(target.pair_state==FP_I01_PAIR_A_ONLY ? source.symbol_b.symbol : (target.pair_state==FP_I01_PAIR_B_ONLY ? source.symbol_a.symbol : ""));
   target.reference_price_a=(target.side==FP_I01_SIDE_HIGH ? source.symbol_a.reference_high : source.symbol_a.reference_low);
   target.reference_price_b=(target.side==FP_I01_SIDE_HIGH ? source.symbol_b.reference_high : source.symbol_b.reference_low);
   target.current_extreme_a=(target.side==FP_I01_SIDE_HIGH ? source.symbol_a.current_high : source.symbol_a.current_low);
   target.current_extreme_b=(target.side==FP_I01_SIDE_HIGH ? source.symbol_b.current_high : source.symbol_b.current_low);
   target.event_time_utc=source.current_cycle_start_ny;
   target.availability_time_utc=source.current_cycle_start_ny;
   target.replay_safe=true;
   bool ready=(source.reference_ready && source.current_range_ready);
   target.health=ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=ready ? "CGH_HUNT_ADAPTED" : "CGH_HUNT_NOT_READY";
   return ready;
  }

bool FP_I01_AdaptCGDDivergence(const SCGDDivergenceCandidate &source,FP_I01_DivergenceCandidate &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0017;
   target.source_type="SCGDDivergenceCandidate";
   target.source_fingerprint=FP_I01_CGDCandidateFingerprint(source);
   target.candidate_id=source.divergence_id;
   target.reference_id=StringFormat("CGR:%s:%d:%I64d",source.group_name,source.reference_cycle_index,(long)source.reference_cycle_start_ny);
   target.opportunity_id=IntegerToString(source.current_cycle_index);
   target.direction=(source.direction==CGD_DIRECTION_BUY ? FP_I01_DIRECTION_BULLISH : (source.direction==CGD_DIRECTION_SELL ? FP_I01_DIRECTION_BEARISH : FP_I01_DIRECTION_NONE));
   target.side=(source.side==CGD_SIDE_HIGH ? FP_I01_SIDE_HIGH : (source.side==CGD_SIDE_LOW ? FP_I01_SIDE_LOW : FP_I01_SIDE_NONE));
   target.hunter_symbol=source.hunter_symbol;
   target.protected_symbol=source.clean_symbol;
   target.one_sided=source.one_sided_hunt;
   target.symmetric=source.both_symbols_hunted_same_side;
   target.data_ready=source.data_ready;
   target.hunter_reference_price=source.hunter_reference_price;
   target.protected_reference_price=source.clean_reference_price;
   target.event_time_utc=source.current_cycle_start_ny;
   target.health=source.data_ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code=source.data_ready ? "CGD_CANDIDATE_ADAPTED" : "CGD_CANDIDATE_NOT_READY";
   return source.data_ready;
  }

bool FP_I01_AdaptCGCConfirmation(const SCGCFinalSignal &source,FP_I01_ConfirmationResult &target)
  {
   target.source_context=FP_I01_SOURCE_EXP0017;
   target.source_type="SCGCFinalSignal";
   target.source_fingerprint=FP_I01_CGCConfirmationFingerprint(source);
   target.result_id=source.signal_id;
   target.candidate_id=source.signal_id;
   target.observation_id="";
   target.opportunity_id=IntegerToString(source.current_cycle_index);
   target.outcome=(source.status==CGC_STATUS_CONFIRMED_TRADEABLE ? FP_I01_CONFIRM_CONFIRMED : (source.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT ? FP_I01_CONFIRM_INVALIDATED_DOUBLE_HUNT : FP_I01_CONFIRM_UNAVAILABLE));
   target.direction=(source.direction==CGC_DIRECTION_BUY ? FP_I01_DIRECTION_BULLISH : (source.direction==CGC_DIRECTION_SELL ? FP_I01_DIRECTION_BEARISH : FP_I01_DIRECTION_NONE));
   target.side=(source.side==CGC_SIDE_HIGH ? FP_I01_SIDE_HIGH : (source.side==CGC_SIDE_LOW ? FP_I01_SIDE_LOW : FP_I01_SIDE_NONE));
   target.hunter_symbol=source.hunter_symbol;
   target.protected_symbol=source.clean_symbol;
   target.host_timeframe_seconds=source.confirmation_timeframe_seconds;
   target.host_bar_close_utc=source.confirmation_time_utc;
   target.host_bar_open_utc=source.confirmation_time_utc-source.confirmation_timeframe_seconds;
   target.confirmation_price=source.clean_stop_reference_price;
   target.is_final=(source.status==CGC_STATUS_CONFIRMED_TRADEABLE || source.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT);
   target.is_immutable=target.is_final;
   target.is_replay_safe=true;
   target.health=source.data_ready ? FP_I01_HEALTH_READY : FP_I01_HEALTH_DEGRADED;
   target.reason_code="CGC_CONFIRMATION_ADAPTED";
   return source.data_ready;
  }

#endif
