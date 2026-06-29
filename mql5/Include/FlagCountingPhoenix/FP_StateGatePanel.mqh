#ifndef __FP_STATE_GATE_PANEL_MQH__
#define __FP_STATE_GATE_PANEL_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Panel
// ----------------------------------------------------------------------------
// Right-upper chart-object dashboard. It only renders State Gate snapshot data
// and owns only objects with the configured Level 19 prefix. Phase 4 makes the
// panel show projected Rally rows and Hook rows while preserving minimize.
// ============================================================================

string FP_StateGateObjectName(const FP_StateGateConfig &cfg, const string suffix)
{
   return cfg.object_prefix + suffix;
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
   ObjectSetInteger(0, name, OBJPROP_CORNER, cfg.panel_corner);
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
   ObjectSetInteger(0, name, OBJPROP_CORNER, cfg.panel_corner);
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
   ObjectSetInteger(0, name, OBJPROP_CORNER, cfg.panel_corner);
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

int FP_StateGatePanelSlotRowBudget(const FP_StateGateSnapshot &snapshot, const int slot)
{
   int rows = 4; // tracker, latest established F, probable next F, hook summary
   int rally_seen = 0;
   for(int r=0; r<snapshot.rally_row_count; r++)
      if(snapshot.rally_rows[r].slot_index == slot && rally_seen < 2)
         rally_seen++;
   int hook_seen = 0;
   for(int h=0; h<snapshot.hook_row_count; h++)
      if(snapshot.hook_rows[h].slot_index == slot && hook_seen < 2)
         hook_seen++;
   return rows + rally_seen + hook_seen;
}

string FP_StateGatePanelClip(const string text, const int max_len)
{
   if(StringLen(text) <= max_len) return text;
   return StringSubstr(text, 0, MathMax(0, max_len - 3)) + "...";
}

void FP_StateGatePanelDraw(const FP_StateGateConfig &cfg,
                           const FP_StateGateSnapshot &snapshot,
                           const bool minimized,
                           FP_StateGateReport &report)
{
   if(!cfg.panel_enabled) return;

   // The Level 19 panel is a live debug dashboard. Clean stale labels before
   // every redraw so row-count changes never leave old Rally/Hook labels on the
   // chart. Cleanup is prefix-isolated and never touches Phoenix renderer objects.
   report.objects_deleted += FP_StateGatePanelCleanup(cfg);

   int width = MathMax(560, cfg.panel_width);
   int font_size = MathMax(7, cfg.panel_font_size);
   int row_h = MathMax(14, font_size + 6);
   int title_h = 22;
   int rows = 1;
   if(!minimized)
   {
      rows = 1;
      for(int i=0; i<snapshot.timeframe_count; i++)
         rows += FP_StateGatePanelSlotRowBudget(snapshot, i);
   }
   int height = title_h + rows * row_h + 8;
   if(minimized) height = title_h + 6;

   FP_StateGateCreateRect(cfg, "BG", cfg.panel_x, cfg.panel_y, width, height, clrBlack, clrDimGray, report);
   FP_StateGateCreateRect(cfg, "TITLE_BG", cfg.panel_x, cfg.panel_y, width, title_h, clrMidnightBlue, clrDimGray, report);
   FP_StateGateCreateLabel(cfg, "TITLE", cfg.panel_x + 8, cfg.panel_y + 4, FP_StateGatePanelClip(FP_StateGateHeaderLabel(snapshot), 90), clrWhite, font_size, report);
   FP_StateGateCreateButton(cfg, "MINBTN", cfg.panel_x + width - 26, cfg.panel_y + 3, 20, 16, (minimized ? "+" : "-"), report);

   if(minimized)
   {
      ChartRedraw(0);
      return;
   }

   int y = cfg.panel_y + title_h + 6;
   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      string suffix = "TF_" + IntegerToString(i) + "_";
      string line1 = snapshot.tf_states[i].timeframe_label + " | " + FP_StateGateDirtyLabel(snapshot.tf_states[i]) + " | closed=" + FP_StateGateClosedBarTimeLabel(snapshot.tf_states[i].last_closed_bar_time) + " | close=" + FP_StateGateCloseLabel(snapshot.tf_states[i].last_closed_bar_close);
      string line2 = "  RALLY LATEST | " + snapshot.tf_states[i].latest_established_f_summary;
      string line3 = "  RALLY NEXT   | " + snapshot.tf_states[i].probable_next_f_summary;
      string line4 = "  HOOK TOP     | " + snapshot.tf_states[i].hook_summary;
      FP_StateGateCreateLabel(cfg, suffix + "A", cfg.panel_x + 8, y, FP_StateGatePanelClip(line1, 96), clrLightSteelBlue, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "B", cfg.panel_x + 8, y, FP_StateGatePanelClip(line2, 96), clrGainsboro, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "C", cfg.panel_x + 8, y, FP_StateGatePanelClip(line3, 96), clrGainsboro, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, suffix + "D", cfg.panel_x + 8, y, FP_StateGatePanelClip(line4, 96), clrPaleGreen, font_size, report);
      y += row_h;

      int rally_seen = 0;
      for(int r=0; r<snapshot.rally_row_count && rally_seen < 2; r++)
      {
         if(snapshot.rally_rows[r].slot_index != i) continue;
         string rline = "    R" + IntegerToString(rally_seen+1) + " | " + snapshot.rally_rows[r].label;
         FP_StateGateCreateLabel(cfg, suffix + "R" + IntegerToString(rally_seen), cfg.panel_x + 8, y, FP_StateGatePanelClip(rline, 96), clrSilver, font_size, report);
         y += row_h;
         rally_seen++;
      }

      int hook_seen = 0;
      for(int h=0; h<snapshot.hook_row_count && hook_seen < 2; h++)
      {
         if(snapshot.hook_rows[h].slot_index != i) continue;
         string hline = "    H" + IntegerToString(hook_seen+1) + " | " + snapshot.hook_rows[h].label;
         FP_StateGateCreateLabel(cfg, suffix + "H" + IntegerToString(hook_seen), cfg.panel_x + 8, y, FP_StateGatePanelClip(hline, 96), clrLightGreen, font_size, report);
         y += row_h;
         hook_seen++;
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
