#ifndef __FP_HOOK_PHASE01_VISUAL_MQH__
#define __FP_HOOK_PHASE01_VISUAL_MQH__
#property strict

#include "FP_HookPhase01Rules.mqh"

int FP_HookPhase01DeleteObjects(const string prefix)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int deleted = 0;
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
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

string FP_HookP01ObjectName(const FP_HookPhase01Config &cfg,
                            const FP_HookPhase01Node &node,
                            const string suffix)
{
   string s = cfg.object_prefix;
   s += FP_HookP01NodeTypeName(node.node_type);
   s += "_L" + IntegerToString(node.scale_l);
   s += "_B" + IntegerToString(node.bar_index);
   s += "_N" + IntegerToString(node.node_id);
   s += suffix;
   return s;
}

bool FP_HookP01DrawOneNode(const FP_HookPhase01Config &cfg,
                           const FP_HookPhase01Node &node,
                           FP_HookPhase01Report &report)
{
   string name = FP_HookP01ObjectName(cfg, node, "_MARK");
   ObjectDelete(0, name);

   if(!ObjectCreate(0, name, OBJ_ARROW, 0, node.bar_time, node.price))
      return false;

   color c = (node.node_type == FP_HOOK_P01_NODE_PEAK ? cfg.peak_color : cfg.valley_color);
   int arrow_code = (node.node_type == FP_HOOK_P01_NODE_PEAK ? 234 : 233);

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, cfg.marker_width);
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, arrow_code);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   report.objects_created++;

   if(cfg.draw_labels)
   {
      string label_name = FP_HookP01ObjectName(cfg, node, "_LABEL");
      ObjectDelete(0, label_name);
      if(ObjectCreate(0, label_name, OBJ_TEXT, 0, node.bar_time, node.price))
      {
         string label = "H01 " + FP_HookP01NodeTypeName(node.node_type) + " L" + IntegerToString(node.scale_l);
         ObjectSetString(0, label_name, OBJPROP_TEXT, label);
         ObjectSetInteger(0, label_name, OBJPROP_COLOR, cfg.label_color);
         ObjectSetInteger(0, label_name, OBJPROP_FONTSIZE, cfg.label_font_size);
         ObjectSetInteger(0, label_name, OBJPROP_BACK, false);
         ObjectSetInteger(0, label_name, OBJPROP_SELECTABLE, false);
         ObjectSetInteger(0, label_name, OBJPROP_HIDDEN, true);
         report.objects_created++;
      }
   }

   return true;
}

int FP_HookP01DrawNodes(const FP_HookPhase01Config &cfg,
                        const FP_HookPhase01Node &nodes[],
                        FP_HookPhase01Report &report)
{
   if(!cfg.draw_nodes)
      return 0;

   report.objects_deleted += FP_HookPhase01DeleteObjects(cfg.object_prefix);

   int n = ArraySize(nodes);
   int max_draw = cfg.max_nodes_to_draw;
   if(max_draw <= 0 || max_draw > n)
      max_draw = n;

   int start = n - max_draw;
   if(start < 0)
      start = 0;

   int drawn = 0;
   for(int i=start; i<n; i++)
   {
      if(FP_HookP01DrawOneNode(cfg, nodes[i], report))
         drawn++;
   }

   report.nodes_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE01_VISUAL_MQH__
