#ifndef __FP_HOOK_PHASE05_VISUAL_MQH__
#define __FP_HOOK_PHASE05_VISUAL_MQH__
#property strict

#include "FP_HookPhase05Rules.mqh"

int FP_HookPhase05DeleteObjects(const string prefix)
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

color FP_HookP05TypeColor(const FP_HookPhase05Config &cfg,
                          const FP_HookPhase05HookType t)
{
   if(t == FP_HOOK_P05_TYPE_A) return cfg.type_a_color;
   if(t == FP_HOOK_P05_TYPE_B) return cfg.type_b_color;
   if(t == FP_HOOK_P05_TYPE_C) return cfg.type_c_color;
   return cfg.insufficient_color;
}

string FP_HookP05BaseName(const FP_HookPhase05Config &cfg,
                          const FP_HookPhase05Record &record)
{
   string name = cfg.object_prefix;
   name += FP_HookP02DirectionName(record.p04.p03.sequence.direction);
   name += "_L" + IntegerToString(record.p04.p03.sequence.scale_l);
   name += "_S" + IntegerToString(record.p04.p03.sequence.sequence_id);
   name += "_O" + IntegerToString(record.p04.p03.sequence.origin_node_id);
   return name;
}

bool FP_HookP05CreateText(const string name,
                          const datetime t,
                          const double price,
                          const string text,
                          const color c,
                          const int font_size,
                          FP_HookPhase05Report &report)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, price))
      return false;

   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   report.objects_created++;
   return true;
}

bool FP_HookP05CreateArrow(const string name,
                           const datetime t,
                           const double price,
                           const color c,
                           const int arrow_code,
                           const int width,
                           FP_HookPhase05Report &report)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_ARROW, 0, t, price))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, arrow_code);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   report.objects_created++;
   return true;
}

bool FP_HookP05CreateTrend(const string name,
                           const datetime t1,
                           const double p1,
                           const datetime t2,
                           const double p2,
                           const color c,
                           const int width,
                           const ENUM_LINE_STYLE style,
                           FP_HookPhase05Report &report)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   report.objects_created++;
   return true;
}

bool FP_HookP05DrawOneRecord(const FP_HookPhase05Config &cfg,
                             const FP_HookPhase05Record &record,
                             FP_HookPhase05Report &report)
{
   if(!record.valid)
      return false;

   string base = FP_HookP05BaseName(cfg, record);
   FP_HookPhase02Sequence seq = record.p04.p03.sequence;
   FP_HookPhase05Classification c = record.classification;
   color type_color = FP_HookP05TypeColor(cfg, c.hook_type);

   datetime anchor_time = seq.origin_time;
   double anchor_price = seq.origin_price;

   if(c.third_y_time > 0)
   {
      anchor_time = c.third_y_time;
      anchor_price = c.third_y_price;
   }
   else if(c.y12_time > 0)
   {
      anchor_time = c.y12_time;
      anchor_price = c.y12_price;
   }

   if(cfg.draw_type_anchor)
   {
      int arrow_code = 108;
      if(c.hook_type == FP_HOOK_P05_TYPE_A) arrow_code = 110;
      else if(c.hook_type == FP_HOOK_P05_TYPE_B) arrow_code = 108;
      else if(c.hook_type == FP_HOOK_P05_TYPE_C) arrow_code = 159;

      FP_HookP05CreateArrow(base + "_TYPE_ANCHOR",
                            anchor_time, anchor_price,
                            type_color, arrow_code,
                            cfg.marker_width + 1, report);
   }

   if(cfg.draw_type_label)
   {
      string txt = "HOOK " + FP_HookP05ShortTypeName(c.hook_type) +
                   " " + FP_HookP02DirectionName(seq.direction) +
                   " L" + IntegerToString(seq.scale_l) +
                   " S" + IntegerToString(seq.sequence_id) +
                   " conf=" + DoubleToString(c.confidence_score, 2);

      FP_HookP05CreateText(base + "_TYPE_LABEL",
                           anchor_time, anchor_price,
                           txt, type_color,
                           cfg.label_font_size, report);
   }

   if(cfg.draw_type_comparison_lines)
   {
      if(c.has_y01 && c.has_y12)
      {
         FP_HookP05CreateTrend(base + "_CMP_Y01_Y12",
                               c.y01_time, c.y01_price,
                               c.y12_time, c.y12_price,
                               cfg.comparison_color, cfg.line_width,
                               STYLE_DOT, report);
      }

      if(c.y12_time > 0 && c.third_y_time > 0)
      {
         FP_HookP05CreateTrend(base + "_CMP_Y12_THIRD",
                               c.y12_time, c.y12_price,
                               c.third_y_time, c.third_y_price,
                               cfg.comparison_color, cfg.line_width,
                               STYLE_DOT, report);
      }
   }

   if(cfg.draw_labels)
   {
      string logic_txt = "P05 first=" + FP_HookP05BoolName(c.condition_first) +
                         " second=" + FP_HookP05BoolName(c.condition_second) +
                         " " + c.reason;

      FP_HookP05CreateText(base + "_LOGIC_LABEL",
                           seq.origin_time, seq.origin_price,
                           logic_txt, cfg.label_color,
                           cfg.label_font_size, report);
   }

   return true;
}

int FP_HookP05DrawRecords(const FP_HookPhase05Config &cfg,
                          const FP_HookPhase05Record &records[],
                          FP_HookPhase05Report &report)
{
   report.objects_deleted += FP_HookPhase05DeleteObjects(cfg.object_prefix);

   int n = ArraySize(records);
   int max_draw = cfg.max_sequences_to_draw;
   if(max_draw <= 0 || max_draw > n)
      max_draw = n;

   int start = n - max_draw;
   if(start < 0)
      start = 0;

   int drawn = 0;
   for(int i=start; i<n; i++)
   {
      if(FP_HookP05DrawOneRecord(cfg, records[i], report))
         drawn++;
   }

   report.records_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE05_VISUAL_MQH__
