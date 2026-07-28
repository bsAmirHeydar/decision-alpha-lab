#ifndef __FP_HOOK_PHASE09_VISUAL_MQH__
#define __FP_HOOK_PHASE09_VISUAL_MQH__
#property strict

#include "FP_HookPhase09Rules.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

int FP_HookP09DeleteObjectsByPrefix(const string prefix)
{
   return AL_UC04DeleteObjectsByPrefix(0, prefix);
}

color FP_HookP09PanelStatusColor(const FP_HookPhase09Config &cfg,
                                 const FP_HookPhase09Report &report)
{
   if(report.blocker_count > 0 || !report.ok)
      return cfg.panel_blocker_color;
   if(report.warning_count > 0)
      return cfg.panel_warning_color;
   return cfg.panel_ok_color;
}

string FP_HookP09PanelText(const FP_HookPhase09Report &report)
{
   string text = "NDS Hook P09 Smoke | " + report.status;
   text += " | profile=" + FP_HookP07ViewProfileName(report.view_profile);
   text += " | scenarios=" + IntegerToString(report.scenarios_passed) + "/" + IntegerToString(report.scenarios_required);
   text += " | objects=" + IntegerToString(report.chart_hook_objects_seen);
   text += " | blockers=" + IntegerToString(report.blocker_count);
   text += " | warnings=" + IntegerToString(report.warning_count);
   return text;
}

bool FP_HookP09DrawPanel(const FP_HookPhase09Config &cfg,
                         FP_HookPhase09Report &report)
{
   if(!cfg.draw_panel)
      return true;

   if(cfg.clean_p09_objects_before_draw)
      report.p09_objects_deleted += FP_HookP09DeleteObjectsByPrefix(cfg.object_prefix);

   string name = cfg.object_prefix + "SMOKE_STATUS";
   if(!ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0))
   {
      if(ObjectFind(0, name) < 0)
      {
         report.file_errors++;
         report.reason = "HOOK_P09_PANEL_CREATE_FAILED";
         return false;
      }
   }

   ObjectSetInteger(0, name, OBJPROP_CORNER, cfg.panel_corner);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, cfg.panel_x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, cfg.panel_y);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, cfg.panel_font_size);
   ObjectSetInteger(0, name, OBJPROP_COLOR, FP_HookP09PanelStatusColor(cfg, report));
   ObjectSetString(0, name, OBJPROP_TEXT, FP_HookP09PanelText(report));
   report.p09_objects_created++;
   return true;
}

#endif // __FP_HOOK_PHASE09_VISUAL_MQH__
