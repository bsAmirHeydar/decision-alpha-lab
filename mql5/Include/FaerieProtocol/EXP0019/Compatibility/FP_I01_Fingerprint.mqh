#ifndef __EXP0019_FP_I01_FINGERPRINT_MQH__
#define __EXP0019_FP_I01_FINGERPRINT_MQH__

string FP_I01_BoolText(const bool value) { return value ? "1" : "0"; }
string FP_I01_DoubleText(const double value) { return DoubleToString(value,10); }

string FP_I01_CGTTimeFingerprint(const SCGTTimeSnapshot &source)
  {
   return StringFormat("CGT|%I64d|%I64d|%I64d|%I64d|%I64d|%s|%d|%s",
                       (long)source.broker_now,(long)source.utc_now,(long)source.new_york_now,
                       (long)source.trading_day_start_ny,(long)source.trading_day_end_ny,
                       FP_I01_BoolText(source.inside_trading_day),source.new_york_utc_offset_hours,
                       source.trading_day_label);
  }

string FP_I01_CGRReferenceFingerprint(const SCGRReferencePair &source)
  {
   return StringFormat("CGR|%s|%d|%I64d|%I64d|%s|%s|%s|%s|%s|%s",
                       source.group_name,source.reference_cycle_index,(long)source.cycle_start_ny,
                       (long)source.cycle_end_ny,FP_I01_BoolText(source.complete_cycle),
                       FP_I01_BoolText(source.ready),source.symbol_a.symbol,source.symbol_b.symbol,
                       FP_I01_DoubleText(source.symbol_a.high),FP_I01_DoubleText(source.symbol_b.high));
  }

string FP_I01_CGHHuntFingerprint(const SCGHReferenceHuntState &source)
  {
   return StringFormat("CGH|%s|%d|%I64d|%I64d|%s|%s|%s|%s",
                       source.group_name,source.reference_cycle_index,
                       (long)source.reference_cycle_start_ny,(long)source.current_cycle_start_ny,
                       FP_I01_BoolText(source.symbol_a.high_hunted),FP_I01_BoolText(source.symbol_a.low_hunted),
                       FP_I01_BoolText(source.symbol_b.high_hunted),FP_I01_BoolText(source.symbol_b.low_hunted));
  }

string FP_I01_CGDCandidateFingerprint(const SCGDDivergenceCandidate &source)
  {
   return StringFormat("CGD|%s|%d|%d|%s|%s|%s|%s",
                       source.divergence_id,(int)source.direction,(int)source.side,
                       source.hunter_symbol,source.clean_symbol,FP_I01_BoolText(source.one_sided_hunt),
                       FP_I01_BoolText(source.data_ready));
  }

string FP_I01_CGCConfirmationFingerprint(const SCGCFinalSignal &source)
  {
   return StringFormat("CGC|%s|%d|%d|%d|%I64d|%s|%s",
                       source.signal_id,(int)source.direction,(int)source.side,(int)source.status,
                       (long)source.confirmation_time_utc,source.hunter_symbol,source.clean_symbol);
  }

string FP_I01_DAYEHuntFingerprint(const DAYE_HuntObservation &source)
  {
   return StringFormat("DAYE_HUNT|%s|%s|%d|%d|%s|%s|%I64d|%I64d",
                       source.observation_id,source.opportunity_id,(int)source.side,(int)source.pair_state,
                       source.hunter_canonical_symbol,source.protected_canonical_symbol,
                       (long)source.event_time_utc,(long)source.availability_time_utc);
  }

string FP_I01_DAYEConfirmationFingerprint(const DAYE_ConfirmationResult &source)
  {
   return StringFormat("DAYE_CONFIRM|%s|%s|%d|%d|%I64d|%I64d|%s|%s",
                       source.result_id,source.candidate_id,(int)source.outcome,(int)source.side,
                       (long)source.host_bar_open_utc,(long)source.host_bar_close_utc,
                       source.hunter_canonical_symbol,source.protected_canonical_symbol);
  }

string FP_I01_DAYELifecycleFingerprint(const DAYE_ReferenceLifecycleRecord &source)
  {
   return StringFormat("DAYE_LIFECYCLE|%s|%d|%d|%s|%s|%d|%d|%d",
                       source.reference_id,(int)source.side,(int)source.state,
                       source.first_hunter_canonical_symbol,source.protected_canonical_symbol,
                       source.accepted_use_count,source.duplicate_use_count,source.rejected_use_count);
  }

#endif
