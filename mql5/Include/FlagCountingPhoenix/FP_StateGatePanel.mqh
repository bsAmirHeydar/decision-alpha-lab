#ifndef __FP_STATE_GATE_PANEL_MQH__
#define __FP_STATE_GATE_PANEL_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Panel
// ----------------------------------------------------------------------------
// Phase 9 keeps the State Gate read-only and adds panel diagnostics on top of the Phase 7/8 usability work:
// - default left-upper placement
// - hard left-upper override for old saved right-corner inputs
// - master minimize / restore
// - per-timeframe section minimize / restore
// - per-timeframe Rally subsection minimize / restore
// - per-timeframe Hook subsection minimize / restore
// The panel remains a pure visualization layer above the locked anatomy
// engines and must never modify Node / Hook / F-counting logic.
// ============================================================================

static bool g_fp_state_gate_section_state_init = false;
static bool g_fp_state_gate_slot_collapsed[FP_STATE_GATE_TF_SLOTS];
static bool g_fp_state_gate_slot_rally_collapsed[FP_STATE_GATE_TF_SLOTS];
static bool g_fp_state_gate_slot_hook_collapsed[FP_STATE_GATE_TF_SLOTS];

void FP_StateGateEnsurePanelState()
{
   if(g_fp_state_gate_section_state_init)
      return;
   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
   {
      g_fp_state_gate_slot_collapsed[i] = false;
      g_fp_state_gate_slot_rally_collapsed[i] = false;
      g_fp_state_gate_slot_hook_collapsed[i] = false;
   }
   g_fp_state_gate_section_state_init = true;
}

string FP_StateGateObjectName(const FP_StateGateConfig &cfg, const string suffix)
{
   return cfg.object_prefix + suffix;
}

int FP_StateGatePanelCorner(const FP_StateGateConfig &cfg)
{
   // Left override wins over older saved right-corner inputs.
   // This fixes cases where old EA input sets kept ForceRightUpper=true
   // and pushed the panel away from the intended upper-left dashboard area.
   if(cfg.panel_force_left_upper)
      return CORNER_LEFT_UPPER;
   if(cfg.panel_force_right_upper)
      return CORNER_RIGHT_UPPER;
   return cfg.panel_corner;
}

int FP_StateGatePanelRallyPreviewLimit(const FP_StateGateConfig &cfg)
{
   return FP_StateGateClampInt(cfg.panel_rally_preview_rows_per_tf, 0, 8);
}

int FP_StateGatePanelHookPreviewLimit(const FP_StateGateConfig &cfg)
{
   return FP_StateGateClampInt(cfg.panel_hook_preview_rows_per_tf, 0, 12);
}

int FP_StateGatePanelTextLimit(const int width, const int font_size)
{
   int chars = width / MathMax(5, font_size - 1);
   return FP_StateGateClampInt(chars, 28, 160);
}

string FP_StateGatePanelClip(const string s, const int limit)
{
   if(limit <= 0)
      return "";
   int n = StringLen(s);
   if(n <= limit || limit < 8)
      return s;
   return StringSubstr(s, 0, limit - 3) + "...";
}

int FP_StateGatePanelCleanup(const FP_StateGateConfig &cfg)
{
   int deleted = 0;
   int total = ObjectsTotal(0, -1, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, cfg.object_prefix) == 0)
      {
         if(ObjectDelete(0, name))
            deleted++;
      }
   }
   return deleted;
}

bool FP_StateGateCreateRect(const FP_StateGateConfig &cfg,
                            const string suffix,
                            const int x,
                            const int y,
                            const int width,
                            const int height,
                            const color bg,
                            const color border,
                            FP_StateGateReport &report)
{
   string name = FP_StateGateObjectName(cfg, suffix);
   report.objects_requested++;
   if(ObjectFind(0, name) < 0)
   {
      if(!ObjectCreate(0, name, OBJ_RECTANGLE_LABEL, 0, 0, 0))
      {
         report.object_errors++;
         report.ok = false;
         report.status = "panel_rect_create_failed";
         report.reason = name;
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_XSIZE, width);
   ObjectSetInteger(0, name, OBJPROP_YSIZE, height);
   ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg);
   ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
   ObjectSetInteger(0, name, OBJPROP_COLOR, border);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 95);
   return true;
}

bool FP_StateGateCreateLabel(const FP_StateGateConfig &cfg,
                             const string suffix,
                             const int x,
                             const int y,
                             const string text,
                             const color clr,
                             const int font_size,
                             FP_StateGateReport &report)
{
   string name = FP_StateGateObjectName(cfg, suffix);
   report.objects_requested++;
   if(ObjectFind(0, name) < 0)
   {
      if(!ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0))
      {
         report.object_errors++;
         report.ok = false;
         report.status = "panel_label_create_failed";
         report.reason = name;
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 105);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 100);
   return true;
}

bool FP_StateGateCreateButton(const FP_StateGateConfig &cfg,
                              const string suffix,
                              const int x,
                              const int y,
                              const int width,
                              const int height,
                              const string text,
                              FP_StateGateReport &report)
{
   string name = FP_StateGateObjectName(cfg, suffix);
   report.objects_requested++;
   if(ObjectFind(0, name) < 0)
   {
      if(!ObjectCreate(0, name, OBJ_BUTTON, 0, 0, 0))
      {
         report.object_errors++;
         report.ok = false;
         report.status = "panel_button_create_failed";
         report.reason = name;
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_XSIZE, width);
   ObjectSetInteger(0, name, OBJPROP_YSIZE, height);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clrWhite);
   ObjectSetInteger(0, name, OBJPROP_BGCOLOR, clrSlateGray);
   ObjectSetInteger(0, name, OBJPROP_BORDER_COLOR, clrDimGray);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 105);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 110);
   return true;
}

int FP_StateGatePanelCountRallyRowsForSlot(const FP_StateGateSnapshot &snapshot, const int slot)
{
   int count = 0;
   for(int r=0; r<snapshot.rally_row_count; r++)
      if(snapshot.rally_rows[r].slot_index == slot)
         count++;
   return count;
}

int FP_StateGatePanelCountHookRowsForSlot(const FP_StateGateSnapshot &snapshot, const int slot)
{
   int count = 0;
   for(int h=0; h<snapshot.hook_row_count; h++)
      if(snapshot.hook_rows[h].slot_index == slot)
         count++;
   return count;
}

color FP_StateGatePanelTrackerColor(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available)
      return clrTomato;
   if(s.dirty)
      return clrLime;
   return clrSilver;
}

color FP_StateGatePanelRallyColor(const FP_StateGateRallyRow &r)
{
   if(r.latest_established_f != FP_STATE_GATE_RALLY_ESTABLISHED_NONE)
      return clrAqua;
   if(r.probable_next_f != FP_STATE_GATE_RALLY_PROBABLE_NONE)
      return clrKhaki;
   return clrSilver;
}

color FP_StateGatePanelHookColor(const FP_StateGateHookRow &h)
{
   if(StringFind(h.polarity, "POSITIVE") >= 0)
      return clrLime;
   if(StringFind(h.polarity, "NEGATIVE") >= 0)
      return clrOrange;
   return clrSilver;
}

string FP_StateGatePanelHeaderLabel(const FP_StateGateSnapshot &snapshot)
{
   string label = "State Gate";
   if(snapshot.symbol != "")
      label += " | " + snapshot.symbol;
   label += " | dirty=" + IntegerToString(snapshot.dirty_timeframes) + "/" + IntegerToString(snapshot.timeframe_count);
   label += " | rally=" + IntegerToString(snapshot.rally_row_count);
   label += " | hook=" + IntegerToString(snapshot.hook_row_count);
   return label;
}

string FP_StateGatePanelSlotHeaderLine(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "[" + s.timeframe_label + "] ";
   line += FP_StateGateDirtyLabel(s);
   line += " | R=" + IntegerToString(s.rally_row_count);
   line += " H=" + IntegerToString(s.hook_row_count);
   if(s.latest_established_f_summary != "")
      line += " | " + s.latest_established_f_summary;
   return line;
}

string FP_StateGatePanelTrackerLine(const FP_StateGateConfig &cfg,
                                    const FP_StateGateTimeframeState &s)
{
   string line = "    T | " + FP_StateGateDirtyLabel(s);
   if(cfg.panel_show_closed_bar)
   {
      line += " | closed=" + FP_StateGateClosedBarTimeLabel(s.last_closed_bar_time);
      line += " | close=" + FP_StateGateCloseLabel(s.last_closed_bar_close);
   }
   line += " | updates=" + IntegerToString(s.update_count);
   return line;
}

string FP_StateGatePanelCountsLine(const FP_StateGateTimeframeState &s)
{
   return "    C | rally=" + IntegerToString(s.rally_row_count) + " | hook=" + IntegerToString(s.hook_row_count) + " | extreme=" + IntegerToString(s.extreme_candidate_row_count) + " | mtf=" + IntegerToString(s.mtf_alignment_row_count) + " | idea=" + IntegerToString(s.entry_idea_row_count) + " | decision=" + IntegerToString(s.entry_decision_row_count) + " | paper=" + IntegerToString(s.paper_ledger_row_count) + " | life=" + IntegerToString(s.paper_lifecycle_row_count) + " | result=" + IntegerToString(s.paper_result_row_count) + " | regime=" + IntegerToString(s.paper_regime_row_count);
}

string FP_StateGatePanelContractLine(const FP_StateGateConfig &cfg,
                                     const FP_StateGateTimeframeState &s,
                                     const int text_limit)
{
   string line = "    K | " + s.entry_bridge_readiness;
   line += " | " + s.candidate_extreme_status;
   line += " | " + s.candidate_direction;
   if(!cfg.panel_compact_mode)
      line += " | key=" + s.entry_bridge_key;
   else
      line += " | key=" + FP_StateGatePanelClip(s.entry_bridge_key, MathMax(24, text_limit - 40));
   return FP_StateGatePanelClip(line, text_limit);
}

string FP_StateGatePanelRallyPreviewLine(const FP_StateGateConfig &cfg,
                                         const int preview_index,
                                         const FP_StateGateRallyRow &r)
{
   string label = r.label;
   if(cfg.panel_compact_mode)
   {
      label = r.timeframe_label + " | " + FP_DirectionName(r.direction);
      if(r.latest_established_f != FP_STATE_GATE_RALLY_ESTABLISHED_NONE)
         label += " | " + r.latest_established_f;
      else if(r.probable_next_f != FP_STATE_GATE_RALLY_PROBABLE_NONE)
         label += " | " + r.probable_next_f;
      else if(r.flag_stage != "")
         label += " | " + r.flag_stage;
      else if(r.post_flag_stage != "")
         label += " | " + r.post_flag_stage;
      if(cfg.show_scale_l)
         label += " | L" + IntegerToString(r.scale_L);
      if(cfg.show_ids)
         label += " | E#" + IntegerToString(r.source_event_id);
   }
   return "      R" + IntegerToString(preview_index+1) + " | " + label;
}

string FP_StateGatePanelHookPreviewLine(const FP_StateGateConfig &cfg,
                                        const int preview_index,
                                        const FP_StateGateHookRow &h)
{
   string label = h.label;
   if(cfg.panel_compact_mode)
   {
      label = h.timeframe_label;
      if(h.polarity != "")
         label += " | " + h.polarity;
      else
         label += " | " + FP_DirectionName(h.direction);
      label += " | N" + IntegerToString(h.current_node_number);
      if(cfg.show_scale_l)
         label += " | L" + IntegerToString(h.scale_L);
      if(h.latest_high_node_id >= 0)
         label += " | H#" + IntegerToString(h.latest_high_node_id);
      if(h.latest_low_node_id >= 0)
         label += " | L#" + IntegerToString(h.latest_low_node_id);
      if(cfg.show_ids)
         label += " | Hk#" + IntegerToString(h.source_hook_id);
   }
   return "      H" + IntegerToString(preview_index+1) + " | " + label;
}

string FP_StateGatePanelDiagnosticsLine(const FP_StateGateConfig &cfg,
                                        const FP_StateGateSnapshot &snapshot)
{
   string s = "diag | ";
   s += FP_StateGatePanelPlacementKey(cfg);
   s += " | serial=" + IntegerToString(snapshot.update_serial);
   s += " | available=" + IntegerToString(snapshot.available_timeframes);
   s += " | no_data=" + IntegerToString(snapshot.unavailable_timeframes);
   return s;
}

int FP_StateGatePanelSlotRowBudget(const FP_StateGateConfig &cfg,
                                   const FP_StateGateSnapshot &snapshot,
                                   const int slot)
{
   if(g_fp_state_gate_slot_collapsed[slot])
      return 1;

   int rows = 2; // slot header + tracker
   if(cfg.panel_show_row_counts)
      rows++;
   if(cfg.panel_show_contract_key)
      rows++;
   rows++; // extreme candidate map
   rows++; // mtf alignment map
   rows++; // entry geometry readiness
   rows++; // entry idea layer
   rows++; // entry decision dry run
   rows++; // paper execution ledger
   rows++; // paper lifecycle tracking
   rows++; // paper result metrics
   rows++; // paper regime attribution

   rows++; // rally header
   if(!g_fp_state_gate_slot_rally_collapsed[slot])
   {
      int rlimit = FP_StateGatePanelRallyPreviewLimit(cfg);
      int rally_total = FP_StateGatePanelCountRallyRowsForSlot(snapshot, slot);
      rows += (rally_total < rlimit ? rally_total : rlimit);
      if(rally_total > rlimit && rlimit > 0)
         rows++;
   }

   rows++; // hook header
   if(!g_fp_state_gate_slot_hook_collapsed[slot])
   {
      int hlimit = FP_StateGatePanelHookPreviewLimit(cfg);
      int hook_total = FP_StateGatePanelCountHookRowsForSlot(snapshot, slot);
      rows += (hook_total < hlimit ? hook_total : hlimit);
      if(hook_total > hlimit && hlimit > 0)
         rows++;
   }

   rows++; // spacer
   return rows;
}

void FP_StateGatePanelDraw(const FP_StateGateConfig &cfg,
                           const FP_StateGateSnapshot &snapshot,
                           const bool minimized,
                           FP_StateGateReport &report)
{
   if(!cfg.panel_enabled)
      return;

   FP_StateGateEnsurePanelState();
   report.objects_deleted += FP_StateGatePanelCleanup(cfg);

   int width = MathMax(560, cfg.panel_width);
   int font_size = MathMax(7, cfg.panel_font_size);
   int text_limit = FP_StateGatePanelTextLimit(width, font_size);
   int row_h = MathMax(14, font_size + 6);
   int title_h = 22;

   int rows = 1;
   if(!minimized)
   {
      rows = 2;
      if(cfg.panel_show_diagnostics)
         rows++;
      rows++; // paper portfolio aggregate metrics
      for(int i=0; i<snapshot.timeframe_count; i++)
         rows += FP_StateGatePanelSlotRowBudget(cfg, snapshot, i);
   }

   int height = title_h + rows * row_h + 8;
   if(minimized)
      height = title_h + 8;

   int x = cfg.panel_x;
   int y = cfg.panel_y;

   FP_StateGateCreateRect(cfg, "BG", x, y, width, height, clrDarkSlateGray, clrWhite, report);
   FP_StateGateCreateRect(cfg, "TITLE_BG", x, y, width, title_h, clrNavy, clrWhite, report);
   FP_StateGateCreateLabel(cfg, "TITLE", x + 8, y + 4, FP_StateGatePanelClip(FP_StateGatePanelHeaderLabel(snapshot), text_limit), clrWhite, font_size, report);
   FP_StateGateCreateButton(cfg, "MINBTN", x + width - 24, y + 3, 18, 16, (minimized ? "+" : "-"), report);

   if(minimized)
   {
      ChartRedraw(0);
      return;
   }

   int cursor_y = y + title_h + 4;

   if(cfg.panel_show_diagnostics)
   {
      FP_StateGateCreateLabel(cfg, "DIAGNOSTICS", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(FP_StateGatePanelDiagnosticsLine(cfg, snapshot), text_limit),
                              clrWhite, font_size, report);
      cursor_y += row_h;
   }

   string portfolio_line = "Portfolio | " + snapshot.paper_portfolio_status + " | " + snapshot.paper_portfolio_distribution + " | net=" + DoubleToString(snapshot.paper_portfolio_net_delta, 5) + " | avgR=" + DoubleToString(snapshot.paper_portfolio_avg_R, 3);
   FP_StateGateCreateLabel(cfg, "PAPER_PORTFOLIO", x + 10, cursor_y + 2,
                           FP_StateGatePanelClip(portfolio_line, text_limit),
                           clrGold, font_size, report);
   cursor_y += row_h;

   string regime_global_line = "Regime | rows=" + IntegerToString(snapshot.paper_regime_row_count) + " | paper attribution | real execution=false";
   FP_StateGateCreateLabel(cfg, "PAPER_REGIME_GLOBAL", x + 10, cursor_y + 2,
                           FP_StateGatePanelClip(regime_global_line, text_limit),
                           clrGold, font_size, report);
   cursor_y += row_h;

   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      FP_StateGateTimeframeState s = snapshot.tf_states[i];
      string suffix = "S" + IntegerToString(i) + "_";
      color slot_color = FP_StateGatePanelTrackerColor(s);

      // Slot header
      FP_StateGateCreateRect(cfg, suffix + "HDR_BG", x + 4, cursor_y, width - 8, row_h, clrDarkSlateGray, clrDimGray, report);
      FP_StateGateCreateLabel(cfg, suffix + "HDR", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(FP_StateGatePanelSlotHeaderLine(snapshot, i), text_limit - 8),
                              slot_color, font_size, report);
      int btn_y = cursor_y + 1;
      int btn_x = x + width - 22;
      FP_StateGateCreateButton(cfg, suffix + "SLOTBTN", btn_x, btn_y, 18, 15, (g_fp_state_gate_slot_collapsed[i] ? "+" : "-"), report);
      if(!g_fp_state_gate_slot_collapsed[i])
      {
         FP_StateGateCreateButton(cfg, suffix + "RBTN", btn_x - 22, btn_y, 18, 15, (g_fp_state_gate_slot_rally_collapsed[i] ? "R+" : "R-"), report);
         FP_StateGateCreateButton(cfg, suffix + "HBTN", btn_x - 44, btn_y, 18, 15, (g_fp_state_gate_slot_hook_collapsed[i] ? "H+" : "H-"), report);
      }
      cursor_y += row_h;

      if(g_fp_state_gate_slot_collapsed[i])
         continue;

      // Tracker
      FP_StateGateCreateLabel(cfg, suffix + "TRACK", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(FP_StateGatePanelTrackerLine(cfg, s), text_limit),
                              FP_StateGatePanelTrackerColor(s), font_size, report);
      cursor_y += row_h;

      if(cfg.panel_show_row_counts)
      {
         FP_StateGateCreateLabel(cfg, suffix + "COUNTS", x + 10, cursor_y + 2,
                                 FP_StateGatePanelClip(FP_StateGatePanelCountsLine(s), text_limit),
                                 clrSilver, font_size, report);
         cursor_y += row_h;
      }

      if(cfg.panel_show_contract_key)
      {
         FP_StateGateCreateLabel(cfg, suffix + "CONTRACT", x + 10, cursor_y + 2,
                                 FP_StateGatePanelContractLine(cfg, s, text_limit),
                                 clrDarkGray, font_size, report);
         cursor_y += row_h;
      }

      string extreme_line = "    XMap | " + s.extreme_map_status + " | " + s.primary_extreme_source + " | " + s.primary_extreme_side + " | " + s.primary_extreme_price_status;
      FP_StateGateCreateLabel(cfg, suffix + "EXTREME_MAP", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(extreme_line, text_limit),
                              clrKhaki, font_size, report);
      cursor_y += row_h;

      string mtf_line = "    MTF | " + s.mtf_alignment_status + " | parent=" + s.mtf_parent_timeframe + " | " + s.mtf_direction_relation + " | " + s.mtf_side_relation;
      FP_StateGateCreateLabel(cfg, suffix + "MTF_ALIGN", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(mtf_line, text_limit),
                              clrLightSteelBlue, font_size, report);
      cursor_y += row_h;

      string geometry_line = "    Geometry | " + s.geometry_readiness + " | entry=" + s.candidate_entry_price_status + " | dest=" + s.candidate_destination_price_status + " | R=" + s.potential_R_status;
      FP_StateGateCreateLabel(cfg, suffix + "GEOMETRY", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(geometry_line, text_limit),
                              clrPaleGreen, font_size, report);
      cursor_y += row_h;

      string idea_line = "    Idea | " + s.entry_idea_status + " | " + s.primary_entry_idea_family + " | " + s.entry_idea_readiness;
      FP_StateGateCreateLabel(cfg, suffix + "ENTRY_IDEA", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(idea_line, text_limit),
                              clrMagenta, font_size, report);
      cursor_y += row_h;

      string decision_line = "    Decision | " + s.entry_decision_status + " | " + s.entry_decision_direction + " | allowed=" + (s.entry_decision_allowed ? "true" : "false");
      FP_StateGateCreateLabel(cfg, suffix + "ENTRY_DECISION", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(decision_line, text_limit),
                              clrYellow, font_size, report);
      cursor_y += row_h;

      string paper_line = "    Paper | " + s.paper_ledger_record_status + " | " + s.paper_ledger_direction + " | " + s.paper_ledger_execution_status;
      FP_StateGateCreateLabel(cfg, suffix + "PAPER_LEDGER", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(paper_line, text_limit),
                              clrYellow, font_size, report);
      cursor_y += row_h;

      string lifecycle_line = "    Life | " + s.paper_lifecycle_path_state + " | " + s.paper_lifecycle_outcome + " | " + s.paper_lifecycle_execution_status;
      FP_StateGateCreateLabel(cfg, suffix + "PAPER_LIFECYCLE", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(lifecycle_line, text_limit),
                              clrLightGreen, font_size, report);
      cursor_y += row_h;

      string result_line = "    Result | " + s.paper_result_status + " | " + s.paper_result_bucket + " | d=" + DoubleToString(s.paper_result_price_delta, 5) + " | " + s.paper_result_r_status;
      FP_StateGateCreateLabel(cfg, suffix + "PAPER_RESULT", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(result_line, text_limit),
                              clrLightGreen, font_size, report);
      cursor_y += row_h;

      // Rally subsection
      int rally_total = FP_StateGatePanelCountRallyRowsForSlot(snapshot, i);
      string rally_head = "    Rally | total=" + IntegerToString(rally_total) + " | probable=" + FP_StateGatePanelClip(s.probable_next_f_summary, 36);
      FP_StateGateCreateLabel(cfg, suffix + "RHEAD", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(rally_head, text_limit),
                              clrAqua, font_size, report);
      cursor_y += row_h;
      if(!g_fp_state_gate_slot_rally_collapsed[i])
      {
         int rlimit = FP_StateGatePanelRallyPreviewLimit(cfg);
         int rally_seen = 0;
         for(int r=0; r<snapshot.rally_row_count && rally_seen < rlimit; r++)
         {
            if(snapshot.rally_rows[r].slot_index != i)
               continue;
            FP_StateGateCreateLabel(cfg, suffix + "R" + IntegerToString(rally_seen),
                                    x + 10, cursor_y + 2,
                                    FP_StateGatePanelClip(FP_StateGatePanelRallyPreviewLine(cfg, rally_seen, snapshot.rally_rows[r]), text_limit),
                                    FP_StateGatePanelRallyColor(snapshot.rally_rows[r]),
                                    font_size, report);
            cursor_y += row_h;
            rally_seen++;
         }
         if(rally_total > rlimit && rlimit > 0)
         {
            string more_r = "      R+ | " + IntegerToString(rally_total - rlimit) + " more Rally rows in CSV";
            FP_StateGateCreateLabel(cfg, suffix + "R_MORE", x + 10, cursor_y + 2,
                                    FP_StateGatePanelClip(more_r, text_limit),
                                    clrGray, font_size, report);
            cursor_y += row_h;
         }
      }

      // Hook subsection
      int hook_total = FP_StateGatePanelCountHookRowsForSlot(snapshot, i);
      string hook_head = "    Hook | total=" + IntegerToString(hook_total) + " | summary=" + FP_StateGatePanelClip(s.hook_summary, 36);
      FP_StateGateCreateLabel(cfg, suffix + "HHEAD", x + 10, cursor_y + 2,
                              FP_StateGatePanelClip(hook_head, text_limit),
                              clrOrange, font_size, report);
      cursor_y += row_h;
      if(!g_fp_state_gate_slot_hook_collapsed[i])
      {
         int hlimit = FP_StateGatePanelHookPreviewLimit(cfg);
         int hook_seen = 0;
         for(int h=0; h<snapshot.hook_row_count && hook_seen < hlimit; h++)
         {
            if(snapshot.hook_rows[h].slot_index != i)
               continue;
            FP_StateGateCreateLabel(cfg, suffix + "H" + IntegerToString(hook_seen),
                                    x + 10, cursor_y + 2,
                                    FP_StateGatePanelClip(FP_StateGatePanelHookPreviewLine(cfg, hook_seen, snapshot.hook_rows[h]), text_limit),
                                    FP_StateGatePanelHookColor(snapshot.hook_rows[h]),
                                    font_size, report);
            cursor_y += row_h;
            hook_seen++;
         }
         if(hook_total > hlimit && hlimit > 0)
         {
            string more_h = "      H+ | " + IntegerToString(hook_total - hlimit) + " more Hook rows in CSV";
            FP_StateGateCreateLabel(cfg, suffix + "H_MORE", x + 10, cursor_y + 2,
                                    FP_StateGatePanelClip(more_h, text_limit),
                                    clrGray, font_size, report);
            cursor_y += row_h;
         }
      }

      cursor_y += row_h / 2;
   }

   ChartRedraw(0);
}

bool FP_StateGatePanelHandleChartEvent(const FP_StateGateConfig &cfg,
                                       FP_StateGateRuntime &runtime,
                                       const int id,
                                       const string sparam)
{
   if(id != CHARTEVENT_OBJECT_CLICK)
      return false;

   FP_StateGateEnsurePanelState();

   string btn = FP_StateGateObjectName(cfg, "MINBTN");
   if(sparam == btn)
   {
      runtime.minimized = !runtime.minimized;
   }
   else
   {
      bool matched = false;
      for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
      {
         string suffix = "S" + IntegerToString(i) + "_";
         if(sparam == FP_StateGateObjectName(cfg, suffix + "SLOTBTN"))
         {
            g_fp_state_gate_slot_collapsed[i] = !g_fp_state_gate_slot_collapsed[i];
            matched = true;
            break;
         }
         if(sparam == FP_StateGateObjectName(cfg, suffix + "RBTN"))
         {
            g_fp_state_gate_slot_rally_collapsed[i] = !g_fp_state_gate_slot_rally_collapsed[i];
            matched = true;
            break;
         }
         if(sparam == FP_StateGateObjectName(cfg, suffix + "HBTN"))
         {
            g_fp_state_gate_slot_hook_collapsed[i] = !g_fp_state_gate_slot_hook_collapsed[i];
            matched = true;
            break;
         }
      }
      if(!matched)
         return false;
   }

   FP_StateGateReport report;
   FP_ResetStateGateReport(report);
   report.attempted = true;
   FP_StateGatePanelCleanup(cfg);
   FP_StateGatePanelDraw(cfg, runtime.snapshot, runtime.minimized, report);
   return true;
}

#endif // __FP_STATE_GATE_PANEL_MQH__
