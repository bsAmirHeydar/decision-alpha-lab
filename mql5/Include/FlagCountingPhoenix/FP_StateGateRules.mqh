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
