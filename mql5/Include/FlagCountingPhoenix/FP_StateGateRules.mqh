#ifndef __FP_STATE_GATE_RULES_MQH__
#define __FP_STATE_GATE_RULES_MQH__
#property strict

#include "FP_StateGateTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Rules
// ----------------------------------------------------------------------------
// Pure read-only label and tracker rules. Phase 2 owns closed-bar tracking and
// placeholder labels only. Real Rally/Hook projection remains reserved for
// Phase 3/4 and must still consume existing Phoenix anatomy only.
// ============================================================================

int FP_StateGateClampInt(const int value, const int lo, const int hi)
{
   if(value < lo) return lo;
   if(value > hi) return hi;
   return value;
}

string FP_StateGateBoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_StateGateTimeframeName(const ENUM_TIMEFRAMES tf)
{
   if(tf == PERIOD_M1)  return "M1";
   if(tf == PERIOD_M2)  return "M2";
   if(tf == PERIOD_M3)  return "M3";
   if(tf == PERIOD_M4)  return "M4";
   if(tf == PERIOD_M5)  return "M5";
   if(tf == PERIOD_M6)  return "M6";
   if(tf == PERIOD_M10) return "M10";
   if(tf == PERIOD_M12) return "M12";
   if(tf == PERIOD_M15) return "M15";
   if(tf == PERIOD_M20) return "M20";
   if(tf == PERIOD_M30) return "M30";
   if(tf == PERIOD_H1)  return "H1";
   if(tf == PERIOD_H2)  return "H2";
   if(tf == PERIOD_H3)  return "H3";
   if(tf == PERIOD_H4)  return "H4";
   if(tf == PERIOD_H6)  return "H6";
   if(tf == PERIOD_H8)  return "H8";
   if(tf == PERIOD_H12) return "H12";
   if(tf == PERIOD_D1)  return "D1";
   if(tf == PERIOD_W1)  return "W1";
   if(tf == PERIOD_MN1) return "MN1";
   if(tf == PERIOD_CURRENT) return "CURRENT";
   return EnumToString(tf);
}

ENUM_TIMEFRAMES FP_StateGateConfigTimeframeAt(const FP_StateGateConfig &cfg, const int slot)
{
   if(slot == 0) return cfg.tf1;
   if(slot == 1) return cfg.tf2;
   if(slot == 2) return cfg.tf3;
   return PERIOD_CURRENT;
}

bool FP_StateGateTimeframeIsUsable(const ENUM_TIMEFRAMES tf)
{
   return (tf != PERIOD_CURRENT);
}

string FP_StateGateClosedBarTimeLabel(const datetime t)
{
   if(t <= 0) return "no_closed_bar";
   return TimeToString(t, TIME_DATE|TIME_MINUTES);
}

string FP_StateGateCloseLabel(const double price)
{
   if(price == 0.0) return "0";
   return DoubleToString(price, _Digits);
}

string FP_StateGateDirtyLabel(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available) return "NO_DATA";
   if(!s.initialized) return "UNINIT";
   return (s.dirty ? "DIRTY" : "UNCHANGED");
}

string FP_StateGateTrackerShortLabel(const FP_StateGateTimeframeState &s)
{
   string label = s.timeframe_label;
   label += " | ";
   label += FP_StateGateDirtyLabel(s);
   label += " | closed=" + FP_StateGateClosedBarTimeLabel(s.last_closed_bar_time);
   label += " | close=" + FP_StateGateCloseLabel(s.last_closed_bar_close);
   label += " | updates=" + IntegerToString(s.update_count);
   return label;
}

string FP_StateGateRallyPlaceholderLabel(const FP_StateGateTimeframeState &tf_state)
{
   string label = tf_state.timeframe_label;
   label += " Rally View | Phase2 tracker | F projection pending";
   label += " | " + FP_StateGateDirtyLabel(tf_state);
   return label;
}

string FP_StateGateHookPlaceholderLabel(const FP_StateGateTimeframeState &tf_state)
{
   string label = tf_state.timeframe_label;
   label += " Hook View | Phase2 tracker | Hook/ND projection pending";
   label += " | " + FP_StateGateDirtyLabel(tf_state);
   return label;
}

string FP_StateGateHeaderLabel(const FP_StateGateSnapshot &snapshot)
{
   string header = "FLAG STATE GATE ";
   header += FP_STATE_GATE_VERSION;
   header += " | ";
   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      if(i > 0) header += "/";
      header += snapshot.tf_states[i].timeframe_label;
   }
   if(snapshot.any_dirty) header += " | UPDATED";
   else header += " | WAITING";
   return header;
}

void FP_StateGateSeedPlaceholderRowsForSlot(const int slot,
                                            const FP_StateGateTimeframeState &tf_state,
                                            FP_StateGateSnapshot &snapshot)
{
   if(snapshot.rally_row_count < FP_STATE_GATE_MAX_RALLY_ROWS)
   {
      int r = snapshot.rally_row_count;
      FP_ResetStateGateRallyRow(snapshot.rally_rows[r]);
      snapshot.rally_rows[r].slot_index = slot;
      snapshot.rally_rows[r].timeframe = tf_state.timeframe;
      snapshot.rally_rows[r].timeframe_label = tf_state.timeframe_label;
      snapshot.rally_rows[r].last_closed_bar_time = tf_state.last_closed_bar_time;
      snapshot.rally_rows[r].last_closed_bar_close = tf_state.last_closed_bar_close;
      snapshot.rally_rows[r].status = FP_STATE_GATE_ROW_PLACEHOLDER;
      snapshot.rally_rows[r].latest_established_f = "LATEST_ESTABLISHED_F_PENDING";
      snapshot.rally_rows[r].probable_next_f = "PROBABLE_NEXT_F_PENDING";
      snapshot.rally_rows[r].body_state = "PHASE2_TRACKER_ONLY";
      snapshot.rally_rows[r].flag_stage = "PROJECTION_PENDING";
      snapshot.rally_rows[r].post_flag_stage = "PROJECTION_PENDING";
      snapshot.rally_rows[r].label = FP_StateGateRallyPlaceholderLabel(tf_state);
      snapshot.rally_rows[r].source_id = "PHASE2_TRACKER";
      snapshot.rally_row_count++;
      snapshot.tf_states[slot].rally_row_count++;
      snapshot.tf_states[slot].latest_established_f_summary = "ESTABLISHED_F_PENDING";
      snapshot.tf_states[slot].probable_next_f_summary = "PROBABLE_NEXT_F_PENDING";
   }

   if(snapshot.hook_row_count < FP_STATE_GATE_MAX_HOOK_ROWS)
   {
      int h = snapshot.hook_row_count;
      FP_ResetStateGateHookRow(snapshot.hook_rows[h]);
      snapshot.hook_rows[h].slot_index = slot;
      snapshot.hook_rows[h].timeframe = tf_state.timeframe;
      snapshot.hook_rows[h].timeframe_label = tf_state.timeframe_label;
      snapshot.hook_rows[h].last_closed_bar_time = tf_state.last_closed_bar_time;
      snapshot.hook_rows[h].last_closed_bar_close = tf_state.last_closed_bar_close;
      snapshot.hook_rows[h].status = FP_STATE_GATE_ROW_PLACEHOLDER;
      snapshot.hook_rows[h].polarity = "HOOK_POLARITY_PENDING";
      snapshot.hook_rows[h].position_label = "PROJECTION_PENDING";
      snapshot.hook_rows[h].label = FP_StateGateHookPlaceholderLabel(tf_state);
      snapshot.hook_rows[h].source_id = "PHASE2_TRACKER";
      snapshot.hook_row_count++;
      snapshot.tf_states[slot].hook_row_count++;
      snapshot.tf_states[slot].hook_summary = "HOOK_STATE_PENDING";
   }
}

#endif // __FP_STATE_GATE_RULES_MQH__
