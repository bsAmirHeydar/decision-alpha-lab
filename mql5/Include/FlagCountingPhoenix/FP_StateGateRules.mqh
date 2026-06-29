#ifndef __FP_STATE_GATE_RULES_MQH__
#define __FP_STATE_GATE_RULES_MQH__
#property strict

#include "FP_StateGateTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Rules
// ----------------------------------------------------------------------------
// Pure read-only labels and projection rules. Phase 5 keeps the Phase 3/4
// Rally and Hook projections and feeds the polished dashboard. It does not
// mutate or reinterpret the locked engines.
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

bool FP_StateGateIsFLevel(const int level)
{
   return (level == FP_LEVEL_F1 || level == FP_LEVEL_F2 || level == FP_LEVEL_F3);
}

bool FP_StateGateEventIsVisibleF(const FP_FlagEvent &e)
{
   if(!FP_StateGateIsFLevel(e.level)) return false;
   if(!e.visible_main) return false;
   if(e.status == FP_STATUS_INVALIDATED) return false;
   return true;
}

bool FP_StateGateEventIsEstablishedF(const FP_FlagEvent &e)
{
   if(e.level == FP_LEVEL_F1)
      return (e.lifecycle_status == FP_F1_LC_CONFIRMED || e.lifecycle_status == FP_F1_LC_EXTENDED);
   if(e.level == FP_LEVEL_F2)
      return (e.f2_lifecycle_status == FP_F2_LC_CONFIRMED || e.f2_lifecycle_status == FP_F2_LC_EXTENDED);
   if(e.level == FP_LEVEL_F3)
      return (e.f3_lifecycle_status == FP_F3_LC_COMPLETED || e.f3_lifecycle_status == FP_F3_LC_LOCKED);
   return false;
}

bool FP_StateGateEventIsProbableF(const FP_FlagEvent &e)
{
   if(!FP_StateGateIsFLevel(e.level)) return false;
   if(FP_StateGateEventIsEstablishedF(e)) return false;
   if(e.status == FP_STATUS_INVALIDATED) return false;

   if(e.level == FP_LEVEL_F1)
      return (e.lifecycle_status == FP_F1_LC_CANDIDATE || e.lifecycle_status == FP_F1_LC_POST_FLAG || e.body_status == FP_BODY_LIVE_LEG || e.body_status == FP_BODY_LIVE_CORRECTION || e.body_status == FP_BODY_COMPLETE || e.body_status == FP_BODY_EXTENDED);
   if(e.level == FP_LEVEL_F2)
      return (e.f2_lifecycle_status == FP_F2_LC_CANDIDATE || e.f2_lifecycle_status == FP_F2_LC_POST_FLAG || e.body_status == FP_BODY_LIVE_LEG || e.body_status == FP_BODY_LIVE_CORRECTION || e.body_status == FP_BODY_COMPLETE || e.body_status == FP_BODY_EXTENDED);
   if(e.level == FP_LEVEL_F3)
      return (e.f3_lifecycle_status == FP_F3_LC_BODY_MISSING || e.f3_lifecycle_status == FP_F3_LC_OR_REJECTED || e.body_status == FP_BODY_LIVE_LEG || e.body_status == FP_BODY_LIVE_CORRECTION || e.body_status == FP_BODY_COMPLETE || e.body_status == FP_BODY_EXTENDED);
   return false;
}

string FP_StateGateLifecycleLabel(const FP_FlagEvent &e)
{
   if(e.level == FP_LEVEL_F1) return FP_F1LifecycleStatusName(e.lifecycle_status);
   if(e.level == FP_LEVEL_F2) return FP_F2LifecycleStatusName(e.f2_lifecycle_status);
   if(e.level == FP_LEVEL_F3) return FP_F3LifecycleStatusName(e.f3_lifecycle_status);
   return FP_StatusName(e.status);
}

string FP_StateGateEstablishedLabel(const FP_FlagEvent &e)
{
   if(!FP_StateGateEventIsEstablishedF(e)) return FP_STATE_GATE_RALLY_ESTABLISHED_NONE;
   string s = FP_LevelName(e.level) + "_ESTABLISHED";
   s += "|" + FP_DirectionName(e.direction);
   s += "|" + FP_StateGateLifecycleLabel(e);
   return s;
}

string FP_StateGateProbableLabel(const FP_FlagEvent &e)
{
   if(!FP_StateGateEventIsProbableF(e)) return FP_STATE_GATE_RALLY_PROBABLE_NONE;
   string s = FP_LevelName(e.level) + "_PROBABLE";
   s += "|" + FP_DirectionName(e.direction);
   s += "|" + FP_StateGateLifecycleLabel(e);
   return s;
}

bool FP_StateGateLeg2BreaksLeg1(const FP_FlagEvent &e)
{
   if(!e.has_leg1 || !e.has_leg2) return false;
   if(e.direction == FP_DIR_BULLISH) return (e.leg2.price > e.leg1.price);
   if(e.direction == FP_DIR_BEARISH) return (e.leg2.price < e.leg1.price);
   return false;
}

string FP_StateGateBodyStateLabel(const FP_FlagEvent &e)
{
   if(FP_StateGateEventIsEstablishedF(e)) return "F_ESTABLISHED";
   if(e.body_status == FP_BODY_SEED || e.body_status == FP_BODY_LIVE_LEG || e.body_status == FP_BODY_LIVE_CORRECTION)
      return "IN_FLAG_BODY";
   if(e.body_status == FP_BODY_COMPLETE || e.body_status == FP_BODY_EXTENDED)
      return "POST_FLAG_BODY";
   if(e.status == FP_STATUS_POST_FLAG) return "POST_FLAG_BODY";
   if(e.status == FP_STATUS_LIVE_LEG || e.status == FP_STATUS_LIVE_BODY) return "IN_FLAG_BODY";
   return "UNKNOWN_BODY_STATE";
}

string FP_StateGateFlagStageLabel(const FP_FlagEvent &e)
{
   if(FP_StateGateBodyStateLabel(e) != "IN_FLAG_BODY")
      return "NOT_IN_FLAG_BODY";
   if(e.has_leg2)
   {
      if(FP_StateGateLeg2BreaksLeg1(e)) return "PROBABLE_LEG2_AFTER_LEG1_BREAK";
      return "PROBABLE_LEG2_BEFORE_LEG1_BREAK";
   }
   if(e.has_waist || e.body_status == FP_BODY_LIVE_CORRECTION) return "LEG1_CORRECTION";
   if(e.has_leg1 || e.body_status == FP_BODY_LIVE_LEG) return "PROBABLE_LEG1";
   return "UNKNOWN_FLAG_STAGE";
}

string FP_StateGatePostFlagStageLabel(const FP_FlagEvent &e)
{
   if(FP_StateGateBodyStateLabel(e) == "IN_FLAG_BODY")
      return "NOT_POST_FLAG_BODY";
   if(FP_StateGateEventIsEstablishedF(e))
      return "F_CONFIRMED_BY_FLAG_BREAK";

   int c = e.internal_pack.count;
   if(c <= 0) return "BEFORE_1";
   if(c == 1) return "AFTER_1_BEFORE_2";
   if(c == 2) return "AFTER_2_BEFORE_3";
   if(c == 3) return "AFTER_3_BEFORE_4";
   return "AFTER_4_PLUS";
}

int FP_StateGateEventLastKnownPos(const FP_FlagEvent &e)
{
   int p = -1;
   if(e.pos_origin > p) p = e.pos_origin;
   if(e.pos_leg1 > p) p = e.pos_leg1;
   if(e.pos_waist > p) p = e.pos_waist;
   if(e.pos_leg2 > p) p = e.pos_leg2;
   if(e.pos_confirm > p) p = e.pos_confirm;
   if(e.pos_invalid > p) p = e.pos_invalid;
   if(e.pos_extension_end > p) p = e.pos_extension_end;
   if(e.internal_pack.last_counted_pos > p) p = e.internal_pack.last_counted_pos;
   return p;
}

string FP_StateGateEventSourceId(const FP_FlagEvent &e)
{
   if(e.canonical_id != "") return e.canonical_id;
   if(e.visual_id != "") return e.visual_id;
   if(e.structural_id != "") return e.structural_id;
   return "E" + IntegerToString(e.event_id);
}

string FP_StateGateRallyRowLabel(const FP_StateGateRallyRow &r)
{
   string label = r.timeframe_label + " Rally";
   label += " | " + FP_LevelName(r.f_level);
   label += " | " + FP_DirectionName(r.direction);
   label += " | " + r.body_state;
   if(r.flag_stage != "" && r.flag_stage != "NOT_IN_FLAG_BODY") label += " | " + r.flag_stage;
   if(r.post_flag_stage != "" && r.post_flag_stage != "NOT_POST_FLAG_BODY") label += " | " + r.post_flag_stage;
   if(r.latest_established_f != FP_STATE_GATE_RALLY_ESTABLISHED_NONE) label += " | established=" + r.latest_established_f;
   if(r.probable_next_f != FP_STATE_GATE_RALLY_PROBABLE_NONE) label += " | probable=" + r.probable_next_f;
   return label;
}

void FP_StateGateFillRallyRowFromEvent(const int slot,
                                       const FP_StateGateTimeframeState &tf_state,
                                       const FP_FlagEvent &e,
                                       FP_StateGateRallyRow &row)
{
   FP_ResetStateGateRallyRow(row);
   row.slot_index = slot;
   row.timeframe = tf_state.timeframe;
   row.timeframe_label = tf_state.timeframe_label;
   row.last_closed_bar_time = tf_state.last_closed_bar_time;
   row.last_closed_bar_close = tf_state.last_closed_bar_close;
   row.status = FP_STATE_GATE_ROW_PROJECTED;
   row.source_event_id = e.event_id;
   row.sequence_id = e.sequence_id;
   row.parent_event_id = e.parent_event_id;
   row.scale_L = e.scale_L;
   row.direction = e.direction;
   row.f_level = e.level;
   row.latest_established_f = FP_StateGateEstablishedLabel(e);
   row.probable_next_f = FP_StateGateProbableLabel(e);
   row.body_state = FP_StateGateBodyStateLabel(e);
   row.flag_stage = FP_StateGateFlagStageLabel(e);
   row.post_flag_stage = FP_StateGatePostFlagStageLabel(e);
   row.source_id = FP_StateGateEventSourceId(e);
   row.label = FP_StateGateRallyRowLabel(row);
}

int FP_StateGateFindLatestEstablishedFIndex(const FP_FlagEvent &events[])
{
   int best = -1;
   int best_pos = -1;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(!FP_StateGateEventIsVisibleF(events[i])) continue;
      if(!FP_StateGateEventIsEstablishedF(events[i])) continue;
      int p = FP_StateGateEventLastKnownPos(events[i]);
      if(best < 0 || p > best_pos || (p == best_pos && events[i].event_id > events[best].event_id))
      {
         best = i;
         best_pos = p;
      }
   }
   return best;
}

int FP_StateGateFindLatestProbableFIndex(const FP_FlagEvent &events[])
{
   int best = -1;
   int best_pos = -1;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(!FP_StateGateEventIsVisibleF(events[i])) continue;
      if(!FP_StateGateEventIsProbableF(events[i])) continue;
      int p = FP_StateGateEventLastKnownPos(events[i]);
      if(best < 0 || p > best_pos || (p == best_pos && events[i].event_id > events[best].event_id))
      {
         best = i;
         best_pos = p;
      }
   }
   return best;
}

void FP_StateGateAddNoRallyRowsForSlot(const int slot,
                                       const FP_StateGateTimeframeState &tf_state,
                                       FP_StateGateSnapshot &snapshot,
                                       const string reason)
{
   if(snapshot.rally_row_count >= FP_STATE_GATE_MAX_RALLY_ROWS) return;
   int r = snapshot.rally_row_count;
   FP_ResetStateGateRallyRow(snapshot.rally_rows[r]);
   snapshot.rally_rows[r].slot_index = slot;
   snapshot.rally_rows[r].timeframe = tf_state.timeframe;
   snapshot.rally_rows[r].timeframe_label = tf_state.timeframe_label;
   snapshot.rally_rows[r].last_closed_bar_time = tf_state.last_closed_bar_time;
   snapshot.rally_rows[r].last_closed_bar_close = tf_state.last_closed_bar_close;
   snapshot.rally_rows[r].status = FP_STATE_GATE_ROW_UNKNOWN;
   snapshot.rally_rows[r].latest_established_f = FP_STATE_GATE_RALLY_ESTABLISHED_NONE;
   snapshot.rally_rows[r].probable_next_f = FP_STATE_GATE_RALLY_PROBABLE_NONE;
   snapshot.rally_rows[r].body_state = "NO_RALLY_BODY_STATE";
   snapshot.rally_rows[r].flag_stage = reason;
   snapshot.rally_rows[r].post_flag_stage = "NO_RALLY_POST_FLAG_STATE";
   snapshot.rally_rows[r].source_id = "LEVEL19_PHASE3";
   snapshot.rally_rows[r].label = tf_state.timeframe_label + " Rally View | " + reason;
   snapshot.rally_row_count++;
   snapshot.tf_states[slot].rally_row_count++;
   snapshot.tf_states[slot].latest_established_f_summary = FP_STATE_GATE_RALLY_ESTABLISHED_NONE;
   snapshot.tf_states[slot].probable_next_f_summary = FP_STATE_GATE_RALLY_PROBABLE_NONE;
}

void FP_StateGateBuildRallyRowsForSlot(const int slot,
                                       const FP_StateGateTimeframeState &tf_state,
                                       const FP_FlagEvent &events[],
                                       const int max_rows_per_tf,
                                       FP_StateGateSnapshot &snapshot)
{
   int cap = FP_StateGateClampInt(max_rows_per_tf, 1, FP_STATE_GATE_MAX_RALLY_ROWS);
   int before_count = snapshot.rally_row_count;
   int latest_established = FP_StateGateFindLatestEstablishedFIndex(events);
   int latest_probable = FP_StateGateFindLatestProbableFIndex(events);

   snapshot.tf_states[slot].latest_established_f_summary = FP_STATE_GATE_RALLY_ESTABLISHED_NONE;
   snapshot.tf_states[slot].probable_next_f_summary = FP_STATE_GATE_RALLY_PROBABLE_NONE;

   if(latest_established >= 0 && snapshot.rally_row_count < FP_STATE_GATE_MAX_RALLY_ROWS && snapshot.tf_states[slot].rally_row_count < cap)
   {
      int r = snapshot.rally_row_count;
      FP_StateGateFillRallyRowFromEvent(slot, tf_state, events[latest_established], snapshot.rally_rows[r]);
      snapshot.tf_states[slot].latest_established_f_summary = snapshot.rally_rows[r].latest_established_f;
      snapshot.rally_row_count++;
      snapshot.tf_states[slot].rally_row_count++;
   }

   if(latest_probable >= 0 && latest_probable != latest_established && snapshot.rally_row_count < FP_STATE_GATE_MAX_RALLY_ROWS && snapshot.tf_states[slot].rally_row_count < cap)
   {
      int r = snapshot.rally_row_count;
      FP_StateGateFillRallyRowFromEvent(slot, tf_state, events[latest_probable], snapshot.rally_rows[r]);
      snapshot.tf_states[slot].probable_next_f_summary = snapshot.rally_rows[r].probable_next_f + "|" + snapshot.rally_rows[r].body_state + "|" + snapshot.rally_rows[r].flag_stage + "|" + snapshot.rally_rows[r].post_flag_stage;
      snapshot.rally_row_count++;
      snapshot.tf_states[slot].rally_row_count++;
   }

   for(int scan=ArraySize(events)-1; scan>=0; scan--)
   {
      if(snapshot.rally_row_count >= FP_STATE_GATE_MAX_RALLY_ROWS) break;
      if(snapshot.tf_states[slot].rally_row_count >= cap) break;
      if(scan == latest_established || scan == latest_probable) continue;
      if(!FP_StateGateEventIsVisibleF(events[scan])) continue;
      if(!FP_StateGateEventIsEstablishedF(events[scan]) && !FP_StateGateEventIsProbableF(events[scan])) continue;

      int r = snapshot.rally_row_count;
      FP_StateGateFillRallyRowFromEvent(slot, tf_state, events[scan], snapshot.rally_rows[r]);
      snapshot.rally_row_count++;
      snapshot.tf_states[slot].rally_row_count++;
   }

   if(snapshot.rally_row_count == before_count)
      FP_StateGateAddNoRallyRowsForSlot(slot, tf_state, snapshot, FP_STATE_GATE_RALLY_NO_ROWS);
}

string FP_StateGateHookPlaceholderLabel(const FP_StateGateTimeframeState &tf_state)
{
   string label = tf_state.timeframe_label;
   label += " Hook View | tracker only | Hook/ND projection pending";
   label += " | " + FP_StateGateDirtyLabel(tf_state);
   return label;
}

void FP_StateGateSeedHookPlaceholderForSlot(const int slot,
                                            const FP_StateGateTimeframeState &tf_state,
                                            FP_StateGateSnapshot &snapshot)
{
   if(snapshot.hook_row_count >= FP_STATE_GATE_MAX_HOOK_ROWS) return;
   int h = snapshot.hook_row_count;
   FP_ResetStateGateHookRow(snapshot.hook_rows[h]);
   snapshot.hook_rows[h].slot_index = slot;
   snapshot.hook_rows[h].timeframe = tf_state.timeframe;
   snapshot.hook_rows[h].timeframe_label = tf_state.timeframe_label;
   snapshot.hook_rows[h].last_closed_bar_time = tf_state.last_closed_bar_time;
   snapshot.hook_rows[h].last_closed_bar_close = tf_state.last_closed_bar_close;
   snapshot.hook_rows[h].status = FP_STATE_GATE_ROW_PLACEHOLDER;
   snapshot.hook_rows[h].polarity = "HOOK_POLARITY_PENDING";
   snapshot.hook_rows[h].position_label = "PHASE4_PROJECTION_PENDING";
   snapshot.hook_rows[h].label = FP_StateGateHookPlaceholderLabel(tf_state);
   snapshot.hook_rows[h].source_id = "TRACKER_ONLY";
   snapshot.hook_row_count++;
   snapshot.tf_states[slot].hook_row_count++;
   snapshot.tf_states[slot].hook_summary = "HOOK_VIEW_PENDING";
}

string FP_StateGateHookPolarityLabel(const FP_HookBranch &h)
{
   if(h.direction == FP_DIR_BULLISH) return "POSITIVE_HOOK_REVERSAL_UP";
   if(h.direction == FP_DIR_BEARISH) return "NEGATIVE_HOOK_REVERSAL_DOWN";
   return "HOOK_POLARITY_UNKNOWN";
}

bool FP_StateGateHookIsProjectable(const FP_HookBranch &h)
{
   if(h.branch_id < 0) return false;
   if(h.node_count <= 0) return false;
   if(h.status == FP_STATUS_INVALIDATED) return false;
   if(h.is_cycle_start_broken) return false;
   return true;
}

void FP_StateGateConsiderNodeForHighLow(const FP_Node &n,
                                        FP_Node &latest_high,
                                        bool &has_high,
                                        FP_Node &latest_low,
                                        bool &has_low)
{
   if(n.id < 0) return;
   if(n.kind == FP_NODE_HIGH)
   {
      if(!has_high || n.index_anchor > latest_high.index_anchor ||
         (n.index_anchor == latest_high.index_anchor && n.id > latest_high.id))
      {
         latest_high = n;
         has_high = true;
      }
   }
   else if(n.kind == FP_NODE_LOW)
   {
      if(!has_low || n.index_anchor > latest_low.index_anchor ||
         (n.index_anchor == latest_low.index_anchor && n.id > latest_low.id))
      {
         latest_low = n;
         has_low = true;
      }
   }
}

void FP_StateGateExtractHookLatestHighLow(const FP_HookBranch &h,
                                          FP_Node &latest_high,
                                          bool &has_high,
                                          FP_Node &latest_low,
                                          bool &has_low)
{
   has_high = false;
   has_low = false;
   if(h.has_cycle_start) FP_StateGateConsiderNodeForHighLow(h.cycle_start_node, latest_high, has_high, latest_low, has_low);
   FP_StateGateConsiderNodeForHighLow(h.start_node, latest_high, has_high, latest_low, has_low);
   if(h.node_count >= 1) FP_StateGateConsiderNodeForHighLow(h.n1, latest_high, has_high, latest_low, has_low);
   if(h.node_count >= 2) FP_StateGateConsiderNodeForHighLow(h.n2, latest_high, has_high, latest_low, has_low);
   if(h.node_count >= 3) FP_StateGateConsiderNodeForHighLow(h.n3, latest_high, has_high, latest_low, has_low);
   if(h.node_count >= 4) FP_StateGateConsiderNodeForHighLow(h.n4, latest_high, has_high, latest_low, has_low);
   FP_StateGateConsiderNodeForHighLow(h.extreme_node, latest_high, has_high, latest_low, has_low);
   FP_StateGateConsiderNodeForHighLow(h.resolve_node, latest_high, has_high, latest_low, has_low);
}

string FP_StateGateHookSourceId(const FP_HookBranch &h)
{
   if(h.audit_id != "") return h.audit_id;
   if(h.chain_id != "") return h.chain_id;
   if(h.phase_id != "") return h.phase_id;
   if(h.visual_id != "") return h.visual_id;
   if(h.structural_id != "") return h.structural_id;
   return "H" + IntegerToString(h.branch_id);
}

string FP_StateGateHookPositionLabel(const FP_HookBranch &h)
{
   string s = "NODE_" + IntegerToString(h.node_count) + "_CONFIRMED";
   if(h.is_nd) s += "|ND";
   else s += "|HOOK";
   if(h.visible_main) s += "|VISIBLE";
   else s += "|HIDDEN";
   if(h.seeds_visible_f1) s += "|SEEDS_VISIBLE_F1";
   if(h.has_cycle_start) s += "|CYCLE_BOUNDARY=" + IntegerToString(h.cycle_start_node.id);
   s += "|RESOLVE=" + IntegerToString(h.resolve_node.id);
   return s;
}

string FP_StateGateHookRowLabel(const FP_StateGateHookRow &r)
{
   string label = r.timeframe_label + " Hook";
   label += " | L" + IntegerToString(r.scale_L);
   label += " | " + FP_DirectionName(r.direction);
   label += " | " + r.polarity;
   label += " | N" + IntegerToString(r.current_node_number);
   label += " | " + r.position_label;
   if(r.latest_high_node_id >= 0)
      label += " | H#" + IntegerToString(r.latest_high_node_id) + "=" + FP_StateGateCloseLabel(r.latest_high_node_price);
   if(r.latest_low_node_id >= 0)
      label += " | L#" + IntegerToString(r.latest_low_node_id) + "=" + FP_StateGateCloseLabel(r.latest_low_node_price);
   return label;
}

void FP_StateGateFillHookRowFromBranch(const int slot,
                                       const FP_StateGateTimeframeState &tf_state,
                                       const FP_HookBranch &h,
                                       FP_StateGateHookRow &row)
{
   FP_ResetStateGateHookRow(row);
   row.slot_index = slot;
   row.timeframe = tf_state.timeframe;
   row.timeframe_label = tf_state.timeframe_label;
   row.last_closed_bar_time = tf_state.last_closed_bar_time;
   row.last_closed_bar_close = tf_state.last_closed_bar_close;
   row.status = FP_STATE_GATE_ROW_PROJECTED;
   row.source_hook_id = h.branch_id;
   row.sequence_id = h.branch_id;
   row.scale_L = h.scale_L;
   row.direction = h.direction;
   row.polarity = FP_StateGateHookPolarityLabel(h);
   row.current_node_number = h.node_count;

   FP_Node latest_high;
   FP_Node latest_low;
   bool has_high = false;
   bool has_low = false;
   FP_StateGateExtractHookLatestHighLow(h, latest_high, has_high, latest_low, has_low);
   if(has_high)
   {
      row.latest_high_node_id = latest_high.id;
      row.latest_high_node_price = latest_high.price;
   }
   if(has_low)
   {
      row.latest_low_node_id = latest_low.id;
      row.latest_low_node_price = latest_low.price;
   }

   row.position_label = FP_StateGateHookPositionLabel(h);
   row.source_id = FP_StateGateHookSourceId(h);
   row.label = FP_StateGateHookRowLabel(row);
}

bool FP_StateGateHookCandidateBetter(const FP_HookBranch &candidate, const FP_HookBranch &current)
{
   if(candidate.visible_main != current.visible_main) return candidate.visible_main;
   if(candidate.scale_L != current.scale_L) return (candidate.scale_L > current.scale_L);
   if(candidate.node_count != current.node_count) return (candidate.node_count > current.node_count);
   if(candidate.is_nd != current.is_nd) return candidate.is_nd;
   if(candidate.resolve_node.index_anchor != current.resolve_node.index_anchor) return (candidate.resolve_node.index_anchor > current.resolve_node.index_anchor);
   return (candidate.branch_id > current.branch_id);
}

int FP_StateGateFindNextHookIndex(const FP_HookBranch &hooks[], bool &used[])
{
   int best = -1;
   for(int i=0; i<ArraySize(hooks); i++)
   {
      if(used[i]) continue;
      if(!FP_StateGateHookIsProjectable(hooks[i])) continue;
      if(best < 0 || FP_StateGateHookCandidateBetter(hooks[i], hooks[best]))
         best = i;
   }
   return best;
}

void FP_StateGateAddNoHookRowsForSlot(const int slot,
                                      const FP_StateGateTimeframeState &tf_state,
                                      FP_StateGateSnapshot &snapshot,
                                      const string reason)
{
   if(snapshot.hook_row_count >= FP_STATE_GATE_MAX_HOOK_ROWS) return;
   int h = snapshot.hook_row_count;
   FP_ResetStateGateHookRow(snapshot.hook_rows[h]);
   snapshot.hook_rows[h].slot_index = slot;
   snapshot.hook_rows[h].timeframe = tf_state.timeframe;
   snapshot.hook_rows[h].timeframe_label = tf_state.timeframe_label;
   snapshot.hook_rows[h].last_closed_bar_time = tf_state.last_closed_bar_time;
   snapshot.hook_rows[h].last_closed_bar_close = tf_state.last_closed_bar_close;
   snapshot.hook_rows[h].status = FP_STATE_GATE_ROW_UNKNOWN;
   snapshot.hook_rows[h].polarity = "NO_HOOK_POLARITY";
   snapshot.hook_rows[h].position_label = reason;
   snapshot.hook_rows[h].source_id = "LEVEL19_PHASE4";
   snapshot.hook_rows[h].label = tf_state.timeframe_label + " Hook View | " + reason;
   snapshot.hook_row_count++;
   snapshot.tf_states[slot].hook_row_count++;
   snapshot.tf_states[slot].hook_summary = FP_STATE_GATE_HOOK_NO_ROWS + "|" + reason;
}

void FP_StateGateBuildHookRowsForSlot(const int slot,
                                      const FP_StateGateTimeframeState &tf_state,
                                      const FP_HookBranch &hooks[],
                                      const int max_rows_per_tf,
                                      FP_StateGateSnapshot &snapshot)
{
   int cap = FP_StateGateClampInt(max_rows_per_tf, 1, FP_STATE_GATE_MAX_HOOK_ROWS);
   int before_count = snapshot.hook_row_count;
   bool used[];
   ArrayResize(used, ArraySize(hooks));
   for(int u=0; u<ArraySize(used); u++) used[u] = false;

   while(snapshot.hook_row_count < FP_STATE_GATE_MAX_HOOK_ROWS && snapshot.tf_states[slot].hook_row_count < cap)
   {
      int best = FP_StateGateFindNextHookIndex(hooks, used);
      if(best < 0) break;
      used[best] = true;
      int h = snapshot.hook_row_count;
      FP_StateGateFillHookRowFromBranch(slot, tf_state, hooks[best], snapshot.hook_rows[h]);
      if(snapshot.tf_states[slot].hook_row_count == 0)
         snapshot.tf_states[slot].hook_summary = snapshot.hook_rows[h].polarity + "|L" + IntegerToString(snapshot.hook_rows[h].scale_L) + "|N" + IntegerToString(snapshot.hook_rows[h].current_node_number);
      snapshot.hook_row_count++;
      snapshot.tf_states[slot].hook_row_count++;
   }

   if(snapshot.hook_row_count == before_count)
      FP_StateGateAddNoHookRowsForSlot(slot, tf_state, snapshot, FP_STATE_GATE_HOOK_NO_ROWS);
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
      snapshot.rally_rows[r].label = tf_state.timeframe_label + " Rally View | Phase2 tracker | F projection pending | " + FP_StateGateDirtyLabel(tf_state);
      snapshot.rally_rows[r].source_id = "PHASE2_TRACKER";
      snapshot.rally_row_count++;
      snapshot.tf_states[slot].rally_row_count++;
      snapshot.tf_states[slot].latest_established_f_summary = "ESTABLISHED_F_PENDING";
      snapshot.tf_states[slot].probable_next_f_summary = "PROBABLE_NEXT_F_PENDING";
   }

   FP_StateGateSeedHookPlaceholderForSlot(slot, tf_state, snapshot);
}

#endif // __FP_STATE_GATE_RULES_MQH__
