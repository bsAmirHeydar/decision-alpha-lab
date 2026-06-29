#ifndef __FP_STATE_GATE_RULES_MQH__
#define __FP_STATE_GATE_RULES_MQH__
#property strict

#include "FP_StateGateTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Rules
// ----------------------------------------------------------------------------
// Pure read-only labels and projection rules. Phase 6 keeps the Phase 3/4
// Rally and Hook projections, preserves the Phase 5 dashboard polish, and adds
// stable State Contract labels and Phase 11 Entry Bridge readiness fields. It does not
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

string FP_StateGateBaseCornerName(const int corner)
{
   if(corner == CORNER_LEFT_UPPER)  return "CORNER_LEFT_UPPER";
   if(corner == CORNER_LEFT_LOWER)  return "CORNER_LEFT_LOWER";
   if(corner == CORNER_RIGHT_UPPER) return "CORNER_RIGHT_UPPER";
   if(corner == CORNER_RIGHT_LOWER) return "CORNER_RIGHT_LOWER";
   return "CORNER_UNKNOWN_" + IntegerToString(corner);
}

string FP_StateGateEffectiveCornerName(const FP_StateGateConfig &cfg)
{
   if(cfg.panel_force_left_upper)
      return "CORNER_LEFT_UPPER_FORCED";
   if(cfg.panel_force_right_upper)
      return "CORNER_RIGHT_UPPER_FORCED";
   return FP_StateGateBaseCornerName(cfg.panel_corner);
}

string FP_StateGatePanelPlacementKey(const FP_StateGateConfig &cfg)
{
   string s = FP_StateGateEffectiveCornerName(cfg);
   s += "|x=" + IntegerToString(cfg.panel_x);
   s += "|y=" + IntegerToString(cfg.panel_y);
   s += "|w=" + IntegerToString(cfg.panel_width);
   s += "|font=" + IntegerToString(cfg.panel_font_size);
   return s;
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


int FP_StateGateProjectedRallyRowsForSlot(const FP_StateGateSnapshot &snapshot, const int slot)
{
   int count = 0;
   for(int r=0; r<snapshot.rally_row_count; r++)
      if(snapshot.rally_rows[r].slot_index == slot && snapshot.rally_rows[r].status == FP_STATE_GATE_ROW_PROJECTED)
         count++;
   return count;
}

int FP_StateGateProjectedHookRowsForSlot(const FP_StateGateSnapshot &snapshot, const int slot)
{
   int count = 0;
   for(int h=0; h<snapshot.hook_row_count; h++)
      if(snapshot.hook_rows[h].slot_index == slot && snapshot.hook_rows[h].status == FP_STATE_GATE_ROW_PROJECTED)
         count++;
   return count;
}

string FP_StateGateKeyPart(string raw)
{
   string s = raw;
   if(s == "") return "NA";
   StringReplace(s, " ", "_");
   StringReplace(s, "\t", "_");
   StringReplace(s, "\r", "_");
   StringReplace(s, "\n", "_");
   StringReplace(s, ",", "_");
   StringReplace(s, ";", "_");
   return s;
}

string FP_StateGateFirstProjectedRallyKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   for(int r=0; r<snapshot.rally_row_count; r++)
   {
      FP_StateGateRallyRow row = snapshot.rally_rows[r];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED) continue;
      string key = FP_LevelName(row.f_level);
      key += "|" + FP_DirectionName(row.direction);
      key += "|L" + IntegerToString(row.scale_L);
      key += "|E" + IntegerToString(row.source_event_id);
      key += "|" + FP_StateGateKeyPart(row.body_state);
      if(row.flag_stage != "" && row.flag_stage != "NOT_IN_FLAG_BODY") key += "|" + FP_StateGateKeyPart(row.flag_stage);
      if(row.post_flag_stage != "" && row.post_flag_stage != "NOT_POST_FLAG_BODY") key += "|" + FP_StateGateKeyPart(row.post_flag_stage);
      return key;
   }
   return "NO_PROJECTED_RALLY_ROW";
}

string FP_StateGateFirstProjectedHookKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   for(int h=0; h<snapshot.hook_row_count; h++)
   {
      FP_StateGateHookRow row = snapshot.hook_rows[h];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED) continue;
      string key = FP_StateGateKeyPart(row.polarity);
      key += "|" + FP_DirectionName(row.direction);
      key += "|L" + IntegerToString(row.scale_L);
      key += "|N" + IntegerToString(row.current_node_number);
      key += "|H" + IntegerToString(row.latest_high_node_id);
      key += "|Lw" + IntegerToString(row.latest_low_node_id);
      key += "|HK" + IntegerToString(row.source_hook_id);
      return key;
   }
   return "NO_PROJECTED_HOOK_ROW";
}

string FP_StateGateSlotAnatomyStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available) return "NO_CLOSED_BAR_ANATOMY";
   int rally_projected = FP_StateGateProjectedRallyRowsForSlot(snapshot, slot);
   int hook_projected = FP_StateGateProjectedHookRowsForSlot(snapshot, slot);
   if(rally_projected > 0 && hook_projected > 0) return "RALLY_AND_HOOK_PROJECTED";
   if(rally_projected > 0) return "RALLY_PROJECTED_HOOK_PENDING";
   if(hook_projected > 0) return "HOOK_PROJECTED_RALLY_PENDING";
   return "ANATOMY_NOT_PROJECTED";
}

string FP_StateGateSlotContractStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available) return FP_STATE_GATE_CONTRACT_NO_DATA;
   int rally_projected = FP_StateGateProjectedRallyRowsForSlot(snapshot, slot);
   int hook_projected = FP_StateGateProjectedHookRowsForSlot(snapshot, slot);
   if(rally_projected > 0 && hook_projected > 0) return FP_STATE_GATE_CONTRACT_READY;
   return FP_STATE_GATE_CONTRACT_PARTIAL;
}

string FP_StateGateSlotEntryBridgeStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   string status = FP_StateGateSlotContractStatus(snapshot, slot);
   if(status == FP_STATE_GATE_CONTRACT_READY) return "ENTRY_CONTEXT_READY_NO_DECISION";
   if(status == FP_STATE_GATE_CONTRACT_PARTIAL) return "ENTRY_CONTEXT_PARTIAL_NO_DECISION";
   return "ENTRY_CONTEXT_BLOCKED_NO_CLOSED_BAR";
}

string FP_StateGateSlotStorageStatus(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available) return "NO_STORAGE_WITHOUT_CLOSED_BAR";
   if(s.dirty) return "STORED_NEW_CLOSED_BAR_STATE";
   return "STORED_UNCHANGED_CLOSED_BAR_STATE";
}

string FP_StateGateSlotStateKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string key = snapshot.symbol;
   key += "|TF=" + s.timeframe_label;
   key += "|T=" + FP_StateGateKeyPart(FP_StateGateClosedBarTimeLabel(s.last_closed_bar_time));
   key += "|U=" + IntegerToString(s.update_count);
   key += "|R=" + FP_StateGateKeyPart(s.primary_rally_key);
   key += "|H=" + FP_StateGateKeyPart(s.primary_hook_key);
   key += "|RR=" + IntegerToString(s.rally_row_count);
   key += "|HR=" + IntegerToString(s.hook_row_count);
   return key;
}


bool FP_StateGateFirstProjectedRallyRowForSlot(const FP_StateGateSnapshot &snapshot,
                                               const int slot,
                                               FP_StateGateRallyRow &out)
{
   for(int r=0; r<snapshot.rally_row_count; r++)
   {
      FP_StateGateRallyRow row = snapshot.rally_rows[r];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateFirstProjectedHookRowForSlot(const FP_StateGateSnapshot &snapshot,
                                              const int slot,
                                              FP_StateGateHookRow &out)
{
   for(int h=0; h<snapshot.hook_row_count; h++)
   {
      FP_StateGateHookRow row = snapshot.hook_rows[h];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED)
         continue;
      out = row;
      return true;
   }
   return false;
}

string FP_StateGateSlotEntryBridgeReadiness(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "ENTRY_BRIDGE_BLOCKED_NO_CLOSED_BAR";
   int rally_projected = FP_StateGateProjectedRallyRowsForSlot(snapshot, slot);
   int hook_projected = FP_StateGateProjectedHookRowsForSlot(snapshot, slot);
   if(rally_projected > 0 && hook_projected > 0)
      return "ENTRY_BRIDGE_READY_FOR_EXTREME_MAPPING_NO_DECISION";
   if(rally_projected > 0)
      return "ENTRY_BRIDGE_RALLY_ONLY_NEEDS_HOOK_CONTEXT_NO_DECISION";
   if(hook_projected > 0)
      return "ENTRY_BRIDGE_HOOK_ONLY_NEEDS_RALLY_CONTEXT_NO_DECISION";
   return "ENTRY_BRIDGE_NOT_READY_NO_PROJECTED_ANATOMY";
}

string FP_StateGateSlotCandidateExtremeStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "CANDIDATE_EXTREME_BLOCKED_NO_CLOSED_BAR";
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0)
      return "CANDIDATE_EXTREME_FROM_HOOK_CONTEXT_NO_PRICE";
   if(FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "CANDIDATE_EXTREME_FROM_RALLY_CONTEXT_NO_PRICE";
   return "CANDIDATE_EXTREME_NOT_AVAILABLE";
}

string FP_StateGateSlotCandidateExtremeKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateHookRow h;
   FP_ResetStateGateHookRow(h);
   if(FP_StateGateFirstProjectedHookRowForSlot(snapshot, slot, h))
   {
      string key = "HOOK_CANDIDATE";
      key += "|POL=" + FP_StateGateKeyPart(h.polarity);
      key += "|DIR=" + FP_DirectionName(h.direction);
      key += "|L=" + IntegerToString(h.scale_L);
      key += "|N=" + IntegerToString(h.current_node_number);
      key += "|H=" + IntegerToString(h.latest_high_node_id);
      key += "|Lw=" + IntegerToString(h.latest_low_node_id);
      key += "|HK=" + IntegerToString(h.source_hook_id);
      return key;
   }

   FP_StateGateRallyRow r;
   FP_ResetStateGateRallyRow(r);
   if(FP_StateGateFirstProjectedRallyRowForSlot(snapshot, slot, r))
   {
      string key = "RALLY_CANDIDATE";
      key += "|F=" + FP_LevelName(r.f_level);
      key += "|DIR=" + FP_DirectionName(r.direction);
      key += "|L=" + IntegerToString(r.scale_L);
      key += "|E=" + IntegerToString(r.source_event_id);
      key += "|BODY=" + FP_StateGateKeyPart(r.body_state);
      key += "|FLAG=" + FP_StateGateKeyPart(r.flag_stage);
      key += "|POST=" + FP_StateGateKeyPart(r.post_flag_stage);
      return key;
   }

   return "NO_CANDIDATE_EXTREME_KEY";
}

string FP_StateGateSlotCandidateExtremeSource(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0)
      return "HOOK_VIEW_PRIMARY";
   if(FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "RALLY_VIEW_PRIMARY";
   return "NO_CANDIDATE_SOURCE";
}

string FP_StateGateSlotCandidateDirection(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateHookRow h;
   FP_ResetStateGateHookRow(h);
   if(FP_StateGateFirstProjectedHookRowForSlot(snapshot, slot, h))
      return FP_DirectionName(h.direction);

   FP_StateGateRallyRow r;
   FP_ResetStateGateRallyRow(r);
   if(FP_StateGateFirstProjectedRallyRowForSlot(snapshot, slot, r))
      return FP_DirectionName(r.direction);

   return "NO_DIRECTION";
}

string FP_StateGateSlotCandidateScaleContext(const FP_StateGateSnapshot &snapshot, const int slot)
{
   string s = "RALLY_ROWS=" + IntegerToString(FP_StateGateProjectedRallyRowsForSlot(snapshot, slot));
   s += "|HOOK_ROWS=" + IntegerToString(FP_StateGateProjectedHookRowsForSlot(snapshot, slot));
   s += "|PRIMARY_R=" + FP_StateGateKeyPart(snapshot.tf_states[slot].primary_rally_key);
   s += "|PRIMARY_H=" + FP_StateGateKeyPart(snapshot.tf_states[slot].primary_hook_key);
   return s;
}

string FP_StateGateSlotXInvalidationStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "X_INVALIDATION_BLOCKED_NO_CLOSED_BAR";
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0 || FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "X_INVALIDATION_PENDING_GEOMETRY_NO_PRICE";
   return "X_INVALIDATION_NOT_AVAILABLE";
}

string FP_StateGateSlotXDestinationStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "X_DESTINATION_BLOCKED_NO_CLOSED_BAR";
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0 || FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "X_DESTINATION_PENDING_GEOMETRY_NO_PRICE";
   return "X_DESTINATION_NOT_AVAILABLE";
}

string FP_StateGateSlotOptionalityStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "OPTIONALITY_BLOCKED_NO_CLOSED_BAR";
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0 || FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "OPTIONALITY_PENDING_X_GEOMETRY_NO_R";
   return "OPTIONALITY_NOT_AVAILABLE";
}

string FP_StateGateSlotEntryBridgeKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   string key = snapshot.symbol;
   key += "|TF=" + snapshot.tf_states[slot].timeframe_label;
   key += "|READINESS=" + FP_StateGateKeyPart(snapshot.tf_states[slot].entry_bridge_readiness);
   key += "|CAND=" + FP_StateGateKeyPart(snapshot.tf_states[slot].candidate_extreme_key);
   key += "|DIR=" + FP_StateGateKeyPart(snapshot.tf_states[slot].candidate_direction);
   key += "|XI=" + FP_StateGateKeyPart(snapshot.tf_states[slot].x_invalidation_status);
   key += "|XD=" + FP_StateGateKeyPart(snapshot.tf_states[slot].x_destination_status);
   key += "|OPT=" + FP_StateGateKeyPart(snapshot.tf_states[slot].optionality_status);
   return key;
}


// ---------------------------------------------------------------------------
// Phase 12 - Extreme Candidate Map
// ---------------------------------------------------------------------------
// This layer maps existing read-only Rally/Hook projection rows into candidate
// X-extreme context rows. It still does not produce entry, stop, target, or
// order decisions.

string FP_StateGateExtremeSideFromHook(const FP_StateGateHookRow &h)
{
   if(StringFind(h.polarity, "POSITIVE") >= 0) return "LOW_EXTREME";
   if(StringFind(h.polarity, "NEGATIVE") >= 0) return "HIGH_EXTREME";
   if(h.direction == FP_DIR_BULLISH) return "LOW_EXTREME";
   if(h.direction == FP_DIR_BEARISH) return "HIGH_EXTREME";
   return "UNKNOWN_EXTREME_SIDE";
}

int FP_StateGateExtremeNodeFromHook(const FP_StateGateHookRow &h, const string side)
{
   if(side == "LOW_EXTREME") return h.latest_low_node_id;
   if(side == "HIGH_EXTREME") return h.latest_high_node_id;
   return -1;
}

double FP_StateGateExtremePriceFromHook(const FP_StateGateHookRow &h, const string side)
{
   if(side == "LOW_EXTREME") return h.latest_low_node_price;
   if(side == "HIGH_EXTREME") return h.latest_high_node_price;
   return 0.0;
}

string FP_StateGateExtremePriceStatusFromHook(const FP_StateGateHookRow &h, const string side)
{
   int node_id = FP_StateGateExtremeNodeFromHook(h, side);
   double price = FP_StateGateExtremePriceFromHook(h, side);
   if(node_id >= 0 && price != 0.0) return "EXTREME_PRICE_FROM_HOOK_NODE_CONTEXT_ONLY";
   if(node_id >= 0) return "EXTREME_NODE_WITHOUT_PRICE_CONTEXT_ONLY";
   return "EXTREME_PRICE_PENDING_NODE_CONTEXT";
}

string FP_StateGateExtremeSourceKeyFromHook(const FP_StateGateHookRow &h,
                                            const string side,
                                            const int rank)
{
   string key = "HOOK_EXTREME";
   key += "|RANK=" + IntegerToString(rank);
   key += "|POL=" + FP_StateGateKeyPart(h.polarity);
   key += "|DIR=" + FP_DirectionName(h.direction);
   key += "|SIDE=" + FP_StateGateKeyPart(side);
   key += "|L=" + IntegerToString(h.scale_L);
   key += "|NODE=" + IntegerToString(FP_StateGateExtremeNodeFromHook(h, side));
   key += "|HK=" + IntegerToString(h.source_hook_id);
   return key;
}

string FP_StateGateExtremeSourceKeyFromRally(const FP_StateGateRallyRow &r,
                                             const int rank)
{
   string key = "RALLY_EXTREME_CONTEXT";
   key += "|RANK=" + IntegerToString(rank);
   key += "|F=" + FP_LevelName(r.f_level);
   key += "|DIR=" + FP_DirectionName(r.direction);
   key += "|L=" + IntegerToString(r.scale_L);
   key += "|E=" + IntegerToString(r.source_event_id);
   key += "|BODY=" + FP_StateGateKeyPart(r.body_state);
   key += "|FLAG=" + FP_StateGateKeyPart(r.flag_stage);
   key += "|POST=" + FP_StateGateKeyPart(r.post_flag_stage);
   return key;
}

bool FP_StateGateAddExtremeCandidateFromHookRow(FP_StateGateSnapshot &snapshot,
                                                const int slot,
                                                const FP_StateGateHookRow &h,
                                                const int rank)
{
   if(snapshot.extreme_candidate_row_count >= FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS)
      return false;

   int idx = snapshot.extreme_candidate_row_count;
   FP_ResetStateGateExtremeCandidateRow(snapshot.extreme_candidate_rows[idx]);

   string side = FP_StateGateExtremeSideFromHook(h);
   int node_id = FP_StateGateExtremeNodeFromHook(h, side);
   double price = FP_StateGateExtremePriceFromHook(h, side);
   string price_status = FP_StateGateExtremePriceStatusFromHook(h, side);

   snapshot.extreme_candidate_rows[idx].slot_index = slot;
   snapshot.extreme_candidate_rows[idx].timeframe = h.timeframe;
   snapshot.extreme_candidate_rows[idx].timeframe_label = h.timeframe_label;
   snapshot.extreme_candidate_rows[idx].last_closed_bar_time = h.last_closed_bar_time;
   snapshot.extreme_candidate_rows[idx].last_closed_bar_close = h.last_closed_bar_close;
   snapshot.extreme_candidate_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.extreme_candidate_rows[idx].source_kind = "HOOK_VIEW";
   snapshot.extreme_candidate_rows[idx].source_id = h.source_id;
   snapshot.extreme_candidate_rows[idx].source_row_index = h.source_hook_id;
   snapshot.extreme_candidate_rows[idx].direction = h.direction;
   snapshot.extreme_candidate_rows[idx].direction_label = FP_DirectionName(h.direction);
   snapshot.extreme_candidate_rows[idx].side = side;
   snapshot.extreme_candidate_rows[idx].role = "HOOK_REVERSAL_EXTREME_CONTEXT";
   snapshot.extreme_candidate_rows[idx].scale_L = h.scale_L;
   snapshot.extreme_candidate_rows[idx].node_id = node_id;
   snapshot.extreme_candidate_rows[idx].price = price;
   snapshot.extreme_candidate_rows[idx].price_status = price_status;
   snapshot.extreme_candidate_rows[idx].rank = rank;
   snapshot.extreme_candidate_rows[idx].source_key = FP_StateGateExtremeSourceKeyFromHook(h, side, rank);
   snapshot.extreme_candidate_rows[idx].readiness = "EXTREME_CANDIDATE_MAPPED_FROM_HOOK_NO_DECISION";
   snapshot.extreme_candidate_rows[idx].label = h.timeframe_label + " | HOOK EXTREME | " + side + " | " + FP_DirectionName(h.direction) + " | L" + IntegerToString(h.scale_L) + " | node=" + IntegerToString(node_id) + " | " + price_status;

   snapshot.extreme_candidate_row_count++;
   snapshot.tf_states[slot].extreme_candidate_row_count++;
   return true;
}

bool FP_StateGateAddExtremeCandidateFromRallyRow(FP_StateGateSnapshot &snapshot,
                                                 const int slot,
                                                 const FP_StateGateRallyRow &r,
                                                 const int rank)
{
   if(snapshot.extreme_candidate_row_count >= FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS)
      return false;

   int idx = snapshot.extreme_candidate_row_count;
   FP_ResetStateGateExtremeCandidateRow(snapshot.extreme_candidate_rows[idx]);

   snapshot.extreme_candidate_rows[idx].slot_index = slot;
   snapshot.extreme_candidate_rows[idx].timeframe = r.timeframe;
   snapshot.extreme_candidate_rows[idx].timeframe_label = r.timeframe_label;
   snapshot.extreme_candidate_rows[idx].last_closed_bar_time = r.last_closed_bar_time;
   snapshot.extreme_candidate_rows[idx].last_closed_bar_close = r.last_closed_bar_close;
   snapshot.extreme_candidate_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.extreme_candidate_rows[idx].source_kind = "RALLY_VIEW";
   snapshot.extreme_candidate_rows[idx].source_id = r.source_id;
   snapshot.extreme_candidate_rows[idx].source_row_index = r.source_event_id;
   snapshot.extreme_candidate_rows[idx].direction = r.direction;
   snapshot.extreme_candidate_rows[idx].direction_label = FP_DirectionName(r.direction);
   snapshot.extreme_candidate_rows[idx].side = "RALLY_CONTEXT_SIDE_PENDING";
   snapshot.extreme_candidate_rows[idx].role = "RALLY_BODY_OR_POST_FLAG_EXTREME_CONTEXT";
   snapshot.extreme_candidate_rows[idx].scale_L = r.scale_L;
   snapshot.extreme_candidate_rows[idx].node_id = -1;
   snapshot.extreme_candidate_rows[idx].price = 0.0;
   snapshot.extreme_candidate_rows[idx].price_status = "RALLY_CONTEXT_NO_EXTREME_PRICE";
   snapshot.extreme_candidate_rows[idx].rank = rank;
   snapshot.extreme_candidate_rows[idx].source_key = FP_StateGateExtremeSourceKeyFromRally(r, rank);
   snapshot.extreme_candidate_rows[idx].readiness = "EXTREME_CANDIDATE_CONTEXT_FROM_RALLY_NO_DECISION";
   snapshot.extreme_candidate_rows[idx].label = r.timeframe_label + " | RALLY EXTREME CONTEXT | " + FP_LevelName(r.f_level) + " | " + FP_DirectionName(r.direction) + " | L" + IntegerToString(r.scale_L) + " | " + r.body_state + " | " + r.flag_stage + " | " + r.post_flag_stage;

   snapshot.extreme_candidate_row_count++;
   snapshot.tf_states[slot].extreme_candidate_row_count++;
   return true;
}

int FP_StateGateBuildExtremeCandidatesForSlot(FP_StateGateSnapshot &snapshot,
                                              const int slot,
                                              const int max_candidates_per_tf)
{
   int limit = FP_StateGateClampInt(max_candidates_per_tf, 0, 24);
   if(limit <= 0) return 0;

   int made = 0;

   for(int h=0; h<snapshot.hook_row_count && made < limit; h++)
   {
      FP_StateGateHookRow row = snapshot.hook_rows[h];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED)
         continue;
      if(FP_StateGateAddExtremeCandidateFromHookRow(snapshot, slot, row, made))
         made++;
   }

   for(int r=0; r<snapshot.rally_row_count && made < limit; r++)
   {
      FP_StateGateRallyRow row = snapshot.rally_rows[r];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED)
         continue;
      if(FP_StateGateAddExtremeCandidateFromRallyRow(snapshot, slot, row, made))
         made++;
   }

   return made;
}

void FP_StateGateBuildExtremeCandidateRows(FP_StateGateSnapshot &snapshot,
                                           const int max_candidates_per_tf)
{
   snapshot.extreme_candidate_row_count = 0;
   for(int x=0; x<FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS; x++)
      FP_ResetStateGateExtremeCandidateRow(snapshot.extreme_candidate_rows[x]);

   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      snapshot.tf_states[i].extreme_candidate_row_count = 0;
      FP_StateGateBuildExtremeCandidatesForSlot(snapshot, i, max_candidates_per_tf);
   }
}

bool FP_StateGateFirstExtremeCandidateForSlot(const FP_StateGateSnapshot &snapshot,
                                              const int slot,
                                              FP_StateGateExtremeCandidateRow &out)
{
   for(int x=0; x<snapshot.extreme_candidate_row_count; x++)
   {
      FP_StateGateExtremeCandidateRow row = snapshot.extreme_candidate_rows[x];
      if(row.slot_index != slot || row.status != FP_STATE_GATE_ROW_PROJECTED)
         continue;
      out = row;
      return true;
   }
   return false;
}

string FP_StateGateSlotExtremeMapStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(!snapshot.tf_states[slot].closed_bar_available)
      return "EXTREME_MAP_BLOCKED_NO_CLOSED_BAR";
   if(snapshot.tf_states[slot].extreme_candidate_row_count > 0)
      return "EXTREME_MAP_READY_CONTEXT_ONLY_NO_DECISION";
   if(FP_StateGateProjectedHookRowsForSlot(snapshot, slot) > 0 || FP_StateGateProjectedRallyRowsForSlot(snapshot, slot) > 0)
      return "EXTREME_MAP_NO_ROWS_DESPITE_ANATOMY_CHECK_CSV";
   return "EXTREME_MAP_NOT_READY_NO_PROJECTED_ANATOMY";
}

string FP_StateGateSlotExtremeMapKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateExtremeCandidateRow x;
   FP_ResetStateGateExtremeCandidateRow(x);
   if(FP_StateGateFirstExtremeCandidateForSlot(snapshot, slot, x))
   {
      string key = snapshot.symbol;
      key += "|TF=" + snapshot.tf_states[slot].timeframe_label;
      key += "|XMAP=" + FP_StateGateKeyPart(x.source_key);
      key += "|ROWS=" + IntegerToString(snapshot.tf_states[slot].extreme_candidate_row_count);
      return key;
   }
   return "NO_EXTREME_MAP_KEY";
}

void FP_StateGateFinalizeSlotExtremeMap(FP_StateGateSnapshot &snapshot, const int slot)
{
   snapshot.tf_states[slot].extreme_map_status = FP_StateGateSlotExtremeMapStatus(snapshot, slot);
   snapshot.tf_states[slot].extreme_map_key = FP_StateGateSlotExtremeMapKey(snapshot, slot);
   snapshot.tf_states[slot].extreme_map_notes = "rows=" + IntegerToString(snapshot.tf_states[slot].extreme_candidate_row_count) + "|status=" + snapshot.tf_states[slot].extreme_map_status;

   FP_StateGateExtremeCandidateRow x;
   FP_ResetStateGateExtremeCandidateRow(x);
   if(FP_StateGateFirstExtremeCandidateForSlot(snapshot, slot, x))
   {
      snapshot.tf_states[slot].primary_extreme_source = x.source_kind;
      snapshot.tf_states[slot].primary_extreme_direction = x.direction_label;
      snapshot.tf_states[slot].primary_extreme_side = x.side;
      snapshot.tf_states[slot].primary_extreme_role = x.role;
      snapshot.tf_states[slot].primary_extreme_price_status = x.price_status;
      snapshot.tf_states[slot].primary_extreme_price = x.price;
      snapshot.tf_states[slot].primary_extreme_node_id = x.node_id;
      snapshot.tf_states[slot].primary_extreme_scale_L = x.scale_L;

      snapshot.tf_states[slot].candidate_extreme_status = x.readiness;
      snapshot.tf_states[slot].candidate_extreme_key = x.source_key;
      snapshot.tf_states[slot].candidate_extreme_source = x.source_kind;
      snapshot.tf_states[slot].candidate_direction = x.direction_label;
      snapshot.tf_states[slot].candidate_scale_context = "EXTREME_ROWS=" + IntegerToString(snapshot.tf_states[slot].extreme_candidate_row_count) + "|PRIMARY=" + FP_StateGateKeyPart(x.source_key);
   }

   snapshot.tf_states[slot].entry_bridge_key = FP_StateGateSlotEntryBridgeKey(snapshot, slot);
}

void FP_StateGateFinalizeSnapshotExtremeMaps(FP_StateGateSnapshot &snapshot)
{
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateFinalizeSlotExtremeMap(snapshot, i);
}


void FP_StateGateFinalizeSlotEntryBridge(FP_StateGateSnapshot &snapshot, const int slot)
{
   snapshot.tf_states[slot].entry_bridge_readiness = FP_StateGateSlotEntryBridgeReadiness(snapshot, slot);
   snapshot.tf_states[slot].candidate_extreme_status = FP_StateGateSlotCandidateExtremeStatus(snapshot, slot);
   snapshot.tf_states[slot].candidate_extreme_key = FP_StateGateSlotCandidateExtremeKey(snapshot, slot);
   snapshot.tf_states[slot].candidate_extreme_source = FP_StateGateSlotCandidateExtremeSource(snapshot, slot);
   snapshot.tf_states[slot].candidate_direction = FP_StateGateSlotCandidateDirection(snapshot, slot);
   snapshot.tf_states[slot].candidate_scale_context = FP_StateGateSlotCandidateScaleContext(snapshot, slot);

   snapshot.tf_states[slot].x_invalidation_status = FP_StateGateSlotXInvalidationStatus(snapshot, slot);
   snapshot.tf_states[slot].x_invalidation_key = "X_INVALIDATION_KEY_PENDING_GEOMETRY";
   snapshot.tf_states[slot].x_destination_status = FP_StateGateSlotXDestinationStatus(snapshot, slot);
   snapshot.tf_states[slot].x_destination_key = "X_DESTINATION_KEY_PENDING_GEOMETRY";
   snapshot.tf_states[slot].optionality_status = FP_StateGateSlotOptionalityStatus(snapshot, slot);
   snapshot.tf_states[slot].optionality_key = "OPTIONALITY_KEY_PENDING_X_GEOMETRY";

   snapshot.tf_states[slot].entry_bridge_key = FP_StateGateSlotEntryBridgeKey(snapshot, slot);
}


void FP_StateGateFinalizeSlotContract(FP_StateGateSnapshot &snapshot, const int slot)
{
   snapshot.tf_states[slot].primary_rally_key = FP_StateGateFirstProjectedRallyKey(snapshot, slot);
   snapshot.tf_states[slot].primary_hook_key = FP_StateGateFirstProjectedHookKey(snapshot, slot);
   snapshot.tf_states[slot].anatomy_status = FP_StateGateSlotAnatomyStatus(snapshot, slot);
   snapshot.tf_states[slot].storage_status = FP_StateGateSlotStorageStatus(snapshot.tf_states[slot]);
   snapshot.tf_states[slot].entry_bridge_status = FP_StateGateSlotEntryBridgeStatus(snapshot, slot);
   snapshot.tf_states[slot].contract_status = FP_StateGateSlotContractStatus(snapshot, slot);
   snapshot.tf_states[slot].state_key = FP_StateGateSlotStateKey(snapshot, slot);
   FP_StateGateFinalizeSlotEntryBridge(snapshot, slot);
   FP_StateGateFinalizeSlotExtremeMap(snapshot, slot);
}

void FP_StateGateFinalizeSnapshotContracts(FP_StateGateSnapshot &snapshot)
{
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateFinalizeSlotContract(snapshot, i);
}


// ---------------------------------------------------------------------------
// Phase 13 - Multi-Timeframe Alignment Map
// ---------------------------------------------------------------------------
// This layer compares lower-slot extreme candidate context against higher-slot
// context. Slot order is treated as small-to-large timeframe order by design
// for the Level 19 State Gate configuration.

string FP_StateGateMtfDirectionRelation(const string child_direction,
                                        const string parent_direction)
{
   if(child_direction == "NO_DIRECTION" || parent_direction == "NO_DIRECTION")
      return "MTF_DIRECTION_UNKNOWN";
   if(StringFind(child_direction, "NONE") >= 0 || StringFind(parent_direction, "NONE") >= 0)
      return "MTF_DIRECTION_UNKNOWN";
   if(child_direction == parent_direction)
      return "MTF_DIRECTION_ALIGNED";
   return "MTF_DIRECTION_DIVERGENT";
}

string FP_StateGateMtfSideRelation(const string child_side,
                                   const string parent_side)
{
   if(child_side == "NO_SIDE" || parent_side == "NO_SIDE")
      return "MTF_SIDE_UNKNOWN";
   if(StringFind(child_side, "PENDING") >= 0 || StringFind(parent_side, "PENDING") >= 0)
      return "MTF_SIDE_PENDING";
   if(child_side == parent_side)
      return "MTF_SAME_EXTREME_SIDE";
   return "MTF_OPPOSITE_EXTREME_SIDE";
}

string FP_StateGateMtfContextRole(const string direction_relation,
                                  const string side_relation)
{
   if(direction_relation == "MTF_DIRECTION_ALIGNED" && side_relation == "MTF_SAME_EXTREME_SIDE")
      return "LTF_EXTREME_WITH_HTF_CONTEXT_ALIGNED";
   if(direction_relation == "MTF_DIRECTION_ALIGNED" && side_relation == "MTF_OPPOSITE_EXTREME_SIDE")
      return "LTF_DIRECTION_ALIGNED_HTF_OPPOSITE_SIDE_CONTEXT";
   if(direction_relation == "MTF_DIRECTION_DIVERGENT")
      return "LTF_HTF_DIRECTION_DIVERGENCE_CONTEXT";
   if(side_relation == "MTF_SIDE_PENDING")
      return "MTF_CONTEXT_PENDING_RALLY_SIDE";
   return "MTF_CONTEXT_INCOMPLETE";
}

string FP_StateGateMtfReadiness(const FP_StateGateTimeframeState &child,
                                const FP_StateGateTimeframeState &parent)
{
   if(!child.closed_bar_available)
      return "MTF_ALIGNMENT_BLOCKED_CHILD_NO_CLOSED_BAR";
   if(!parent.closed_bar_available)
      return "MTF_ALIGNMENT_BLOCKED_PARENT_NO_CLOSED_BAR";
   if(child.extreme_candidate_row_count <= 0)
      return "MTF_ALIGNMENT_BLOCKED_CHILD_NO_EXTREME";
   if(parent.extreme_candidate_row_count <= 0)
      return "MTF_ALIGNMENT_BLOCKED_PARENT_NO_EXTREME";
   return "MTF_ALIGNMENT_READY_CONTEXT_ONLY_NO_DECISION";
}

string FP_StateGateMtfAlignmentKey(const FP_StateGateSnapshot &snapshot,
                                   const int child_slot,
                                   const int parent_slot,
                                   const string direction_relation,
                                   const string side_relation,
                                   const string context_role)
{
   string key = snapshot.symbol;
   key += "|CHILD=" + snapshot.tf_states[child_slot].timeframe_label;
   key += "|PARENT=" + snapshot.tf_states[parent_slot].timeframe_label;
   key += "|CDIR=" + FP_StateGateKeyPart(snapshot.tf_states[child_slot].primary_extreme_direction);
   key += "|PDIR=" + FP_StateGateKeyPart(snapshot.tf_states[parent_slot].primary_extreme_direction);
   key += "|CSIDE=" + FP_StateGateKeyPart(snapshot.tf_states[child_slot].primary_extreme_side);
   key += "|PSIDE=" + FP_StateGateKeyPart(snapshot.tf_states[parent_slot].primary_extreme_side);
   key += "|DREL=" + FP_StateGateKeyPart(direction_relation);
   key += "|SREL=" + FP_StateGateKeyPart(side_relation);
   key += "|ROLE=" + FP_StateGateKeyPart(context_role);
   return key;
}

bool FP_StateGateAddMtfAlignmentRow(FP_StateGateSnapshot &snapshot,
                                    const int child_slot,
                                    const int parent_slot)
{
   if(snapshot.mtf_alignment_row_count >= FP_STATE_GATE_MAX_MTF_ALIGNMENT_ROWS)
      return false;
   if(child_slot < 0 || child_slot >= snapshot.timeframe_count)
      return false;
   if(parent_slot < 0 || parent_slot >= snapshot.timeframe_count)
      return false;
   if(child_slot == parent_slot)
      return false;

   FP_StateGateTimeframeState child = snapshot.tf_states[child_slot];
   FP_StateGateTimeframeState parent = snapshot.tf_states[parent_slot];

   int idx = snapshot.mtf_alignment_row_count;
   FP_ResetStateGateMtfAlignmentRow(snapshot.mtf_alignment_rows[idx]);

   string direction_relation = FP_StateGateMtfDirectionRelation(child.primary_extreme_direction, parent.primary_extreme_direction);
   string side_relation = FP_StateGateMtfSideRelation(child.primary_extreme_side, parent.primary_extreme_side);
   string context_role = FP_StateGateMtfContextRole(direction_relation, side_relation);
   string readiness = FP_StateGateMtfReadiness(child, parent);

   snapshot.mtf_alignment_rows[idx].child_slot = child_slot;
   snapshot.mtf_alignment_rows[idx].parent_slot = parent_slot;
   snapshot.mtf_alignment_rows[idx].child_timeframe_label = child.timeframe_label;
   snapshot.mtf_alignment_rows[idx].parent_timeframe_label = parent.timeframe_label;
   snapshot.mtf_alignment_rows[idx].child_closed_bar_time = child.last_closed_bar_time;
   snapshot.mtf_alignment_rows[idx].parent_closed_bar_time = parent.last_closed_bar_time;
   snapshot.mtf_alignment_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.mtf_alignment_rows[idx].readiness = readiness;
   snapshot.mtf_alignment_rows[idx].child_extreme_key = child.extreme_map_key;
   snapshot.mtf_alignment_rows[idx].parent_extreme_key = parent.extreme_map_key;
   snapshot.mtf_alignment_rows[idx].child_source = child.primary_extreme_source;
   snapshot.mtf_alignment_rows[idx].parent_source = parent.primary_extreme_source;
   snapshot.mtf_alignment_rows[idx].child_direction = child.primary_extreme_direction;
   snapshot.mtf_alignment_rows[idx].parent_direction = parent.primary_extreme_direction;
   snapshot.mtf_alignment_rows[idx].child_side = child.primary_extreme_side;
   snapshot.mtf_alignment_rows[idx].parent_side = parent.primary_extreme_side;
   snapshot.mtf_alignment_rows[idx].direction_relation = direction_relation;
   snapshot.mtf_alignment_rows[idx].side_relation = side_relation;
   snapshot.mtf_alignment_rows[idx].context_role = context_role;
   snapshot.mtf_alignment_rows[idx].child_node_id = child.primary_extreme_node_id;
   snapshot.mtf_alignment_rows[idx].parent_node_id = parent.primary_extreme_node_id;
   snapshot.mtf_alignment_rows[idx].child_price = child.primary_extreme_price;
   snapshot.mtf_alignment_rows[idx].parent_price = parent.primary_extreme_price;
   snapshot.mtf_alignment_rows[idx].child_price_status = child.primary_extreme_price_status;
   snapshot.mtf_alignment_rows[idx].parent_price_status = parent.primary_extreme_price_status;
   snapshot.mtf_alignment_rows[idx].alignment_key = FP_StateGateMtfAlignmentKey(snapshot, child_slot, parent_slot, direction_relation, side_relation, context_role);
   snapshot.mtf_alignment_rows[idx].label = child.timeframe_label + " -> " + parent.timeframe_label + " | " + readiness + " | " + direction_relation + " | " + side_relation + " | " + context_role;

   snapshot.mtf_alignment_row_count++;
   snapshot.tf_states[child_slot].mtf_alignment_row_count++;
   snapshot.tf_states[parent_slot].mtf_alignment_row_count++;
   return true;
}

void FP_StateGateBuildMtfAlignmentRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.mtf_alignment_row_count = 0;
   for(int m=0; m<FP_STATE_GATE_MAX_MTF_ALIGNMENT_ROWS; m++)
      FP_ResetStateGateMtfAlignmentRow(snapshot.mtf_alignment_rows[m]);

   for(int i=0; i<snapshot.timeframe_count; i++)
      snapshot.tf_states[i].mtf_alignment_row_count = 0;

   for(int child=0; child<snapshot.timeframe_count; child++)
   {
      for(int parent=child+1; parent<snapshot.timeframe_count; parent++)
         FP_StateGateAddMtfAlignmentRow(snapshot, child, parent);
   }
}

bool FP_StateGateFirstMtfAlignmentForChildSlot(const FP_StateGateSnapshot &snapshot,
                                               const int child_slot,
                                               FP_StateGateMtfAlignmentRow &out)
{
   for(int i=0; i<snapshot.mtf_alignment_row_count; i++)
   {
      FP_StateGateMtfAlignmentRow row = snapshot.mtf_alignment_rows[i];
      if(row.child_slot != child_slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

string FP_StateGateSlotMtfTopStatus(const FP_StateGateSnapshot &snapshot, const int slot)
{
   if(slot == snapshot.timeframe_count - 1)
   {
      if(snapshot.tf_states[slot].extreme_candidate_row_count > 0)
         return "MTF_TOP_CONTEXT_READY_NO_PARENT";
      return "MTF_TOP_CONTEXT_NO_EXTREME";
   }
   return "MTF_ALIGNMENT_PENDING";
}

void FP_StateGateFinalizeSlotMtfAlignment(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateMtfAlignmentRow row;
   FP_ResetStateGateMtfAlignmentRow(row);

   if(FP_StateGateFirstMtfAlignmentForChildSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].mtf_alignment_status = row.readiness;
      snapshot.tf_states[slot].mtf_alignment_key = row.alignment_key;
      snapshot.tf_states[slot].mtf_parent_timeframe = row.parent_timeframe_label;
      snapshot.tf_states[slot].mtf_parent_extreme_key = row.parent_extreme_key;
      snapshot.tf_states[slot].mtf_parent_direction = row.parent_direction;
      snapshot.tf_states[slot].mtf_parent_side = row.parent_side;
      snapshot.tf_states[slot].mtf_direction_relation = row.direction_relation;
      snapshot.tf_states[slot].mtf_side_relation = row.side_relation;
      snapshot.tf_states[slot].mtf_context_role = row.context_role;
      snapshot.tf_states[slot].mtf_alignment_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].mtf_alignment_status = FP_StateGateSlotMtfTopStatus(snapshot, slot);
   snapshot.tf_states[slot].mtf_alignment_key = "NO_PARENT_ALIGNMENT_KEY";
   snapshot.tf_states[slot].mtf_parent_timeframe = "NO_PARENT_TF";
   snapshot.tf_states[slot].mtf_parent_extreme_key = "NO_PARENT_EXTREME";
   snapshot.tf_states[slot].mtf_parent_direction = "NO_PARENT_DIRECTION";
   snapshot.tf_states[slot].mtf_parent_side = "NO_PARENT_SIDE";
   snapshot.tf_states[slot].mtf_direction_relation = "NO_PARENT_DIRECTION_RELATION";
   snapshot.tf_states[slot].mtf_side_relation = "NO_PARENT_SIDE_RELATION";
   snapshot.tf_states[slot].mtf_context_role = "HTF_TOP_LEVEL_CONTEXT";
   snapshot.tf_states[slot].mtf_alignment_notes = snapshot.tf_states[slot].mtf_alignment_status;
}

void FP_StateGateFinalizeSnapshotMtfAlignment(FP_StateGateSnapshot &snapshot)
{
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateFinalizeSlotMtfAlignment(snapshot, i);
}



// ---------------------------------------------------------------------------
// Phase 14 - Entry Geometry Readiness
// ---------------------------------------------------------------------------
// This layer prepares price geometry anchors from the existing Extreme Candidate
// and MTF context. It is still NO_SIGNAL / NO_ORDER. Invalidation remains an
// anchor until a future buffer/stop model is explicitly added.

bool FP_StateGateGeometryPrimaryEntryReady(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available) return false;
   if(s.extreme_candidate_row_count <= 0) return false;
   if(s.primary_extreme_price == 0.0) return false;
   if(StringFind(s.primary_extreme_price_status, "PRICE") < 0) return false;
   return true;
}

string FP_StateGateGeometryEntryStatus(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "ENTRY_PRICE_BLOCKED_NO_CLOSED_BAR";
   if(s.extreme_candidate_row_count <= 0)
      return "ENTRY_PRICE_BLOCKED_NO_EXTREME";
   if(FP_StateGateGeometryPrimaryEntryReady(s))
      return "ENTRY_PRICE_ANCHOR_FROM_PRIMARY_EXTREME_NO_SIGNAL";
   return "ENTRY_PRICE_PENDING_EXTREME_HAS_NO_PRICE";
}

double FP_StateGateGeometryEntryPrice(const FP_StateGateTimeframeState &s)
{
   if(FP_StateGateGeometryPrimaryEntryReady(s))
      return s.primary_extreme_price;
   return 0.0;
}

string FP_StateGateGeometryInvalidationStatus(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "INVALIDATION_PRICE_BLOCKED_NO_CLOSED_BAR";
   if(!FP_StateGateGeometryPrimaryEntryReady(s))
      return "INVALIDATION_PRICE_PENDING_ENTRY_ANCHOR";
   return "INVALIDATION_ANCHOR_FROM_PRIMARY_EXTREME_NEEDS_BUFFER_NO_STOP";
}

double FP_StateGateGeometryInvalidationPrice(const FP_StateGateTimeframeState &s)
{
   if(FP_StateGateGeometryPrimaryEntryReady(s))
      return s.primary_extreme_price;
   return 0.0;
}

bool FP_StateGateGeometryDestinationFromHook(const FP_StateGateSnapshot &snapshot,
                                             const int slot,
                                             double &out_price,
                                             int &out_node_id,
                                             string &out_status)
{
   out_price = 0.0;
   out_node_id = -1;
   out_status = "DESTINATION_PRICE_PENDING_NO_HOOK_CONTEXT";

   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   if(!FP_StateGateGeometryPrimaryEntryReady(s))
   {
      out_status = "DESTINATION_PRICE_PENDING_ENTRY_ANCHOR";
      return false;
   }

   FP_StateGateHookRow h;
   FP_ResetStateGateHookRow(h);
   if(!FP_StateGateFirstProjectedHookRowForSlot(snapshot, slot, h))
   {
      out_status = "DESTINATION_PRICE_PENDING_NO_PROJECTED_HOOK";
      return false;
   }

   if(s.primary_extreme_side == "LOW_EXTREME")
   {
      out_price = h.latest_high_node_price;
      out_node_id = h.latest_high_node_id;
   }
   else if(s.primary_extreme_side == "HIGH_EXTREME")
   {
      out_price = h.latest_low_node_price;
      out_node_id = h.latest_low_node_id;
   }
   else
   {
      out_status = "DESTINATION_PRICE_PENDING_UNKNOWN_EXTREME_SIDE";
      return false;
   }

   if(out_node_id >= 0 && out_price != 0.0)
   {
      out_status = "DESTINATION_ANCHOR_FROM_OPPOSITE_HOOK_NODE_NO_TARGET";
      return true;
   }

   if(out_node_id >= 0)
      out_status = "DESTINATION_NODE_WITHOUT_PRICE_CONTEXT_ONLY";
   else
      out_status = "DESTINATION_PRICE_PENDING_OPPOSITE_NODE";
   return false;
}

string FP_StateGateGeometryRiskDistanceStatus(const FP_StateGateTimeframeState &s)
{
   if(!FP_StateGateGeometryPrimaryEntryReady(s))
      return "RISK_DISTANCE_BLOCKED_NO_ENTRY_ANCHOR";
   return "RISK_DISTANCE_PENDING_INVALIDATION_BUFFER_NO_POSITION";
}

string FP_StateGateGeometryDestinationDistanceStatus(const FP_StateGateTimeframeState &s)
{
   if(!FP_StateGateGeometryPrimaryEntryReady(s))
      return "DESTINATION_DISTANCE_BLOCKED_NO_ENTRY_ANCHOR";
   if(s.candidate_destination_price != 0.0)
      return "DESTINATION_DISTANCE_READY_CONTEXT_ONLY";
   return "DESTINATION_DISTANCE_PENDING_DESTINATION_ANCHOR";
}

string FP_StateGateGeometryPotentialRStatus(const FP_StateGateTimeframeState &s)
{
   if(!FP_StateGateGeometryPrimaryEntryReady(s))
      return "POTENTIAL_R_BLOCKED_NO_ENTRY_ANCHOR";
   if(s.destination_distance <= 0.0)
      return "POTENTIAL_R_PENDING_DESTINATION_DISTANCE";
   return "POTENTIAL_R_PENDING_RISK_BUFFER_NO_SIGNAL";
}

string FP_StateGateGeometryReadiness(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "ENTRY_GEOMETRY_BLOCKED_NO_CLOSED_BAR";
   if(s.extreme_candidate_row_count <= 0)
      return "ENTRY_GEOMETRY_BLOCKED_NO_EXTREME";
   if(s.candidate_entry_price != 0.0 && s.candidate_destination_price != 0.0)
      return "ENTRY_GEOMETRY_PARTIAL_READY_NO_SIGNAL";
   if(s.candidate_entry_price != 0.0)
      return "ENTRY_GEOMETRY_ENTRY_ANCHOR_READY_DESTINATION_PENDING_NO_SIGNAL";
   return "ENTRY_GEOMETRY_PENDING_PRICE_CONTEXT_NO_SIGNAL";
}

string FP_StateGateGeometryKey(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string key = snapshot.symbol;
   key += "|TF=" + s.timeframe_label;
   key += "|GEOM=" + FP_StateGateKeyPart(s.geometry_readiness);
   key += "|ENTRY=" + FP_StateGateKeyPart(s.candidate_entry_price_status);
   key += "|INV=" + FP_StateGateKeyPart(s.candidate_invalidation_price_status);
   key += "|DEST=" + FP_StateGateKeyPart(s.candidate_destination_price_status);
   key += "|RISK=" + FP_StateGateKeyPart(s.risk_distance_status);
   key += "|RR=" + FP_StateGateKeyPart(s.potential_R_status);
   key += "|XMAP=" + FP_StateGateKeyPart(s.extreme_map_key);
   key += "|MTF=" + FP_StateGateKeyPart(s.mtf_alignment_key);
   return key;
}

void FP_StateGateFinalizeSlotEntryGeometry(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];

   double dest_price = 0.0;
   int dest_node_id = -1;
   string dest_status = "DESTINATION_PRICE_PENDING";
   bool has_dest = FP_StateGateGeometryDestinationFromHook(snapshot, slot, dest_price, dest_node_id, dest_status);

   snapshot.tf_states[slot].candidate_entry_price_status = FP_StateGateGeometryEntryStatus(s);
   snapshot.tf_states[slot].candidate_entry_price = FP_StateGateGeometryEntryPrice(s);

   snapshot.tf_states[slot].candidate_invalidation_price_status = FP_StateGateGeometryInvalidationStatus(s);
   snapshot.tf_states[slot].candidate_invalidation_price = FP_StateGateGeometryInvalidationPrice(s);

   snapshot.tf_states[slot].candidate_destination_price_status = dest_status;
   snapshot.tf_states[slot].candidate_destination_price = (has_dest ? dest_price : 0.0);

   snapshot.tf_states[slot].risk_distance_status = FP_StateGateGeometryRiskDistanceStatus(snapshot.tf_states[slot]);
   snapshot.tf_states[slot].risk_distance = 0.0;

   snapshot.tf_states[slot].destination_distance_status = FP_StateGateGeometryDestinationDistanceStatus(snapshot.tf_states[slot]);
   if(snapshot.tf_states[slot].candidate_entry_price != 0.0 && snapshot.tf_states[slot].candidate_destination_price != 0.0)
      snapshot.tf_states[slot].destination_distance = MathAbs(snapshot.tf_states[slot].candidate_destination_price - snapshot.tf_states[slot].candidate_entry_price);
   else
      snapshot.tf_states[slot].destination_distance = 0.0;

   snapshot.tf_states[slot].potential_R_status = FP_StateGateGeometryPotentialRStatus(snapshot.tf_states[slot]);
   snapshot.tf_states[slot].potential_R = 0.0;

   snapshot.tf_states[slot].geometry_readiness = FP_StateGateGeometryReadiness(snapshot.tf_states[slot]);
   snapshot.tf_states[slot].geometry_key = FP_StateGateGeometryKey(snapshot, slot);
   snapshot.tf_states[slot].geometry_notes = "dest_node=" + IntegerToString(dest_node_id) + "|risk_buffer_required=true|no_signal=true|no_order=true";

   if(snapshot.tf_states[slot].candidate_invalidation_price != 0.0)
   {
      snapshot.tf_states[slot].x_invalidation_status = "X_INVALIDATION_ANCHOR_READY_NEEDS_BUFFER_NO_STOP";
      snapshot.tf_states[slot].x_invalidation_key = "XINV|TF=" + snapshot.tf_states[slot].timeframe_label + "|PRICE=" + DoubleToString(snapshot.tf_states[slot].candidate_invalidation_price, 8);
   }

   if(snapshot.tf_states[slot].candidate_destination_price != 0.0)
   {
      snapshot.tf_states[slot].x_destination_status = "X_DESTINATION_ANCHOR_READY_NO_TARGET_ORDER";
      snapshot.tf_states[slot].x_destination_key = "XDEST|TF=" + snapshot.tf_states[slot].timeframe_label + "|PRICE=" + DoubleToString(snapshot.tf_states[slot].candidate_destination_price, 8);
   }

   snapshot.tf_states[slot].optionality_status = snapshot.tf_states[slot].potential_R_status;
   snapshot.tf_states[slot].optionality_key = "OPT|TF=" + snapshot.tf_states[slot].timeframe_label + "|DEST_DIST=" + DoubleToString(snapshot.tf_states[slot].destination_distance, 8) + "|RISK_STATUS=" + FP_StateGateKeyPart(snapshot.tf_states[slot].risk_distance_status);

   snapshot.tf_states[slot].entry_bridge_key = FP_StateGateSlotEntryBridgeKey(snapshot, slot);
}

void FP_StateGateFinalizeSnapshotEntryGeometry(FP_StateGateSnapshot &snapshot)
{
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateFinalizeSlotEntryGeometry(snapshot, i);
}



// ---------------------------------------------------------------------------
// Phase 15 - Entry Idea Layer
// ---------------------------------------------------------------------------
// This layer wraps the prepared geometry into idea-only records.  It still
// never produces trade permission, orders, position sizing, or execution fields.

string FP_StateGateEntryIdeaFamily(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "ENTRY_IDEA_BLOCKED_NO_CLOSED_BAR";
   if(s.candidate_entry_price == 0.0)
      return "ENTRY_IDEA_BLOCKED_NO_ENTRY_GEOMETRY";
   if(StringFind(s.primary_extreme_source, "HOOK") >= 0 && StringFind(s.mtf_context_role, "ALIGNED") >= 0)
      return "MTF_ALIGNED_HOOK_EXTREME_IDEA_ONLY";
   if(StringFind(s.primary_extreme_source, "HOOK") >= 0)
      return "HOOK_EXTREME_REVERSAL_IDEA_ONLY";
   if(StringFind(s.primary_extreme_source, "RALLY") >= 0)
      return "RALLY_CONTEXT_EXTREME_IDEA_ONLY";
   if(StringFind(s.geometry_readiness, "PARTIAL") >= 0)
      return "GEOMETRY_CONTEXT_IDEA_ONLY";
   return "ENTRY_IDEA_PENDING_CONTEXT_ONLY";
}

string FP_StateGateEntryIdeaType(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "NO_ENTRY_IDEA_TYPE";
   if(s.candidate_entry_price == 0.0)
      return "WAIT_FOR_ENTRY_GEOMETRY_IDEA_ONLY";
   if(StringFind(s.primary_extreme_source, "HOOK") >= 0)
      return "SELECTED_EXTREME_REVERSION_CONTEXT_IDEA_ONLY";
   if(StringFind(s.primary_extreme_source, "RALLY") >= 0)
      return "RALLY_STAGE_CONTEXT_IDEA_ONLY";
   return "GEOMETRY_CONTEXT_IDEA_ONLY";
}

string FP_StateGateEntryIdeaReadiness(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "ENTRY_IDEA_BLOCKED_NO_CLOSED_BAR";
   if(s.candidate_entry_price == 0.0)
      return "ENTRY_IDEA_BLOCKED_NO_ENTRY_ANCHOR";
   if(s.candidate_destination_price != 0.0)
      return "ENTRY_IDEA_READY_FOR_DRY_RUN_NO_SIGNAL_NO_ORDER";
   return "ENTRY_IDEA_PARTIAL_DESTINATION_PENDING_NO_SIGNAL_NO_ORDER";
}

string FP_StateGateEntryIdeaStatus(const FP_StateGateTimeframeState &s)
{
   string readiness = FP_StateGateEntryIdeaReadiness(s);
   if(StringFind(readiness, "READY") >= 0)
      return "ENTRY_IDEA_CONTEXT_READY_NO_SIGNAL";
   if(StringFind(readiness, "PARTIAL") >= 0)
      return "ENTRY_IDEA_CONTEXT_PARTIAL_NO_SIGNAL";
   return "ENTRY_IDEA_CONTEXT_BLOCKED_NO_SIGNAL";
}

string FP_StateGateEntryIdeaRole(const FP_StateGateTimeframeState &s)
{
   if(StringFind(s.mtf_context_role, "ALIGNED") >= 0)
      return "IDEA_ROLE_LTF_EXTREME_WITH_HTF_CONTEXT";
   if(StringFind(s.mtf_context_role, "DIVERGENCE") >= 0)
      return "IDEA_ROLE_LTF_HTF_DIVERGENCE_REVIEW";
   if(StringFind(s.primary_extreme_source, "HOOK") >= 0)
      return "IDEA_ROLE_HOOK_EXTREME_REVIEW";
   if(StringFind(s.primary_extreme_source, "RALLY") >= 0)
      return "IDEA_ROLE_RALLY_STAGE_REVIEW";
   return "IDEA_ROLE_CONTEXT_REVIEW";
}

string FP_StateGateEntryIdeaKey(const FP_StateGateSnapshot &snapshot,
                                const int slot,
                                const string idea_family,
                                const string idea_type,
                                const string readiness)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string key = snapshot.symbol;
   key += "|TF=" + s.timeframe_label;
   key += "|IDEA=" + FP_StateGateKeyPart(idea_family);
   key += "|TYPE=" + FP_StateGateKeyPart(idea_type);
   key += "|READY=" + FP_StateGateKeyPart(readiness);
   key += "|DIR=" + FP_StateGateKeyPart(s.primary_extreme_direction);
   key += "|SIDE=" + FP_StateGateKeyPart(s.primary_extreme_side);
   key += "|GEOM=" + FP_StateGateKeyPart(s.geometry_key);
   key += "|MTF=" + FP_StateGateKeyPart(s.mtf_alignment_key);
   return key;
}

bool FP_StateGateAddEntryIdeaRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.entry_idea_row_count >= FP_STATE_GATE_MAX_ENTRY_IDEA_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   int idx = snapshot.entry_idea_row_count;
   FP_ResetStateGateEntryIdeaRow(snapshot.entry_idea_rows[idx]);

   string family = FP_StateGateEntryIdeaFamily(s);
   string idea_type = FP_StateGateEntryIdeaType(s);
   string readiness = FP_StateGateEntryIdeaReadiness(s);
   string status = FP_StateGateEntryIdeaStatus(s);
   string role = FP_StateGateEntryIdeaRole(s);
   string idea_key = FP_StateGateEntryIdeaKey(snapshot, slot, family, idea_type, readiness);

   snapshot.entry_idea_rows[idx].slot_index = slot;
   snapshot.entry_idea_rows[idx].timeframe = s.timeframe;
   snapshot.entry_idea_rows[idx].timeframe_label = s.timeframe_label;
   snapshot.entry_idea_rows[idx].last_closed_bar_time = s.last_closed_bar_time;
   snapshot.entry_idea_rows[idx].last_closed_bar_close = s.last_closed_bar_close;
   snapshot.entry_idea_rows[idx].status = (StringFind(status, "BLOCKED") >= 0 ? FP_STATE_GATE_ROW_PLACEHOLDER : FP_STATE_GATE_ROW_PROJECTED);
   snapshot.entry_idea_rows[idx].readiness = readiness;
   snapshot.entry_idea_rows[idx].idea_family = family;
   snapshot.entry_idea_rows[idx].idea_type = idea_type;
   snapshot.entry_idea_rows[idx].idea_direction = s.primary_extreme_direction;
   snapshot.entry_idea_rows[idx].idea_source = s.primary_extreme_source;
   snapshot.entry_idea_rows[idx].idea_role = role;
   snapshot.entry_idea_rows[idx].geometry_status = s.geometry_readiness;
   snapshot.entry_idea_rows[idx].mtf_context_role = s.mtf_context_role;
   snapshot.entry_idea_rows[idx].extreme_side = s.primary_extreme_side;
   snapshot.entry_idea_rows[idx].entry_price = s.candidate_entry_price;
   snapshot.entry_idea_rows[idx].invalidation_anchor_price = s.candidate_invalidation_price;
   snapshot.entry_idea_rows[idx].destination_anchor_price = s.candidate_destination_price;
   snapshot.entry_idea_rows[idx].destination_distance = s.destination_distance;
   snapshot.entry_idea_rows[idx].risk_status = s.risk_distance_status;
   snapshot.entry_idea_rows[idx].potential_R_status = s.potential_R_status;
   snapshot.entry_idea_rows[idx].potential_R = s.potential_R;
   snapshot.entry_idea_rows[idx].idea_key = idea_key;
   snapshot.entry_idea_rows[idx].label = s.timeframe_label + " | " + family + " | " + readiness + " | " + s.primary_extreme_direction + " | " + s.primary_extreme_side + " | " + s.geometry_readiness + " | " + s.mtf_context_role;

   snapshot.entry_idea_row_count++;
   snapshot.tf_states[slot].entry_idea_row_count++;
   return true;
}

void FP_StateGateBuildEntryIdeaRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.entry_idea_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_ENTRY_IDEA_ROWS; i++)
      FP_ResetStateGateEntryIdeaRow(snapshot.entry_idea_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].entry_idea_row_count = 0;
      FP_StateGateAddEntryIdeaRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstEntryIdeaForSlot(const FP_StateGateSnapshot &snapshot,
                                       const int slot,
                                       FP_StateGateEntryIdeaRow &out)
{
   for(int i=0; i<snapshot.entry_idea_row_count; i++)
   {
      FP_StateGateEntryIdeaRow row = snapshot.entry_idea_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotEntryIdea(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateEntryIdeaRow idea;
   FP_ResetStateGateEntryIdeaRow(idea);

   if(FP_StateGateFirstEntryIdeaForSlot(snapshot, slot, idea))
   {
      snapshot.tf_states[slot].entry_idea_status = FP_StateGateEntryIdeaStatus(snapshot.tf_states[slot]);
      snapshot.tf_states[slot].entry_idea_readiness = idea.readiness;
      snapshot.tf_states[slot].entry_idea_key = idea.idea_key;
      snapshot.tf_states[slot].primary_entry_idea_family = idea.idea_family;
      snapshot.tf_states[slot].primary_entry_idea_type = idea.idea_type;
      snapshot.tf_states[slot].primary_entry_idea_direction = idea.idea_direction;
      snapshot.tf_states[slot].primary_entry_idea_source = idea.idea_source;
      snapshot.tf_states[slot].primary_entry_idea_role = idea.idea_role;
      snapshot.tf_states[slot].primary_entry_idea_geometry_status = idea.geometry_status;
      snapshot.tf_states[slot].primary_entry_idea_mtf_context = idea.mtf_context_role;
      snapshot.tf_states[slot].entry_idea_notes = idea.label;
      return;
   }

   snapshot.tf_states[slot].entry_idea_status = "ENTRY_IDEA_NO_ROW_NO_SIGNAL";
   snapshot.tf_states[slot].entry_idea_readiness = "ENTRY_IDEA_NO_ROW_NO_SIGNAL";
   snapshot.tf_states[slot].entry_idea_key = "NO_ENTRY_IDEA_KEY";
   snapshot.tf_states[slot].entry_idea_notes = "No entry idea row was built";
}

void FP_StateGateFinalizeSnapshotEntryIdeas(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotEntryIdea(snapshot, slot);
}



// ---------------------------------------------------------------------------
// Phase 16 - Entry Decision Layer / Dry Run
// ---------------------------------------------------------------------------
// This layer converts entry ideas into non-executable dry-run decision rows.
// It never allows real execution.  decision_allowed is always false here.

string FP_StateGateEntryDecisionDirection(const FP_StateGateTimeframeState &s)
{
   if(StringFind(s.primary_entry_idea_direction, "BULLISH") >= 0)
      return "BUY_DRY_RUN_ONLY";
   if(StringFind(s.primary_entry_idea_direction, "BEARISH") >= 0)
      return "SELL_DRY_RUN_ONLY";
   if(StringFind(s.primary_extreme_direction, "BULLISH") >= 0)
      return "BUY_DRY_RUN_ONLY";
   if(StringFind(s.primary_extreme_direction, "BEARISH") >= 0)
      return "SELL_DRY_RUN_ONLY";
   return "NO_ENTRY_DECISION_DIRECTION";
}

string FP_StateGateEntryDecisionType(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "NO_ENTRY_DECISION_TYPE";
   if(s.candidate_entry_price == 0.0)
      return "WAIT_FOR_ENTRY_ANCHOR_DRY_RUN";
   if(StringFind(s.primary_entry_idea_family, "HOOK") >= 0)
      return "LIMIT_AT_SELECTED_HOOK_EXTREME_DRY_RUN_ONLY";
   if(StringFind(s.primary_entry_idea_family, "RALLY") >= 0)
      return "LIMIT_AT_RALLY_CONTEXT_EXTREME_DRY_RUN_ONLY";
   return "LIMIT_AT_GEOMETRY_ANCHOR_DRY_RUN_ONLY";
}

string FP_StateGateEntryDecisionReadiness(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "ENTRY_DECISION_BLOCKED_NO_CLOSED_BAR";
   if(s.entry_idea_row_count <= 0)
      return "ENTRY_DECISION_BLOCKED_NO_ENTRY_IDEA";
   if(s.candidate_entry_price == 0.0)
      return "ENTRY_DECISION_BLOCKED_NO_ENTRY_PRICE";
   if(s.candidate_destination_price == 0.0)
      return "ENTRY_DECISION_PARTIAL_DESTINATION_PENDING_DRY_RUN_ONLY";
   return "ENTRY_DECISION_READY_DRY_RUN_NO_ORDER";
}

string FP_StateGateEntryDecisionStatus(const FP_StateGateTimeframeState &s)
{
   string readiness = FP_StateGateEntryDecisionReadiness(s);
   if(StringFind(readiness, "READY") >= 0)
      return "ENTRY_DECISION_CONTEXT_READY_DRY_RUN_ONLY";
   if(StringFind(readiness, "PARTIAL") >= 0)
      return "ENTRY_DECISION_CONTEXT_PARTIAL_DRY_RUN_ONLY";
   return "ENTRY_DECISION_CONTEXT_BLOCKED_DRY_RUN_ONLY";
}

string FP_StateGateEntryDecisionPriceStatus(const FP_StateGateTimeframeState &s)
{
   if(s.candidate_entry_price != 0.0)
      return "ENTRY_DECISION_PRICE_FROM_GEOMETRY_ANCHOR_DRY_RUN_ONLY";
   return "ENTRY_DECISION_PRICE_UNAVAILABLE_DRY_RUN_ONLY";
}

string FP_StateGateEntryDecisionBlockReason(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return "BLOCKED_NO_CLOSED_BAR";
   if(s.entry_idea_row_count <= 0)
      return "BLOCKED_NO_ENTRY_IDEA_ROW";
   if(s.candidate_entry_price == 0.0)
      return "BLOCKED_NO_ENTRY_ANCHOR_PRICE";
   if(s.candidate_destination_price == 0.0)
      return "PARTIAL_DESTINATION_ANCHOR_PENDING";
   return "NOT_BLOCKED_BUT_EXECUTION_DISABLED_DRY_RUN_ONLY";
}

string FP_StateGateEntryDecisionKey(const FP_StateGateSnapshot &snapshot,
                                    const int slot,
                                    const string readiness,
                                    const string decision_type,
                                    const string decision_direction)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string key = snapshot.symbol;
   key += "|TF=" + s.timeframe_label;
   key += "|DECISION=" + FP_StateGateKeyPart(readiness);
   key += "|TYPE=" + FP_StateGateKeyPart(decision_type);
   key += "|DIR=" + FP_StateGateKeyPart(decision_direction);
   key += "|IDEA=" + FP_StateGateKeyPart(s.entry_idea_key);
   key += "|GEOM=" + FP_StateGateKeyPart(s.geometry_key);
   key += "|MTF=" + FP_StateGateKeyPart(s.mtf_alignment_key);
   key += "|ALLOWED=false";
   return key;
}

bool FP_StateGateAddEntryDecisionRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.entry_decision_row_count >= FP_STATE_GATE_MAX_ENTRY_DECISION_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   int idx = snapshot.entry_decision_row_count;
   FP_ResetStateGateEntryDecisionRow(snapshot.entry_decision_rows[idx]);

   string direction = FP_StateGateEntryDecisionDirection(s);
   string decision_type = FP_StateGateEntryDecisionType(s);
   string readiness = FP_StateGateEntryDecisionReadiness(s);
   string decision_status = FP_StateGateEntryDecisionStatus(s);
   string price_status = FP_StateGateEntryDecisionPriceStatus(s);
   string block_reason = FP_StateGateEntryDecisionBlockReason(s);
   string decision_key = FP_StateGateEntryDecisionKey(snapshot, slot, readiness, decision_type, direction);

   snapshot.entry_decision_rows[idx].slot_index = slot;
   snapshot.entry_decision_rows[idx].timeframe = s.timeframe;
   snapshot.entry_decision_rows[idx].timeframe_label = s.timeframe_label;
   snapshot.entry_decision_rows[idx].last_closed_bar_time = s.last_closed_bar_time;
   snapshot.entry_decision_rows[idx].last_closed_bar_close = s.last_closed_bar_close;
   snapshot.entry_decision_rows[idx].status = (StringFind(decision_status, "BLOCKED") >= 0 ? FP_STATE_GATE_ROW_PLACEHOLDER : FP_STATE_GATE_ROW_PROJECTED);
   snapshot.entry_decision_rows[idx].readiness = readiness;
   snapshot.entry_decision_rows[idx].decision_status = decision_status;
   snapshot.entry_decision_rows[idx].decision_direction = direction;
   snapshot.entry_decision_rows[idx].decision_type = decision_type;
   snapshot.entry_decision_rows[idx].decision_mode = "DRY_RUN_ONLY_NON_EXECUTABLE";
   snapshot.entry_decision_rows[idx].decision_allowed = false;
   snapshot.entry_decision_rows[idx].decision_price_status = price_status;
   snapshot.entry_decision_rows[idx].decision_price = s.candidate_entry_price;
   snapshot.entry_decision_rows[idx].invalidation_status = s.candidate_invalidation_price_status;
   snapshot.entry_decision_rows[idx].invalidation_price = s.candidate_invalidation_price;
   snapshot.entry_decision_rows[idx].destination_status = s.candidate_destination_price_status;
   snapshot.entry_decision_rows[idx].destination_price = s.candidate_destination_price;
   snapshot.entry_decision_rows[idx].risk_status = s.risk_distance_status;
   snapshot.entry_decision_rows[idx].potential_R_status = s.potential_R_status;
   snapshot.entry_decision_rows[idx].source_idea_key = s.entry_idea_key;
   snapshot.entry_decision_rows[idx].source_geometry_key = s.geometry_key;
   snapshot.entry_decision_rows[idx].source_mtf_key = s.mtf_alignment_key;
   snapshot.entry_decision_rows[idx].block_reason = block_reason;
   snapshot.entry_decision_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE16_DRY_RUN_ONLY";
   snapshot.entry_decision_rows[idx].decision_key = decision_key;
   snapshot.entry_decision_rows[idx].label = s.timeframe_label + " | " + decision_status + " | " + decision_type + " | " + direction + " | allowed=false | " + block_reason;

   snapshot.entry_decision_row_count++;
   snapshot.tf_states[slot].entry_decision_row_count++;
   return true;
}

void FP_StateGateBuildEntryDecisionRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.entry_decision_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_ENTRY_DECISION_ROWS; i++)
      FP_ResetStateGateEntryDecisionRow(snapshot.entry_decision_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].entry_decision_row_count = 0;
      FP_StateGateAddEntryDecisionRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstEntryDecisionForSlot(const FP_StateGateSnapshot &snapshot,
                                           const int slot,
                                           FP_StateGateEntryDecisionRow &out)
{
   for(int i=0; i<snapshot.entry_decision_row_count; i++)
   {
      FP_StateGateEntryDecisionRow row = snapshot.entry_decision_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotEntryDecision(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateEntryDecisionRow row;
   FP_ResetStateGateEntryDecisionRow(row);

   if(FP_StateGateFirstEntryDecisionForSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].entry_decision_status = row.decision_status;
      snapshot.tf_states[slot].entry_decision_readiness = row.readiness;
      snapshot.tf_states[slot].entry_decision_key = row.decision_key;
      snapshot.tf_states[slot].entry_decision_direction = row.decision_direction;
      snapshot.tf_states[slot].entry_decision_type = row.decision_type;
      snapshot.tf_states[slot].entry_decision_mode = row.decision_mode;
      snapshot.tf_states[slot].entry_decision_allowed = false;
      snapshot.tf_states[slot].entry_decision_price_status = row.decision_price_status;
      snapshot.tf_states[slot].entry_decision_price = row.decision_price;
      snapshot.tf_states[slot].entry_decision_invalidation_status = row.invalidation_status;
      snapshot.tf_states[slot].entry_decision_invalidation_price = row.invalidation_price;
      snapshot.tf_states[slot].entry_decision_destination_status = row.destination_status;
      snapshot.tf_states[slot].entry_decision_destination_price = row.destination_price;
      snapshot.tf_states[slot].entry_decision_risk_status = row.risk_status;
      snapshot.tf_states[slot].entry_decision_potential_R_status = row.potential_R_status;
      snapshot.tf_states[slot].entry_decision_block_reason = row.block_reason;
      snapshot.tf_states[slot].entry_decision_execution_status = row.execution_status;
      snapshot.tf_states[slot].entry_decision_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].entry_decision_status = "ENTRY_DECISION_NO_ROW_DRY_RUN_ONLY";
   snapshot.tf_states[slot].entry_decision_readiness = "ENTRY_DECISION_NO_ROW_NO_SIGNAL";
   snapshot.tf_states[slot].entry_decision_allowed = false;
   snapshot.tf_states[slot].entry_decision_execution_status = "REAL_EXECUTION_DISABLED_PHASE16_DRY_RUN_ONLY";
   snapshot.tf_states[slot].entry_decision_notes = "No entry decision row was built";
}

void FP_StateGateFinalizeSnapshotEntryDecisions(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotEntryDecision(snapshot, slot);
}



// ---------------------------------------------------------------------------
// Phase 17 - Paper Execution / Dry Run Ledger
// ---------------------------------------------------------------------------
// This layer records dry-run entry decisions into a paper ledger snapshot.
// It is still non-executable.  Real order placement remains disabled.

string FP_StateGatePaperLedgerEventId(const FP_StateGateSnapshot &snapshot,
                                      const int slot,
                                      const FP_StateGateEntryDecisionRow &d)
{
   string id = "PAPER";
   id += "|" + snapshot.symbol;
   id += "|TF=" + snapshot.tf_states[slot].timeframe_label;
   id += "|T=" + FP_StateGateKeyPart(FP_StateGateClosedBarTimeLabel(snapshot.tf_states[slot].last_closed_bar_time));
   id += "|DIR=" + FP_StateGateKeyPart(d.decision_direction);
   id += "|TYPE=" + FP_StateGateKeyPart(d.decision_type);
   id += "|PX=" + DoubleToString(d.decision_price, 8);
   return id;
}

string FP_StateGatePaperLedgerRecordStatus(const FP_StateGateTimeframeState &s,
                                           const FP_StateGateEntryDecisionRow &d)
{
   if(!s.closed_bar_available)
      return "PAPER_LEDGER_BLOCKED_NO_CLOSED_BAR";
   if(d.decision_key == "NO_ENTRY_DECISION_KEY" || d.decision_key == "")
      return "PAPER_LEDGER_BLOCKED_NO_DECISION";
   if(d.decision_price == 0.0)
      return "PAPER_LEDGER_BLOCKED_NO_DECISION_PRICE";
   return "PAPER_LEDGER_RECORDED_DRY_RUN_ONLY";
}

string FP_StateGatePaperLedgerLifecycleStatus(const FP_StateGateEntryDecisionRow &d)
{
   if(d.decision_price == 0.0)
      return "PAPER_LIFECYCLE_NOT_OPEN_NO_ENTRY_PRICE";
   if(d.destination_price != 0.0)
      return "PAPER_LIFECYCLE_HYPOTHETICAL_OPEN_WITH_DESTINATION_ANCHOR";
   return "PAPER_LIFECYCLE_HYPOTHETICAL_OPEN_DESTINATION_PENDING";
}

string FP_StateGatePaperLedgerKey(const FP_StateGateSnapshot &snapshot,
                                  const int slot,
                                  const FP_StateGateEntryDecisionRow &d,
                                  const string record_status,
                                  const string event_id)
{
   string key = snapshot.symbol;
   key += "|TF=" + snapshot.tf_states[slot].timeframe_label;
   key += "|REC=" + FP_StateGateKeyPart(record_status);
   key += "|EVENT=" + FP_StateGateKeyPart(event_id);
   key += "|DEC=" + FP_StateGateKeyPart(d.decision_key);
   key += "|EXEC=DISABLED";
   return key;
}

bool FP_StateGateFirstEntryDecisionForLedgerSlot(const FP_StateGateSnapshot &snapshot,
                                                 const int slot,
                                                 FP_StateGateEntryDecisionRow &out)
{
   for(int i=0; i<snapshot.entry_decision_row_count; i++)
   {
      FP_StateGateEntryDecisionRow row = snapshot.entry_decision_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateAddPaperLedgerRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.paper_ledger_row_count >= FP_STATE_GATE_MAX_PAPER_LEDGER_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGateEntryDecisionRow d;
   FP_ResetStateGateEntryDecisionRow(d);
   if(!FP_StateGateFirstEntryDecisionForLedgerSlot(snapshot, slot, d))
      return false;

   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   int idx = snapshot.paper_ledger_row_count;
   FP_ResetStateGatePaperLedgerRow(snapshot.paper_ledger_rows[idx]);

   string event_id = FP_StateGatePaperLedgerEventId(snapshot, slot, d);
   string record_status = FP_StateGatePaperLedgerRecordStatus(s, d);
   string lifecycle = FP_StateGatePaperLedgerLifecycleStatus(d);
   string ledger_key = FP_StateGatePaperLedgerKey(snapshot, slot, d, record_status, event_id);

   snapshot.paper_ledger_rows[idx].slot_index = slot;
   snapshot.paper_ledger_rows[idx].timeframe = s.timeframe;
   snapshot.paper_ledger_rows[idx].timeframe_label = s.timeframe_label;
   snapshot.paper_ledger_rows[idx].recorded_at = TimeCurrent();
   snapshot.paper_ledger_rows[idx].last_closed_bar_time = s.last_closed_bar_time;
   snapshot.paper_ledger_rows[idx].last_closed_bar_close = s.last_closed_bar_close;
   snapshot.paper_ledger_rows[idx].status = (StringFind(record_status, "RECORDED") >= 0 ? FP_STATE_GATE_ROW_PROJECTED : FP_STATE_GATE_ROW_PLACEHOLDER);
   snapshot.paper_ledger_rows[idx].record_status = record_status;
   snapshot.paper_ledger_rows[idx].ledger_mode = "PAPER_DRY_RUN_ONLY";
   snapshot.paper_ledger_rows[idx].lifecycle_status = lifecycle;
   snapshot.paper_ledger_rows[idx].decision_status = d.decision_status;
   snapshot.paper_ledger_rows[idx].decision_readiness = d.readiness;
   snapshot.paper_ledger_rows[idx].decision_direction = d.decision_direction;
   snapshot.paper_ledger_rows[idx].decision_type = d.decision_type;
   snapshot.paper_ledger_rows[idx].decision_allowed = false;
   snapshot.paper_ledger_rows[idx].entry_price = d.decision_price;
   snapshot.paper_ledger_rows[idx].invalidation_price = d.invalidation_price;
   snapshot.paper_ledger_rows[idx].destination_price = d.destination_price;
   snapshot.paper_ledger_rows[idx].risk_status = d.risk_status;
   snapshot.paper_ledger_rows[idx].potential_R_status = d.potential_R_status;
   snapshot.paper_ledger_rows[idx].source_decision_key = d.decision_key;
   snapshot.paper_ledger_rows[idx].source_idea_key = d.source_idea_key;
   snapshot.paper_ledger_rows[idx].source_geometry_key = d.source_geometry_key;
   snapshot.paper_ledger_rows[idx].source_mtf_key = d.source_mtf_key;
   snapshot.paper_ledger_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE17_PAPER_ONLY";
   snapshot.paper_ledger_rows[idx].block_reason = d.block_reason;
   snapshot.paper_ledger_rows[idx].ledger_key = ledger_key;
   snapshot.paper_ledger_rows[idx].event_id = event_id;
   snapshot.paper_ledger_rows[idx].label = s.timeframe_label + " | PAPER LEDGER | " + record_status + " | " + d.decision_direction + " | " + d.decision_type + " | real_execution=false";

   snapshot.paper_ledger_row_count++;
   snapshot.tf_states[slot].paper_ledger_row_count++;
   return true;
}

void FP_StateGateBuildPaperLedgerRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.paper_ledger_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_PAPER_LEDGER_ROWS; i++)
      FP_ResetStateGatePaperLedgerRow(snapshot.paper_ledger_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].paper_ledger_row_count = 0;
      FP_StateGateAddPaperLedgerRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstPaperLedgerForSlot(const FP_StateGateSnapshot &snapshot,
                                         const int slot,
                                         FP_StateGatePaperLedgerRow &out)
{
   for(int i=0; i<snapshot.paper_ledger_row_count; i++)
   {
      FP_StateGatePaperLedgerRow row = snapshot.paper_ledger_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotPaperLedger(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGatePaperLedgerRow row;
   FP_ResetStateGatePaperLedgerRow(row);

   if(FP_StateGateFirstPaperLedgerForSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].paper_ledger_status = "PAPER_LEDGER_CONTEXT_AVAILABLE_NO_REAL_EXECUTION";
      snapshot.tf_states[slot].paper_ledger_record_status = row.record_status;
      snapshot.tf_states[slot].paper_ledger_key = row.ledger_key;
      snapshot.tf_states[slot].paper_ledger_event_id = row.event_id;
      snapshot.tf_states[slot].paper_ledger_mode = row.ledger_mode;
      snapshot.tf_states[slot].paper_ledger_direction = row.decision_direction;
      snapshot.tf_states[slot].paper_ledger_type = row.decision_type;
      snapshot.tf_states[slot].paper_ledger_entry_price = row.entry_price;
      snapshot.tf_states[slot].paper_ledger_invalidation_price = row.invalidation_price;
      snapshot.tf_states[slot].paper_ledger_destination_price = row.destination_price;
      snapshot.tf_states[slot].paper_ledger_lifecycle_status = row.lifecycle_status;
      snapshot.tf_states[slot].paper_ledger_execution_status = row.execution_status;
      snapshot.tf_states[slot].paper_ledger_source_decision_key = row.source_decision_key;
      snapshot.tf_states[slot].paper_ledger_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].paper_ledger_status = "PAPER_LEDGER_NO_ROW_NO_REAL_EXECUTION";
   snapshot.tf_states[slot].paper_ledger_record_status = "PAPER_LEDGER_NO_ROW";
   snapshot.tf_states[slot].paper_ledger_key = "NO_PAPER_LEDGER_KEY";
   snapshot.tf_states[slot].paper_ledger_execution_status = "REAL_EXECUTION_DISABLED_PHASE17_PAPER_ONLY";
   snapshot.tf_states[slot].paper_ledger_notes = "No paper ledger row was built";
}

void FP_StateGateFinalizeSnapshotPaperLedger(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotPaperLedger(snapshot, slot);
}



// ---------------------------------------------------------------------------
// Phase 18 - Paper Ledger Lifecycle Tracking
// ---------------------------------------------------------------------------
// This layer evaluates paper ledger anchors against the latest closed candle
// close only.  It remains non-executable and does not manage broker orders.

bool FP_StateGatePaperIsBuyDirection(const string direction)
{
   return (StringFind(direction, "BUY") >= 0 || StringFind(direction, "BULLISH") >= 0);
}

bool FP_StateGatePaperIsSellDirection(const string direction)
{
   return (StringFind(direction, "SELL") >= 0 || StringFind(direction, "BEARISH") >= 0);
}

bool FP_StateGatePaperTouchByClose(const string direction,
                                   const double close_price,
                                   const double anchor_price,
                                   const bool is_destination)
{
   if(anchor_price == 0.0 || close_price == 0.0)
      return false;

   if(FP_StateGatePaperIsBuyDirection(direction))
   {
      if(is_destination)
         return (close_price >= anchor_price);
      return (close_price <= anchor_price);
   }

   if(FP_StateGatePaperIsSellDirection(direction))
   {
      if(is_destination)
         return (close_price <= anchor_price);
      return (close_price >= anchor_price);
   }

   return false;
}

string FP_StateGatePaperEntryTouchStatus(const FP_StateGatePaperLedgerRow &p)
{
   if(p.entry_price == 0.0)
      return "PAPER_ENTRY_TOUCH_BLOCKED_NO_ENTRY_PRICE";
   if(FP_StateGatePaperTouchByClose(p.decision_direction, p.last_closed_bar_close, p.entry_price, false))
      return "PAPER_ENTRY_ANCHOR_TOUCHED_BY_CLOSED_CLOSE_ONLY";
   return "PAPER_ENTRY_ANCHOR_NOT_TOUCHED_BY_CLOSED_CLOSE_ONLY";
}

string FP_StateGatePaperInvalidationTouchStatus(const FP_StateGatePaperLedgerRow &p)
{
   if(p.invalidation_price == 0.0)
      return "PAPER_INVALIDATION_TOUCH_PENDING_NO_INVALIDATION_ANCHOR";
   if(FP_StateGatePaperTouchByClose(p.decision_direction, p.last_closed_bar_close, p.invalidation_price, false))
      return "PAPER_INVALIDATION_ANCHOR_TOUCHED_NO_STOP_NO_ORDER";
   return "PAPER_INVALIDATION_ANCHOR_NOT_TOUCHED";
}

string FP_StateGatePaperDestinationTouchStatus(const FP_StateGatePaperLedgerRow &p)
{
   if(p.destination_price == 0.0)
      return "PAPER_DESTINATION_TOUCH_PENDING_NO_DESTINATION_ANCHOR";
   if(FP_StateGatePaperTouchByClose(p.decision_direction, p.last_closed_bar_close, p.destination_price, true))
      return "PAPER_DESTINATION_ANCHOR_TOUCHED_NO_TARGET_NO_ORDER";
   return "PAPER_DESTINATION_ANCHOR_NOT_TOUCHED";
}

string FP_StateGatePaperLifecyclePathState(const bool entry_touched,
                                           const bool invalidation_touched,
                                           const bool destination_touched)
{
   if(!entry_touched)
      return "PAPER_PATH_WAITING_FOR_ENTRY_ANCHOR";
   if(destination_touched && invalidation_touched)
      return "PAPER_PATH_BOTH_DESTINATION_AND_INVALIDATION_TOUCHED_SAME_CLOSE_AMBIGUOUS";
   if(destination_touched)
      return "PAPER_PATH_DESTINATION_TOUCHED_AFTER_HYPOTHETICAL_ENTRY";
   if(invalidation_touched)
      return "PAPER_PATH_INVALIDATION_TOUCHED_AFTER_HYPOTHETICAL_ENTRY";
   return "PAPER_PATH_HYPOTHETICAL_ENTRY_OPEN_NO_EXIT_TOUCH";
}

string FP_StateGatePaperLifecycleOutcome(const string path_state)
{
   if(StringFind(path_state, "DESTINATION_TOUCHED") >= 0 && StringFind(path_state, "BOTH") < 0)
      return "PAPER_OUTCOME_HYPOTHETICAL_DESTINATION";
   if(StringFind(path_state, "INVALIDATION_TOUCHED") >= 0 && StringFind(path_state, "BOTH") < 0)
      return "PAPER_OUTCOME_HYPOTHETICAL_INVALIDATION";
   if(StringFind(path_state, "BOTH") >= 0)
      return "PAPER_OUTCOME_AMBIGUOUS_SAME_CLOSE_ONLY";
   if(StringFind(path_state, "OPEN") >= 0)
      return "PAPER_OUTCOME_HYPOTHETICAL_OPEN";
   return "PAPER_OUTCOME_WAITING_FOR_ENTRY";
}

string FP_StateGatePaperLifecycleKey(const FP_StateGateSnapshot &snapshot,
                                     const int slot,
                                     const FP_StateGatePaperLedgerRow &p,
                                     const string path_state,
                                     const string outcome)
{
   string key = snapshot.symbol;
   key += "|TF=" + snapshot.tf_states[slot].timeframe_label;
   key += "|LEDGER=" + FP_StateGateKeyPart(p.ledger_key);
   key += "|PATH=" + FP_StateGateKeyPart(path_state);
   key += "|OUTCOME=" + FP_StateGateKeyPart(outcome);
   key += "|CLOSE=" + DoubleToString(p.last_closed_bar_close, 8);
   key += "|EXEC=DISABLED";
   return key;
}

bool FP_StateGateFirstPaperLedgerForLifecycleSlot(const FP_StateGateSnapshot &snapshot,
                                                  const int slot,
                                                  FP_StateGatePaperLedgerRow &out)
{
   for(int i=0; i<snapshot.paper_ledger_row_count; i++)
   {
      FP_StateGatePaperLedgerRow row = snapshot.paper_ledger_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateAddPaperLifecycleRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.paper_lifecycle_row_count >= FP_STATE_GATE_MAX_PAPER_LIFECYCLE_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGatePaperLedgerRow p;
   FP_ResetStateGatePaperLedgerRow(p);
   if(!FP_StateGateFirstPaperLedgerForLifecycleSlot(snapshot, slot, p))
      return false;

   int idx = snapshot.paper_lifecycle_row_count;
   FP_ResetStateGatePaperLifecycleRow(snapshot.paper_lifecycle_rows[idx]);

   string entry_status = FP_StateGatePaperEntryTouchStatus(p);
   string invalid_status = FP_StateGatePaperInvalidationTouchStatus(p);
   string dest_status = FP_StateGatePaperDestinationTouchStatus(p);

   bool entry_touched = (StringFind(entry_status, "TOUCHED") >= 0 && StringFind(entry_status, "NOT_TOUCHED") < 0);
   bool invalid_touched = (StringFind(invalid_status, "TOUCHED") >= 0 && StringFind(invalid_status, "NOT_TOUCHED") < 0);
   bool dest_touched = (StringFind(dest_status, "TOUCHED") >= 0 && StringFind(dest_status, "NOT_TOUCHED") < 0);

   if(!entry_touched)
   {
      invalid_touched = false;
      dest_touched = false;
   }

   string path_state = FP_StateGatePaperLifecyclePathState(entry_touched, invalid_touched, dest_touched);
   string outcome = FP_StateGatePaperLifecycleOutcome(path_state);
   string lifecycle_key = FP_StateGatePaperLifecycleKey(snapshot, slot, p, path_state, outcome);

   snapshot.paper_lifecycle_rows[idx].slot_index = slot;
   snapshot.paper_lifecycle_rows[idx].timeframe = p.timeframe;
   snapshot.paper_lifecycle_rows[idx].timeframe_label = p.timeframe_label;
   snapshot.paper_lifecycle_rows[idx].evaluated_at = TimeCurrent();
   snapshot.paper_lifecycle_rows[idx].last_closed_bar_time = p.last_closed_bar_time;
   snapshot.paper_lifecycle_rows[idx].last_closed_bar_close = p.last_closed_bar_close;
   snapshot.paper_lifecycle_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.paper_lifecycle_rows[idx].lifecycle_status = "PAPER_LIFECYCLE_EVALUATED_CLOSED_CLOSE_ONLY";
   snapshot.paper_lifecycle_rows[idx].path_state = path_state;
   snapshot.paper_lifecycle_rows[idx].entry_touch_status = entry_status;
   snapshot.paper_lifecycle_rows[idx].invalidation_touch_status = invalid_status;
   snapshot.paper_lifecycle_rows[idx].destination_touch_status = dest_status;
   snapshot.paper_lifecycle_rows[idx].outcome = outcome;
   snapshot.paper_lifecycle_rows[idx].direction = p.decision_direction;
   snapshot.paper_lifecycle_rows[idx].decision_type = p.decision_type;
   snapshot.paper_lifecycle_rows[idx].entry_price = p.entry_price;
   snapshot.paper_lifecycle_rows[idx].invalidation_price = p.invalidation_price;
   snapshot.paper_lifecycle_rows[idx].destination_price = p.destination_price;
   snapshot.paper_lifecycle_rows[idx].entry_touched = entry_touched;
   snapshot.paper_lifecycle_rows[idx].invalidation_touched = invalid_touched;
   snapshot.paper_lifecycle_rows[idx].destination_touched = dest_touched;
   snapshot.paper_lifecycle_rows[idx].source_ledger_key = p.ledger_key;
   snapshot.paper_lifecycle_rows[idx].source_decision_key = p.source_decision_key;
   snapshot.paper_lifecycle_rows[idx].event_id = p.event_id;
   snapshot.paper_lifecycle_rows[idx].lifecycle_key = lifecycle_key;
   snapshot.paper_lifecycle_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE18_LIFECYCLE_ONLY";
   snapshot.paper_lifecycle_rows[idx].label = p.timeframe_label + " | PAPER LIFECYCLE | " + path_state + " | " + outcome + " | close_only=true | real_execution=false";

   snapshot.paper_lifecycle_row_count++;
   snapshot.tf_states[slot].paper_lifecycle_row_count++;
   return true;
}

void FP_StateGateBuildPaperLifecycleRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.paper_lifecycle_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_PAPER_LIFECYCLE_ROWS; i++)
      FP_ResetStateGatePaperLifecycleRow(snapshot.paper_lifecycle_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].paper_lifecycle_row_count = 0;
      FP_StateGateAddPaperLifecycleRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstPaperLifecycleForSlot(const FP_StateGateSnapshot &snapshot,
                                            const int slot,
                                            FP_StateGatePaperLifecycleRow &out)
{
   for(int i=0; i<snapshot.paper_lifecycle_row_count; i++)
   {
      FP_StateGatePaperLifecycleRow row = snapshot.paper_lifecycle_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotPaperLifecycle(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGatePaperLifecycleRow row;
   FP_ResetStateGatePaperLifecycleRow(row);

   if(FP_StateGateFirstPaperLifecycleForSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].paper_lifecycle_status = row.lifecycle_status;
      snapshot.tf_states[slot].paper_lifecycle_key = row.lifecycle_key;
      snapshot.tf_states[slot].paper_lifecycle_event_id = row.event_id;
      snapshot.tf_states[slot].paper_lifecycle_path_state = row.path_state;
      snapshot.tf_states[slot].paper_entry_touch_status = row.entry_touch_status;
      snapshot.tf_states[slot].paper_invalidation_touch_status = row.invalidation_touch_status;
      snapshot.tf_states[slot].paper_destination_touch_status = row.destination_touch_status;
      snapshot.tf_states[slot].paper_lifecycle_outcome = row.outcome;
      snapshot.tf_states[slot].paper_lifecycle_execution_status = row.execution_status;
      snapshot.tf_states[slot].paper_lifecycle_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].paper_lifecycle_status = "PAPER_LIFECYCLE_NO_ROW";
   snapshot.tf_states[slot].paper_lifecycle_key = "NO_PAPER_LIFECYCLE_KEY";
   snapshot.tf_states[slot].paper_lifecycle_path_state = "PAPER_PATH_NO_ROW";
   snapshot.tf_states[slot].paper_lifecycle_outcome = "PAPER_OUTCOME_NO_ROW";
   snapshot.tf_states[slot].paper_lifecycle_execution_status = "REAL_EXECUTION_DISABLED_PHASE18_LIFECYCLE_ONLY";
   snapshot.tf_states[slot].paper_lifecycle_notes = "No paper lifecycle row was built";
}

void FP_StateGateFinalizeSnapshotPaperLifecycle(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotPaperLifecycle(snapshot, slot);
}



// ---------------------------------------------------------------------------
// Phase 19 - Paper Result Metrics / R-Equivalent Summary
// ---------------------------------------------------------------------------
// This layer summarizes paper lifecycle rows into dry-run result metrics.
// It remains non-executable and does not create broker-side performance state.

string FP_StateGatePaperResultBucket(const string outcome)
{
   if(StringFind(outcome, "DESTINATION") >= 0)
      return "PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN";
   if(StringFind(outcome, "INVALIDATION") >= 0)
      return "PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS";
   if(StringFind(outcome, "OPEN") >= 0)
      return "PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN";
   if(StringFind(outcome, "AMBIGUOUS") >= 0)
      return "PAPER_RESULT_BUCKET_AMBIGUOUS";
   if(StringFind(outcome, "WAITING") >= 0)
      return "PAPER_RESULT_BUCKET_WAITING";
   return "PAPER_RESULT_BUCKET_UNKNOWN";
}

string FP_StateGatePaperResultStatus(const string bucket)
{
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN")
      return "PAPER_RESULT_HYPOTHETICAL_WIN_NO_EXECUTION";
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS")
      return "PAPER_RESULT_HYPOTHETICAL_LOSS_NO_EXECUTION";
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN")
      return "PAPER_RESULT_HYPOTHETICAL_OPEN_NO_EXECUTION";
   if(bucket == "PAPER_RESULT_BUCKET_AMBIGUOUS")
      return "PAPER_RESULT_AMBIGUOUS_CLOSE_ONLY_NO_EXECUTION";
   if(bucket == "PAPER_RESULT_BUCKET_WAITING")
      return "PAPER_RESULT_WAITING_FOR_ENTRY_NO_EXECUTION";
   return "PAPER_RESULT_UNKNOWN_NO_EXECUTION";
}

double FP_StateGatePaperSignedDelta(const FP_StateGatePaperLifecycleRow &p,
                                    const string bucket)
{
   if(p.entry_price == 0.0)
      return 0.0;

   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN" && p.destination_price != 0.0)
      return MathAbs(p.destination_price - p.entry_price);

   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS" && p.invalidation_price != 0.0)
      return -MathAbs(p.entry_price - p.invalidation_price);

   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN" && p.last_closed_bar_close != 0.0)
   {
      if(FP_StateGatePaperIsBuyDirection(p.direction))
         return p.last_closed_bar_close - p.entry_price;
      if(FP_StateGatePaperIsSellDirection(p.direction))
         return p.entry_price - p.last_closed_bar_close;
   }

   return 0.0;
}

string FP_StateGatePaperRStatus(const FP_StateGatePaperLifecycleRow &p,
                                const double signed_delta)
{
   if(p.entry_price == 0.0)
      return "PAPER_R_BLOCKED_NO_ENTRY_PRICE";
   if(p.invalidation_price == 0.0 || MathAbs(p.entry_price - p.invalidation_price) == 0.0)
      return "PAPER_R_PENDING_INVALIDATION_BUFFER_NO_RISK_DISTANCE";
   if(signed_delta == 0.0)
      return "PAPER_R_ZERO_OR_WAITING";
   return "PAPER_R_EQUIVALENT_READY_PAPER_ONLY";
}

double FP_StateGatePaperRMultiple(const FP_StateGatePaperLifecycleRow &p,
                                  const double signed_delta)
{
   if(p.entry_price == 0.0 || p.invalidation_price == 0.0)
      return 0.0;
   double risk = MathAbs(p.entry_price - p.invalidation_price);
   if(risk == 0.0)
      return 0.0;
   return signed_delta / risk;
}

double FP_StateGatePaperExitAnchor(const FP_StateGatePaperLifecycleRow &p,
                                   const string bucket)
{
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN")
      return p.destination_price;
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS")
      return p.invalidation_price;
   if(bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN")
      return p.last_closed_bar_close;
   return 0.0;
}

string FP_StateGatePaperResultKey(const FP_StateGateSnapshot &snapshot,
                                  const int slot,
                                  const FP_StateGatePaperLifecycleRow &p,
                                  const string result_status,
                                  const string bucket,
                                  const double signed_delta,
                                  const string r_status)
{
   string key = snapshot.symbol;
   key += "|TF=" + snapshot.tf_states[slot].timeframe_label;
   key += "|STATUS=" + FP_StateGateKeyPart(result_status);
   key += "|BUCKET=" + FP_StateGateKeyPart(bucket);
   key += "|OUTCOME=" + FP_StateGateKeyPart(p.outcome);
   key += "|DELTA=" + DoubleToString(signed_delta, 8);
   key += "|RSTATUS=" + FP_StateGateKeyPart(r_status);
   key += "|LIFE=" + FP_StateGateKeyPart(p.lifecycle_key);
   key += "|EXEC=DISABLED";
   return key;
}

bool FP_StateGateFirstPaperLifecycleForResultSlot(const FP_StateGateSnapshot &snapshot,
                                                  const int slot,
                                                  FP_StateGatePaperLifecycleRow &out)
{
   for(int i=0; i<snapshot.paper_lifecycle_row_count; i++)
   {
      FP_StateGatePaperLifecycleRow row = snapshot.paper_lifecycle_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateAddPaperResultRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.paper_result_row_count >= FP_STATE_GATE_MAX_PAPER_RESULT_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGatePaperLifecycleRow p;
   FP_ResetStateGatePaperLifecycleRow(p);
   if(!FP_StateGateFirstPaperLifecycleForResultSlot(snapshot, slot, p))
      return false;

   int idx = snapshot.paper_result_row_count;
   FP_ResetStateGatePaperResultRow(snapshot.paper_result_rows[idx]);

   string bucket = FP_StateGatePaperResultBucket(p.outcome);
   string result_status = FP_StateGatePaperResultStatus(bucket);
   double signed_delta = FP_StateGatePaperSignedDelta(p, bucket);
   double abs_distance = MathAbs(signed_delta);
   string r_status = FP_StateGatePaperRStatus(p, signed_delta);
   double r_multiple = FP_StateGatePaperRMultiple(p, signed_delta);
   double exit_anchor = FP_StateGatePaperExitAnchor(p, bucket);
   string result_key = FP_StateGatePaperResultKey(snapshot, slot, p, result_status, bucket, signed_delta, r_status);

   snapshot.paper_result_rows[idx].slot_index = slot;
   snapshot.paper_result_rows[idx].timeframe = p.timeframe;
   snapshot.paper_result_rows[idx].timeframe_label = p.timeframe_label;
   snapshot.paper_result_rows[idx].summarized_at = TimeCurrent();
   snapshot.paper_result_rows[idx].last_closed_bar_time = p.last_closed_bar_time;
   snapshot.paper_result_rows[idx].last_closed_bar_close = p.last_closed_bar_close;
   snapshot.paper_result_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.paper_result_rows[idx].result_status = result_status;
   snapshot.paper_result_rows[idx].outcome = p.outcome;
   snapshot.paper_result_rows[idx].result_bucket = bucket;
   snapshot.paper_result_rows[idx].direction = p.direction;
   snapshot.paper_result_rows[idx].decision_type = p.decision_type;
   snapshot.paper_result_rows[idx].entry_price = p.entry_price;
   snapshot.paper_result_rows[idx].exit_anchor_price = exit_anchor;
   snapshot.paper_result_rows[idx].destination_price = p.destination_price;
   snapshot.paper_result_rows[idx].invalidation_price = p.invalidation_price;
   snapshot.paper_result_rows[idx].price_delta = signed_delta;
   snapshot.paper_result_rows[idx].abs_distance = abs_distance;
   snapshot.paper_result_rows[idx].r_status = r_status;
   snapshot.paper_result_rows[idx].r_multiple = r_multiple;
   snapshot.paper_result_rows[idx].source_lifecycle_key = p.lifecycle_key;
   snapshot.paper_result_rows[idx].source_ledger_key = p.source_ledger_key;
   snapshot.paper_result_rows[idx].source_decision_key = p.source_decision_key;
   snapshot.paper_result_rows[idx].event_id = p.event_id;
   snapshot.paper_result_rows[idx].result_key = result_key;
   snapshot.paper_result_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE19_RESULT_ONLY";
   snapshot.paper_result_rows[idx].label = p.timeframe_label + " | PAPER RESULT | " + result_status + " | " + bucket + " | delta=" + DoubleToString(signed_delta, 8) + " | " + r_status;

   snapshot.paper_result_row_count++;
   snapshot.tf_states[slot].paper_result_row_count++;
   return true;
}

void FP_StateGateBuildPaperResultRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.paper_result_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_PAPER_RESULT_ROWS; i++)
      FP_ResetStateGatePaperResultRow(snapshot.paper_result_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].paper_result_row_count = 0;
      FP_StateGateAddPaperResultRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstPaperResultForSlot(const FP_StateGateSnapshot &snapshot,
                                         const int slot,
                                         FP_StateGatePaperResultRow &out)
{
   for(int i=0; i<snapshot.paper_result_row_count; i++)
   {
      FP_StateGatePaperResultRow row = snapshot.paper_result_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotPaperResult(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGatePaperResultRow row;
   FP_ResetStateGatePaperResultRow(row);

   if(FP_StateGateFirstPaperResultForSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].paper_result_status = row.result_status;
      snapshot.tf_states[slot].paper_result_key = row.result_key;
      snapshot.tf_states[slot].paper_result_outcome = row.outcome;
      snapshot.tf_states[slot].paper_result_direction = row.direction;
      snapshot.tf_states[slot].paper_result_type = row.decision_type;
      snapshot.tf_states[slot].paper_result_entry_price = row.entry_price;
      snapshot.tf_states[slot].paper_result_exit_anchor_price = row.exit_anchor_price;
      snapshot.tf_states[slot].paper_result_price_delta = row.price_delta;
      snapshot.tf_states[slot].paper_result_abs_distance = row.abs_distance;
      snapshot.tf_states[slot].paper_result_r_status = row.r_status;
      snapshot.tf_states[slot].paper_result_r_multiple = row.r_multiple;
      snapshot.tf_states[slot].paper_result_bucket = row.result_bucket;
      snapshot.tf_states[slot].paper_result_execution_status = row.execution_status;
      snapshot.tf_states[slot].paper_result_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].paper_result_status = "PAPER_RESULT_NO_ROW";
   snapshot.tf_states[slot].paper_result_key = "NO_PAPER_RESULT_KEY";
   snapshot.tf_states[slot].paper_result_outcome = "PAPER_RESULT_NO_OUTCOME";
   snapshot.tf_states[slot].paper_result_execution_status = "REAL_EXECUTION_DISABLED_PHASE19_RESULT_ONLY";
   snapshot.tf_states[slot].paper_result_notes = "No paper result row was built";
}

void FP_StateGateFinalizeSnapshotPaperResults(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotPaperResult(snapshot, slot);
}



// ---------------------------------------------------------------------------
// Phase 20 - Paper Portfolio / Aggregate Metrics
// ---------------------------------------------------------------------------
// This layer aggregates paper result rows across the configured State Gate
// timeframes.  It remains non-executable and portfolio-only.

string FP_StateGatePaperPortfolioStatus(const int total_rows,
                                        const int win_rows,
                                        const int loss_rows,
                                        const int open_rows,
                                        const int waiting_rows,
                                        const int ambiguous_rows)
{
   if(total_rows <= 0)
      return "PAPER_PORTFOLIO_EMPTY_NO_EXECUTION";
   if(ambiguous_rows > 0)
      return "PAPER_PORTFOLIO_HAS_AMBIGUOUS_ROWS_NO_EXECUTION";
   if(open_rows > 0)
      return "PAPER_PORTFOLIO_HAS_OPEN_ROWS_NO_EXECUTION";
   if(waiting_rows == total_rows)
      return "PAPER_PORTFOLIO_WAITING_ONLY_NO_EXECUTION";
   if(win_rows > 0 && loss_rows == 0)
      return "PAPER_PORTFOLIO_WIN_LIKE_ONLY_NO_EXECUTION";
   if(loss_rows > 0 && win_rows == 0)
      return "PAPER_PORTFOLIO_LOSS_LIKE_ONLY_NO_EXECUTION";
   return "PAPER_PORTFOLIO_MIXED_RESULT_ROWS_NO_EXECUTION";
}

string FP_StateGatePaperPortfolioDistribution(const int total_rows,
                                              const int win_rows,
                                              const int loss_rows,
                                              const int open_rows,
                                              const int waiting_rows,
                                              const int ambiguous_rows,
                                              const int unknown_rows)
{
   string d = "total=" + IntegerToString(total_rows);
   d += "|win=" + IntegerToString(win_rows);
   d += "|loss=" + IntegerToString(loss_rows);
   d += "|open=" + IntegerToString(open_rows);
   d += "|waiting=" + IntegerToString(waiting_rows);
   d += "|ambiguous=" + IntegerToString(ambiguous_rows);
   d += "|unknown=" + IntegerToString(unknown_rows);
   return d;
}

string FP_StateGatePaperPortfolioKey(const FP_StateGateSnapshot &snapshot,
                                      const string portfolio_status,
                                      const string distribution,
                                      const double net_delta,
                                      const double avg_R)
{
   string key = snapshot.symbol;
   key += "|PORTFOLIO=" + FP_StateGateKeyPart(portfolio_status);
   key += "|DIST=" + FP_StateGateKeyPart(distribution);
   key += "|NET=" + DoubleToString(net_delta, 8);
   key += "|AVGR=" + DoubleToString(avg_R, 8);
   key += "|EXEC=DISABLED";
   return key;
}

void FP_StateGateBuildPaperPortfolioRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.paper_portfolio_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_PAPER_PORTFOLIO_ROWS; i++)
      FP_ResetStateGatePaperPortfolioRow(snapshot.paper_portfolio_rows[i]);

   if(FP_STATE_GATE_MAX_PAPER_PORTFOLIO_ROWS <= 0)
      return;

   int idx = 0;
   FP_ResetStateGatePaperPortfolioRow(snapshot.paper_portfolio_rows[idx]);

   int total_rows = snapshot.paper_result_row_count;
   int win_rows = 0;
   int loss_rows = 0;
   int open_rows = 0;
   int waiting_rows = 0;
   int ambiguous_rows = 0;
   int unknown_rows = 0;
   int r_ready_rows = 0;
   int r_pending_rows = 0;

   double net_delta = 0.0;
   double sum_R = 0.0;
   double best_R = 0.0;
   double worst_R = 0.0;
   bool have_R = false;

   for(int r=0; r<snapshot.paper_result_row_count; r++)
   {
      FP_StateGatePaperResultRow row = snapshot.paper_result_rows[r];
      net_delta += row.price_delta;

      if(row.result_bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN")
         win_rows++;
      else if(row.result_bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS")
         loss_rows++;
      else if(row.result_bucket == "PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN")
         open_rows++;
      else if(row.result_bucket == "PAPER_RESULT_BUCKET_WAITING")
         waiting_rows++;
      else if(row.result_bucket == "PAPER_RESULT_BUCKET_AMBIGUOUS")
         ambiguous_rows++;
      else
         unknown_rows++;

      if(StringFind(row.r_status, "READY") >= 0)
      {
         r_ready_rows++;
         sum_R += row.r_multiple;
         if(!have_R)
         {
            best_R = row.r_multiple;
            worst_R = row.r_multiple;
            have_R = true;
         }
         else
         {
            if(row.r_multiple > best_R) best_R = row.r_multiple;
            if(row.r_multiple < worst_R) worst_R = row.r_multiple;
         }
      }
      else
         r_pending_rows++;
   }

   double avg_delta = 0.0;
   if(total_rows > 0)
      avg_delta = net_delta / total_rows;

   double avg_R = 0.0;
   if(r_ready_rows > 0)
      avg_R = sum_R / r_ready_rows;

   string status = FP_StateGatePaperPortfolioStatus(total_rows, win_rows, loss_rows, open_rows, waiting_rows, ambiguous_rows);
   string distribution = FP_StateGatePaperPortfolioDistribution(total_rows, win_rows, loss_rows, open_rows, waiting_rows, ambiguous_rows, unknown_rows);
   string key = FP_StateGatePaperPortfolioKey(snapshot, status, distribution, net_delta, avg_R);

   snapshot.paper_portfolio_rows[idx].row_index = idx;
   snapshot.paper_portfolio_rows[idx].summarized_at = TimeCurrent();
   snapshot.paper_portfolio_rows[idx].status = FP_STATE_GATE_ROW_PROJECTED;
   snapshot.paper_portfolio_rows[idx].portfolio_status = status;
   snapshot.paper_portfolio_rows[idx].portfolio_key = key;
   snapshot.paper_portfolio_rows[idx].total_result_rows = total_rows;
   snapshot.paper_portfolio_rows[idx].win_like_rows = win_rows;
   snapshot.paper_portfolio_rows[idx].loss_like_rows = loss_rows;
   snapshot.paper_portfolio_rows[idx].open_rows = open_rows;
   snapshot.paper_portfolio_rows[idx].waiting_rows = waiting_rows;
   snapshot.paper_portfolio_rows[idx].ambiguous_rows = ambiguous_rows;
   snapshot.paper_portfolio_rows[idx].unknown_rows = unknown_rows;
   snapshot.paper_portfolio_rows[idx].r_ready_rows = r_ready_rows;
   snapshot.paper_portfolio_rows[idx].r_pending_rows = r_pending_rows;
   snapshot.paper_portfolio_rows[idx].net_delta = net_delta;
   snapshot.paper_portfolio_rows[idx].avg_delta = avg_delta;
   snapshot.paper_portfolio_rows[idx].avg_R = avg_R;
   snapshot.paper_portfolio_rows[idx].best_R = best_R;
   snapshot.paper_portfolio_rows[idx].worst_R = worst_R;
   snapshot.paper_portfolio_rows[idx].result_distribution = distribution;
   snapshot.paper_portfolio_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE20_PORTFOLIO_ONLY";
   snapshot.paper_portfolio_rows[idx].label = "PAPER PORTFOLIO | " + status + " | " + distribution + " | net_delta=" + DoubleToString(net_delta, 8) + " | avg_R=" + DoubleToString(avg_R, 8) + " | real_execution=false";

   snapshot.paper_portfolio_row_count = 1;
}

void FP_StateGateFinalizeSnapshotPaperPortfolio(FP_StateGateSnapshot &snapshot)
{
   if(snapshot.paper_portfolio_row_count <= 0)
   {
      snapshot.paper_portfolio_status = "PAPER_PORTFOLIO_NO_ROW";
      snapshot.paper_portfolio_key = "NO_PAPER_PORTFOLIO_KEY";
      snapshot.paper_portfolio_execution_status = "REAL_EXECUTION_DISABLED_PHASE20_PORTFOLIO_ONLY";
      snapshot.paper_portfolio_notes = "No paper portfolio row was built";
      return;
   }

   FP_StateGatePaperPortfolioRow row = snapshot.paper_portfolio_rows[0];
   snapshot.paper_portfolio_status = row.portfolio_status;
   snapshot.paper_portfolio_key = row.portfolio_key;
   snapshot.paper_portfolio_total_results = row.total_result_rows;
   snapshot.paper_portfolio_win_like_rows = row.win_like_rows;
   snapshot.paper_portfolio_loss_like_rows = row.loss_like_rows;
   snapshot.paper_portfolio_open_rows = row.open_rows;
   snapshot.paper_portfolio_waiting_rows = row.waiting_rows;
   snapshot.paper_portfolio_ambiguous_rows = row.ambiguous_rows;
   snapshot.paper_portfolio_unknown_rows = row.unknown_rows;
   snapshot.paper_portfolio_r_ready_rows = row.r_ready_rows;
   snapshot.paper_portfolio_r_pending_rows = row.r_pending_rows;
   snapshot.paper_portfolio_net_delta = row.net_delta;
   snapshot.paper_portfolio_avg_delta = row.avg_delta;
   snapshot.paper_portfolio_avg_R = row.avg_R;
   snapshot.paper_portfolio_best_R = row.best_R;
   snapshot.paper_portfolio_worst_R = row.worst_R;
   snapshot.paper_portfolio_distribution = row.result_distribution;
   snapshot.paper_portfolio_execution_status = row.execution_status;
   snapshot.paper_portfolio_notes = row.label;
}



// ---------------------------------------------------------------------------
// Phase 21 - Paper Regime Attribution
// ---------------------------------------------------------------------------
// This layer attributes paper result rows back to the context that produced
// them.  It remains non-executable and does not make trading decisions.

string FP_StateGatePaperRegimeContextFamily(const FP_StateGateTimeframeState &s)
{
   bool has_hook = (StringFind(s.primary_extreme_source, "HOOK") >= 0 || StringFind(s.primary_entry_idea_family, "HOOK") >= 0);
   bool has_rally = (StringFind(s.primary_extreme_source, "RALLY") >= 0 || StringFind(s.primary_entry_idea_family, "RALLY") >= 0);
   bool mtf_aligned = (StringFind(s.mtf_direction_relation, "ALIGNED") >= 0 || StringFind(s.mtf_context_role, "ALIGNED") >= 0);
   bool mtf_divergent = (StringFind(s.mtf_direction_relation, "DIVERGENT") >= 0 || StringFind(s.mtf_context_role, "DIVERGENCE") >= 0);

   if(has_hook && mtf_aligned)
      return "REGIME_MTF_ALIGNED_HOOK_EXTREME";
   if(has_hook && mtf_divergent)
      return "REGIME_MTF_DIVERGENT_HOOK_EXTREME";
   if(has_hook)
      return "REGIME_HOOK_EXTREME";
   if(has_rally && mtf_aligned)
      return "REGIME_MTF_ALIGNED_RALLY_CONTEXT";
   if(has_rally)
      return "REGIME_RALLY_CONTEXT";
   if(StringFind(s.geometry_readiness, "READY") >= 0 || StringFind(s.geometry_readiness, "PARTIAL") >= 0)
      return "REGIME_GEOMETRY_CONTEXT";
   return "REGIME_CONTEXT_PENDING";
}

string FP_StateGatePaperRegimeSourceContext(const FP_StateGateTimeframeState &s)
{
   string out = s.primary_extreme_source;
   out += "|SIDE=" + s.primary_extreme_side;
   out += "|ROLE=" + s.primary_extreme_role;
   out += "|DIR=" + s.primary_extreme_direction;
   return out;
}

string FP_StateGatePaperRegimeMtfContext(const FP_StateGateTimeframeState &s)
{
   string out = s.mtf_context_role;
   out += "|DIR_REL=" + s.mtf_direction_relation;
   out += "|SIDE_REL=" + s.mtf_side_relation;
   out += "|PARENT=" + s.mtf_parent_timeframe;
   return out;
}

string FP_StateGatePaperRegimeGeometryContext(const FP_StateGateTimeframeState &s)
{
   string out = s.geometry_readiness;
   out += "|ENTRY=" + s.candidate_entry_price_status;
   out += "|DEST=" + s.candidate_destination_price_status;
   out += "|R=" + s.potential_R_status;
   return out;
}

string FP_StateGatePaperRegimeAttributionStatus(const FP_StateGateTimeframeState &s,
                                                const FP_StateGatePaperResultRow &r)
{
   if(!s.closed_bar_available)
      return "PAPER_REGIME_BLOCKED_NO_CLOSED_BAR";
   if(r.result_key == "NO_PAPER_RESULT_KEY" || r.result_key == "")
      return "PAPER_REGIME_BLOCKED_NO_RESULT_ROW";
   if(StringFind(r.result_bucket, "UNKNOWN") >= 0)
      return "PAPER_REGIME_ATTRIBUTED_UNKNOWN_RESULT_NO_EXECUTION";
   return "PAPER_REGIME_ATTRIBUTED_NO_EXECUTION";
}

string FP_StateGatePaperRegimeKey(const FP_StateGateSnapshot &snapshot,
                                  const int slot,
                                  const FP_StateGatePaperResultRow &r,
                                  const string context_family,
                                  const string attribution_status)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string key = snapshot.symbol;
   key += "|TF=" + s.timeframe_label;
   key += "|ATTR=" + FP_StateGateKeyPart(attribution_status);
   key += "|CTX=" + FP_StateGateKeyPart(context_family);
   key += "|OUTCOME=" + FP_StateGateKeyPart(r.outcome);
   key += "|BUCKET=" + FP_StateGateKeyPart(r.result_bucket);
   key += "|IDEA=" + FP_StateGateKeyPart(s.primary_entry_idea_family);
   key += "|MTF=" + FP_StateGateKeyPart(s.mtf_context_role);
   key += "|RESULT=" + FP_StateGateKeyPart(r.result_key);
   key += "|EXEC=DISABLED";
   return key;
}

bool FP_StateGateFirstPaperResultForRegimeSlot(const FP_StateGateSnapshot &snapshot,
                                               const int slot,
                                               FP_StateGatePaperResultRow &out)
{
   for(int i=0; i<snapshot.paper_result_row_count; i++)
   {
      FP_StateGatePaperResultRow row = snapshot.paper_result_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateFirstPaperLifecycleForRegimeSlot(const FP_StateGateSnapshot &snapshot,
                                                  const int slot,
                                                  FP_StateGatePaperLifecycleRow &out)
{
   for(int i=0; i<snapshot.paper_lifecycle_row_count; i++)
   {
      FP_StateGatePaperLifecycleRow row = snapshot.paper_lifecycle_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

bool FP_StateGateAddPaperRegimeRowForSlot(FP_StateGateSnapshot &snapshot, const int slot)
{
   if(snapshot.paper_regime_row_count >= FP_STATE_GATE_MAX_PAPER_REGIME_ROWS)
      return false;
   if(slot < 0 || slot >= snapshot.timeframe_count)
      return false;

   FP_StateGatePaperResultRow result;
   FP_ResetStateGatePaperResultRow(result);
   if(!FP_StateGateFirstPaperResultForRegimeSlot(snapshot, slot, result))
      return false;

   FP_StateGatePaperLifecycleRow lifecycle;
   FP_ResetStateGatePaperLifecycleRow(lifecycle);
   bool has_lifecycle = FP_StateGateFirstPaperLifecycleForRegimeSlot(snapshot, slot, lifecycle);

   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   int idx = snapshot.paper_regime_row_count;
   FP_ResetStateGatePaperRegimeRow(snapshot.paper_regime_rows[idx]);

   string context_family = FP_StateGatePaperRegimeContextFamily(s);
   string source_context = FP_StateGatePaperRegimeSourceContext(s);
   string mtf_context = FP_StateGatePaperRegimeMtfContext(s);
   string geometry_context = FP_StateGatePaperRegimeGeometryContext(s);
   string attribution_status = FP_StateGatePaperRegimeAttributionStatus(s, result);
   string lifecycle_path = (has_lifecycle ? lifecycle.path_state : "PAPER_PATH_MISSING_FOR_ATTRIBUTION");
   string attribution_key = FP_StateGatePaperRegimeKey(snapshot, slot, result, context_family, attribution_status);

   snapshot.paper_regime_rows[idx].slot_index = slot;
   snapshot.paper_regime_rows[idx].timeframe = s.timeframe;
   snapshot.paper_regime_rows[idx].timeframe_label = s.timeframe_label;
   snapshot.paper_regime_rows[idx].attributed_at = TimeCurrent();
   snapshot.paper_regime_rows[idx].last_closed_bar_time = s.last_closed_bar_time;
   snapshot.paper_regime_rows[idx].last_closed_bar_close = s.last_closed_bar_close;
   snapshot.paper_regime_rows[idx].status = (StringFind(attribution_status, "ATTRIBUTED") >= 0 ? FP_STATE_GATE_ROW_PROJECTED : FP_STATE_GATE_ROW_PLACEHOLDER);
   snapshot.paper_regime_rows[idx].attribution_status = attribution_status;
   snapshot.paper_regime_rows[idx].context_family = context_family;
   snapshot.paper_regime_rows[idx].source_context = source_context;
   snapshot.paper_regime_rows[idx].mtf_context = mtf_context;
   snapshot.paper_regime_rows[idx].mtf_direction_relation = s.mtf_direction_relation;
   snapshot.paper_regime_rows[idx].mtf_side_relation = s.mtf_side_relation;
   snapshot.paper_regime_rows[idx].geometry_context = geometry_context;
   snapshot.paper_regime_rows[idx].idea_family = s.primary_entry_idea_family;
   snapshot.paper_regime_rows[idx].idea_type = s.primary_entry_idea_type;
   snapshot.paper_regime_rows[idx].decision_type = s.entry_decision_type;
   snapshot.paper_regime_rows[idx].extreme_source = s.primary_extreme_source;
   snapshot.paper_regime_rows[idx].extreme_side = s.primary_extreme_side;
   snapshot.paper_regime_rows[idx].hook_context = s.hook_summary;
   snapshot.paper_regime_rows[idx].rally_context = s.probable_next_f_summary;
   snapshot.paper_regime_rows[idx].lifecycle_path_state = lifecycle_path;
   snapshot.paper_regime_rows[idx].outcome = result.outcome;
   snapshot.paper_regime_rows[idx].result_bucket = result.result_bucket;
   snapshot.paper_regime_rows[idx].price_delta = result.price_delta;
   snapshot.paper_regime_rows[idx].r_status = result.r_status;
   snapshot.paper_regime_rows[idx].r_multiple = result.r_multiple;
   snapshot.paper_regime_rows[idx].source_result_key = result.result_key;
   snapshot.paper_regime_rows[idx].source_lifecycle_key = (has_lifecycle ? lifecycle.lifecycle_key : "NO_SOURCE_LIFECYCLE_KEY");
   snapshot.paper_regime_rows[idx].source_portfolio_key = snapshot.paper_portfolio_key;
   snapshot.paper_regime_rows[idx].attribution_key = attribution_key;
   snapshot.paper_regime_rows[idx].execution_status = "REAL_EXECUTION_DISABLED_PHASE21_ATTRIBUTION_ONLY";
   snapshot.paper_regime_rows[idx].label = s.timeframe_label + " | PAPER REGIME | " + context_family + " | " + result.result_bucket + " | " + result.outcome + " | real_execution=false";

   snapshot.paper_regime_row_count++;
   snapshot.tf_states[slot].paper_regime_row_count++;
   return true;
}

void FP_StateGateBuildPaperRegimeRows(FP_StateGateSnapshot &snapshot)
{
   snapshot.paper_regime_row_count = 0;
   for(int i=0; i<FP_STATE_GATE_MAX_PAPER_REGIME_ROWS; i++)
      FP_ResetStateGatePaperRegimeRow(snapshot.paper_regime_rows[i]);

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      snapshot.tf_states[slot].paper_regime_row_count = 0;
      FP_StateGateAddPaperRegimeRowForSlot(snapshot, slot);
   }
}

bool FP_StateGateFirstPaperRegimeForSlot(const FP_StateGateSnapshot &snapshot,
                                         const int slot,
                                         FP_StateGatePaperRegimeRow &out)
{
   for(int i=0; i<snapshot.paper_regime_row_count; i++)
   {
      FP_StateGatePaperRegimeRow row = snapshot.paper_regime_rows[i];
      if(row.slot_index != slot)
         continue;
      out = row;
      return true;
   }
   return false;
}

void FP_StateGateFinalizeSlotPaperRegime(FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGatePaperRegimeRow row;
   FP_ResetStateGatePaperRegimeRow(row);

   if(FP_StateGateFirstPaperRegimeForSlot(snapshot, slot, row))
   {
      snapshot.tf_states[slot].paper_regime_status = row.attribution_status;
      snapshot.tf_states[slot].paper_regime_key = row.attribution_key;
      snapshot.tf_states[slot].paper_regime_context_family = row.context_family;
      snapshot.tf_states[slot].paper_regime_source_context = row.source_context;
      snapshot.tf_states[slot].paper_regime_mtf_context = row.mtf_context;
      snapshot.tf_states[slot].paper_regime_geometry_context = row.geometry_context;
      snapshot.tf_states[slot].paper_regime_outcome = row.outcome;
      snapshot.tf_states[slot].paper_regime_result_bucket = row.result_bucket;
      snapshot.tf_states[slot].paper_regime_execution_status = row.execution_status;
      snapshot.tf_states[slot].paper_regime_notes = row.label;
      return;
   }

   snapshot.tf_states[slot].paper_regime_status = "PAPER_REGIME_NO_ROW";
   snapshot.tf_states[slot].paper_regime_key = "NO_PAPER_REGIME_KEY";
   snapshot.tf_states[slot].paper_regime_context_family = "PAPER_REGIME_NO_CONTEXT";
   snapshot.tf_states[slot].paper_regime_outcome = "PAPER_REGIME_NO_OUTCOME";
   snapshot.tf_states[slot].paper_regime_execution_status = "REAL_EXECUTION_DISABLED_PHASE21_ATTRIBUTION_ONLY";
   snapshot.tf_states[slot].paper_regime_notes = "No paper regime attribution row was built";
}

void FP_StateGateFinalizeSnapshotPaperRegime(FP_StateGateSnapshot &snapshot)
{
   for(int slot=0; slot<snapshot.timeframe_count; slot++)
      FP_StateGateFinalizeSlotPaperRegime(snapshot, slot);
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
