#ifndef __FP_STATE_GATE_PANEL_MQH__
#define __FP_STATE_GATE_PANEL_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// Level 19 Clean Panel
// ----------------------------------------------------------------------------
// Disabled by default. If enabled, it uses its own dedicated prefix only.
// It never uses the renderer prefix and never deletes F/Hook/Node/chart objects.
// ============================================================================

int FP_L19PanelCleanup(const string prefix)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int deleted = 0;
   int total = ObjectsTotal(0, -1, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
      {
         if(ObjectDelete(0, name))
            deleted++;
      }
   }
   return deleted;
}

bool FP_L19PanelLabel(const FP_Level19StateGateConfig &cfg,
                      const string suffix,
                      const int x,
                      const int y,
                      const string text,
                      const color clr,
                      FP_Level19StateGateReport &report)
{
   string name = cfg.object_prefix + suffix;
   if(ObjectFind(0, name) < 0)
   {
      if(!ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0))
      {
         report.panel_object_errors++;
         return false;
      }
      report.panel_objects_created++;
   }

   ObjectSetInteger(0, name, OBJPROP_CORNER, cfg.panel_corner);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, 5);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, MathMax(7, cfg.panel_font_size));
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   return true;
}

void FP_L19PanelDraw(const FP_Level19StateGateConfig &cfg,
                     const FP_Level19StateGateSnapshot &s,
                     FP_Level19StateGateReport &report)
{
   if(!cfg.panel_enabled)
      return;

   report.panel_objects_deleted += FP_L19PanelCleanup(cfg.object_prefix);

   int x = MathMax(0, cfg.panel_x);
   int y = MathMax(0, cfg.panel_y);
   int row = MathMax(12, cfg.panel_font_size + 6);

   FP_L19PanelLabel(cfg, "L0_TITLE", x, y + row * 0,
                    "L19 StateGate | " + s.symbol + " | " + s.period_label + " | READ_ONLY",
                    clrWhite, report);
   FP_L19PanelLabel(cfg, "L1_STATUS", x, y + row * 1,
                    "status=" + s.state_status,
                    clrYellow, report);
   FP_L19PanelLabel(cfg, "L2_COUNTS", x, y + row * 2,
                    "bars=" + IntegerToString(s.bars) +
                    " events=" + IntegerToString(s.events_total) +
                    " hooks=" + IntegerToString(s.hooks_total) +
                    " nd=" + IntegerToString(s.nd_total),
                    clrAqua, report);
   FP_L19PanelLabel(cfg, "L3_F", x, y + row * 3,
                    "F1=" + IntegerToString(s.f1_total) +
                    " F2=" + IntegerToString(s.f2_total) +
                    " F3=" + IntegerToString(s.f3_total) +
                    " visible=" + IntegerToString(s.visible_events_total),
                    clrLime, report);
   FP_L19PanelLabel(cfg, "L4_RENDER", x, y + row * 4,
                    "render_attempted=" + FP_L19Bool(s.render_attempted) +
                    " render_ok=" + FP_L19Bool(s.render_ok) +
                    " errors=" + IntegerToString(s.render_object_errors),
                    clrSilver, report);
   FP_L19PanelLabel(cfg, "L5_CONTRACT", x, y + row * 5,
                    "NO_TOUCH renderer/F/Hook/Node/lines",
                    clrOrange, report);
}

#endif // __FP_STATE_GATE_PANEL_MQH__
