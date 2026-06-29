#ifndef __FP_STATE_GATE_PANEL_MQH__
#define __FP_STATE_GATE_PANEL_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Panel
// ----------------------------------------------------------------------------
// Phase 5 polishes the right-upper dashboard: configurable row previews, compact
// labels, dirty/no-data colors, row-count hints, forced right-upper anchoring,
// and stable cleanup/redraw behavior. It only renders State Gate snapshot data.
// ============================================================================

string FP_StateGateObjectName(const FP_StateGateConfig &cfg, const string suffix)
{
   return cfg.object_prefix + suffix;
}

int FP_StateGatePanelCorner(const FP_StateGateConfig &cfg)
{
   if(cfg.panel_force_right_upper) return CORNER_RIGHT_UPPER;
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
   int safe_width = MathMax(240, width - 24);
   int char_px = MathMax(5, font_size + 1);
   int limit = safe_width / char_px;
   return FP_StateGateClampInt(limit, 42, 140);
}

int FP_StateGatePanelCleanup(const FP_StateGateConfig &cfg)
{
   int total = ObjectsTotal(0, -1, -1);
   int deleted = 0;
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, cfg.object_prefix) == 0)
      {
         if(ObjectDelete(0, name)) deleted++;
      }
   }
   return deleted;
}

bool FP_StateGateCreateRect(const FP_StateGateConfig &cfg,
                            const string suffix,
                            const int x,
                            const int y,
                            const int w,
                            const int h,
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
         report.reason = "panel_rect_create_failed";
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_XSIZE, w);
   ObjectSetInteger(0, name, OBJPROP_YSIZE, h);
   ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg);
   ObjectSetInteger(0, name, OBJPROP_COLOR, border);
   ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 90);
   return true;
}

bool FP_StateGateCreateLabel(const FP_StateGateConfig &cfg,
                             const string suffix,
                             const int x,
                             const int y,
                             const string text,
                             const color c,
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
         report.reason = "panel_label_create_failed";
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, MathMax(7, font_size));
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 100);
   return true;
}

bool FP_StateGateCreateButton(const FP_StateGateConfig &cfg,
                              const string suffix,
                              const int x,
                              const int y,
                              const int w,
                              const int h,
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
         report.reason = "panel_button_create_failed";
         return false;
      }
      report.objects_created++;
   }
   ObjectSetInteger(0, name, OBJPROP_CORNER, FP_StateGatePanelCorner(cfg));
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_XSIZE, w);
   ObjectSetInteger(0, name, OBJPROP_YSIZE, h);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, MathMax(7, cfg.panel_font_size));
   ObjectSetInteger(0, name, OBJPROP_COLOR, clrWhite);
   ObjectSetInteger(0, name, OBJPROP_BGCOLOR, clrDimGray);
   ObjectSetInteger(0, name, OBJPROP_BORDER_COLOR, clrGray);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 110);
   return true;
}

string FP_StateGatePanelClip(const string text, const int max_len)
{
   if(StringLen(text) <= max_len) return text;
   return StringSubstr(text, 0, MathMax(0, max_len - 3)) + "...";
}

color FP_StateGatePanelTfColor(const FP_StateGateTimeframeState &s)
{
   if(!s.closed_bar_available) return clrTomato;
   if(s.dirty) return clrLightSkyBlue;
   return clrLightSteelBlue;
}

color FP_StateGatePanelRallyColor(const FP_StateGateRallyRow &r)
{
   if(r.status == FP_STATE_GATE_ROW_PROJECTED) return clrSilver;
   if(r.status == FP_STATE_GATE_ROW_UNKNOWN) return clrTomato;
   return clrDimGray;
}

color FP_StateGatePanelHookColor(const FP_StateGateHookRow &h)
{
   if(h.status == FP_STATE_GATE_ROW_PROJECTED) return clrLightGreen;
   if(h.status == FP_STATE_GATE_ROW_UNKNOWN) return clrTomato;
   return clrDimGray;
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

int FP_StateGatePanelSlotRowBudget(const FP_StateGateConfig &cfg,
                                   const FP_StateGateSnapshot &snapshot,
                                   const int slot)
{
   int rows = 3; // tracker, latest/probable rally, hook summary
   if(cfg.panel_show_row_counts) rows++;
   int rlimit = FP_StateGatePanelRallyPreviewLimit(cfg);
   int hlimit = FP_StateGatePanelHookPreviewLimit(cfg);
   int rally_count = FP_StateGatePanelCountRallyRowsForSlot(snapshot, slot);
   int hook_count = FP_StateGatePanelCountHookRowsForSlot(snapshot, slot);
   rows += (rally_count < rlimit ? rally_count : rlimit);
   rows += (hook_count < hlimit ? hook_count : hlimit);
   if(rally_count > rlimit && rlimit > 0) rows++;
   if(hook_count > hlimit && hlimit > 0) rows++;
   return rows;
}

string FP_StateGatePanelTrackerLine(const FP_StateGateConfig &cfg,
                                    const FP_StateGateTimeframeState &s)
{
   string line = s.timeframe_label + " | " + FP_StateGateDirtyLabel(s);
   if(cfg.panel_show_closed_bar)
   {
      line += " | closed=" + FP_StateGateClosedBarTimeLabel(s.last_closed_bar_time);
      line += " | close=" + FP_StateGateCloseLabel(s.last_closed_bar_close);
   }
   line += " | updates=" + IntegerToString(s.update_count);
   if(!s.closed_bar_available) line += " | " + s.reason;
   return line;
}

string FP_StateGatePanelCountsLine(const FP_StateGateSnapshot &snapshot,
                                   const int slot)
{
   string line = "  rows | rally=" + IntegerToString(snapshot.tf_states[slot].rally_row_count);
   line += " hook=" + IntegerToString(snapshot.tf_states[slot].hook_row_count);
   line += " | status=" + snapshot.tf_states[slot].tracker_status;
   return line;
}

string FP_StateGatePanelRallyPreviewLine(const FP_StateGateConfig &cfg,
                                         const int preview_index,
                                         const FP_StateGateRallyRow &r)
{
   string label = r.label;
   if(cfg.panel_compact_mode)
   {
      label = r.timeframe_label + " " + FP_LevelName(r.f_level);
      label += " | " + FP_DirectionName(r.direction);
      if(r.latest_established_f != FP_STATE_GATE_RALLY_ESTABLISHED_NONE)
         label += " | " + r.latest_established_f;
      else if(r.probable_next_f != FP_STATE_GATE_RALLY_PROBABLE_NONE)
         label += " | " + r.probable_next_f;
      else
         label += " | " + r.flag_stage;
      if(cfg.show_scale_l) label += " | L" + IntegerToString(r.scale_L);
      if(cfg.show_ids) label += " | E#" + IntegerToString(r.source_event_id);
   }
   return "    R" + IntegerToString(preview_index+1) + " | " + label;
}

string FP_StateGatePanelHookPreviewLine(const FP_StateGateConfig &cfg,
                                        const int preview_index,
                                        const FP_StateGateHookRow &h)
{
   string label = h.label;
   if(cfg.panel_compact_mode)
   {
      label = h.timeframe_label + " Hook";
      if(cfg.show_scale_l) label += " | L" + IntegerToString(h.scale_L);
      label += " | " + h.polarity;
      label += " | N" + IntegerToString(h.current_node_number);
      if(h.latest_high_node_id >= 0) label += " | H#" + IntegerToString(h.latest_high_node_id);
      if(h.latest_low_node_id >= 0) label += " | L#" + IntegerToString(h.latest_low_node_id);
      if(cfg.show_ids) label += " | Hk#" + IntegerToString(h.source_hook_id);
   }
   return "    H" + IntegerToString(preview_index+1) + " | " + label;
}

void FP_StateGatePanelDrawSeparator(const FP_StateGateConfig &cfg,
                                    const string suffix,
                                    const int x,
                                    const int y,
                                    const int width,
                                    FP_StateGateReport &report)
{
   FP_StateGateCreateRect(cfg, suffix, x, y + 5, width, 1, clrDimGray, clrDimGray, report);
}

void FP_StateGatePanelDraw(const FP_StateGateConfig &cfg,
                           const FP_StateGateSnapshot &snapshot,
                           const bool minimized,
                           FP_StateGateReport &report)
{
   if(!cfg.panel_enabled) return;

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
      for(int i=0; i<snapshot.timeframe_count; i++)
         rows += FP_StateGatePanelSlotRowBudget(cfg, snapshot, i) + 1;
   }
   int height = title_h + rows * row_h + 8;
   if(minimized) height = title_h + 8;

   FP_StateGateCreateRect(cfg, "BG", cfg.panel_x, cfg.panel_y, width, height, clrBlack, clrDimGray, report);
   FP_StateGateCreateRect(cfg, "TITLE_BG", cfg.panel_x, cfg.panel_y, width, title_h, clrMidnightBlue, clrDimGray, report);
   FP_StateGateCreateLabel(cfg, "TITLE", cfg.panel_x + 8, cfg.panel_y + 4, FP_StateGatePanelClip(FP_StateGateHeaderLabel(snapshot), text_limit), clrWhite, font_size, report);
   FP_StateGateCreateButton(cfg, "MINBTN", cfg.panel_x + width - 26, cfg.panel_y + 3, 20, 16, (minimized ? "+" : "-"), report);

   if(minimized)
   {
      ChartRedraw(0);
      return;
   }

   int y = cfg.panel_y + title_h + 6;
   string overview = "symbol=" + snapshot.symbol;
   overview += " | dirty=" + IntegerToString(snapshot.dirty_timeframes);
   overview += "/" + IntegerToString(snapshot.timeframe_count);
   overview += " | rally=" + IntegerToString(snapshot.rally_row_count);
   overview += " | hook=" + IntegerToString(snapshot.hook_row_count);
   overview += " | generated=" + TimeToString(snapshot.generated_at, TIME_DATE|TIME_MINUTES);
   FP_StateGateCreateLabel(cfg, "OVERVIEW", cfg.panel_x + 8, y, FP_StateGatePanelClip(overview, text_limit), clrGainsboro, font_size, report);
   y += row_h;

   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      string suffix = "TF_" + IntegerToString(i) + "_";
      FP_StateGatePanelDrawSeparator(cfg, suffix + "SEP", cfg.panel_x + 8, y, width - 16, report);
      y += row_h;

      string line1 = FP_StateGatePanelTrackerLine(cfg, snapshot.tf_states[i]);
      string line2 = "  RALLY LATEST | " + snapshot.tf_states[i].latest_established_f_summary;
      string line3 = "  RALLY NEXT   | " + snapshot.tf_states[i].probable_next_f_summary;
      string line4 = "  HOOK TOP     | " + snapshot.tf_states[i].hook_summary;
      FP_StateGateCreateLabel(cfg, suffix + "A", cfg.panel_x + 8, y, FP_StateGatePanelClip(line1, text_limit), FP_StateGatePanelTfColor(snapshot.tf_states[i]), font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "B", cfg.panel_x + 8, y, FP_StateGatePanelClip(line2, text_limit), clrGainsboro, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "C", cfg.panel_x + 8, y, FP_StateGatePanelClip(line3, text_limit), clrGainsboro, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "D", cfg.panel_x + 8, y, FP_StateGatePanelClip(line4, text_limit), clrPaleGreen, font_size, report);
      y += row_h;

      if(cfg.panel_show_row_counts)
      {
         FP_StateGateCreateLabel(cfg, suffix + "CNT", cfg.panel_x + 8, y, FP_StateGatePanelClip(FP_StateGatePanelCountsLine(snapshot, i), text_limit), clrGray, font_size, report);
         y += row_h;
      }

      int rlimit = FP_StateGatePanelRallyPreviewLimit(cfg);
      int rally_seen = 0;
      int rally_total = FP_StateGatePanelCountRallyRowsForSlot(snapshot, i);
      for(int r=0; r<snapshot.rally_row_count && rally_seen < rlimit; r++)
      {
         if(snapshot.rally_rows[r].slot_index != i) continue;
         string rline = FP_StateGatePanelRallyPreviewLine(cfg, rally_seen, snapshot.rally_rows[r]);
         FP_StateGateCreateLabel(cfg, suffix + "R" + IntegerToString(rally_seen), cfg.panel_x + 8, y, FP_StateGatePanelClip(rline, text_limit), FP_StateGatePanelRallyColor(snapshot.rally_rows[r]), font_size, report);
         y += row_h;
         rally_seen++;
      }
      if(rally_total > rlimit && rlimit > 0)
      {
         string more_r = "    R+ | " + IntegerToString(rally_total - rlimit) + " more Rally rows in CSV";
         FP_StateGateCreateLabel(cfg, suffix + "R_MORE", cfg.panel_x + 8, y, more_r, clrGray, font_size, report);
         y += row_h;
      }

      int hlimit = FP_StateGatePanelHookPreviewLimit(cfg);
      int hook_seen = 0;
      int hook_total = FP_StateGatePanelCountHookRowsForSlot(snapshot, i);
      for(int h=0; h<snapshot.hook_row_count && hook_seen < hlimit; h++)
      {
         if(snapshot.hook_rows[h].slot_index != i) continue;
         string hline = FP_StateGatePanelHookPreviewLine(cfg, hook_seen, snapshot.hook_rows[h]);
         FP_StateGateCreateLabel(cfg, suffix + "H" + IntegerToString(hook_seen), cfg.panel_x + 8, y, FP_StateGatePanelClip(hline, text_limit), FP_StateGatePanelHookColor(snapshot.hook_rows[h]), font_size, report);
         y += row_h;
         hook_seen++;
      }
      if(hook_total > hlimit && hlimit > 0)
      {
         string more_h = "    H+ | " + IntegerToString(hook_total - hlimit) + " more Hook rows in CSV";
         FP_StateGateCreateLabel(cfg, suffix + "H_MORE", cfg.panel_x + 8, y, more_h, clrGray, font_size, report);
         y += row_h;
      }
   }
   ChartRedraw(0);
}

bool FP_StateGatePanelHandleChartEvent(const FP_StateGateConfig &cfg,
                                       FP_StateGateRuntime &runtime,
                                       const int id,
                                       const string sparam)
{
   if(id != CHARTEVENT_OBJECT_CLICK) return false;
   string btn = FP_StateGateObjectName(cfg, "MINBTN");
   if(sparam != btn) return false;
   runtime.minimized = !runtime.minimized;
   FP_StateGateReport report;
   FP_ResetStateGateReport(report);
   report.attempted = true;
   FP_StateGatePanelCleanup(cfg);
   FP_StateGatePanelDraw(cfg, runtime.snapshot, runtime.minimized, report);
   return true;
}

#endif // __FP_STATE_GATE_PANEL_MQH__
