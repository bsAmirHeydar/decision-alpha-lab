#ifndef __FP_STATE_GATE_PANEL_MQH__
#define __FP_STATE_GATE_PANEL_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Panel
// ----------------------------------------------------------------------------
// Minimal chart-object dashboard shell.  It only renders State Gate snapshot
// data and owns only objects with the configured Level 19 prefix.
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

void FP_StateGatePanelDraw(const FP_StateGateConfig &cfg,
                           const FP_StateGateSnapshot &snapshot,
                           const bool minimized,
                           FP_StateGateReport &report)
{
   if(!cfg.panel_enabled) return;

   int width = MathMax(300, cfg.panel_width);
   int font_size = MathMax(7, cfg.panel_font_size);
   int row_h = MathMax(14, font_size + 6);
   int title_h = 22;
   int rows = 1;
   if(!minimized)
      rows = 1 + snapshot.timeframe_count * 3;
   int height = title_h + rows * row_h + 8;
   if(minimized) height = title_h + 6;

   FP_StateGateCreateRect(cfg, "BG", cfg.panel_x, cfg.panel_y, width, height, clrBlack, clrDimGray, report);
   FP_StateGateCreateRect(cfg, "TITLE_BG", cfg.panel_x, cfg.panel_y, width, title_h, clrMidnightBlue, clrDimGray, report);
   FP_StateGateCreateLabel(cfg, "TITLE", cfg.panel_x + 8, cfg.panel_y + 4, FP_StateGateHeaderLabel(snapshot), clrWhite, font_size, report);
   FP_StateGateCreateButton(cfg, "MINBTN", cfg.panel_x + width - 26, cfg.panel_y + 3, 20, 16, (minimized ? "+" : "-"), report);

   if(minimized)
   {
      ChartRedraw(0);
      return;
   }

   int y = cfg.panel_y + title_h + 6;
   for(int i=0; i<snapshot.timeframe_count; i++)
   {
      string line1 = snapshot.tf_states[i].timeframe_label + " | close_bar=" + FP_StateGateClosedBarTimeLabel(snapshot.tf_states[i].last_closed_bar_time);
      string line2 = "  RALLY | " + snapshot.tf_states[i].latest_established_f_summary + " | " + snapshot.tf_states[i].probable_next_f_summary;
      string line3 = "  HOOK  | " + snapshot.tf_states[i].hook_summary;
      FP_StateGateCreateLabel(cfg, "TF_" + IntegerToString(i) + "_A", cfg.panel_x + 8, y, line1, clrLightSteelBlue, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, "TF_" + IntegerToString(i) + "_B", cfg.panel_x + 8, y, line2, clrGainsboro, font_size, report);
      y += row_h;
      FP_StateGateCreateLabel(cfg, "TF_" + IntegerToString(i) + "_C", cfg.panel_x + 8, y, line3, clrGainsboro, font_size, report);
      y += row_h;
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
