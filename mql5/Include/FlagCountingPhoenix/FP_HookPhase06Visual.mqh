#ifndef __FP_HOOK_PHASE06_VISUAL_MQH__
#define __FP_HOOK_PHASE06_VISUAL_MQH__
#property strict

#include "FP_HookPhase06Rules.mqh"

int FP_HookPhase06DeleteObjects(const string prefix)
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

string FP_HookP06ShortXYStateName(const FP_HookPhase06XYClosureState s)
{
   if(s == FP_HOOK_P06_XY_CLOSED) return "XY";
   if(s == FP_HOOK_P06_XY_X_ONLY) return "X";
   if(s == FP_HOOK_P06_XY_Y_ONLY) return "Y";
   if(s == FP_HOOK_P06_XY_OPEN) return "OPN";
   if(s == FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN) return "DED";
   if(s == FP_HOOK_P06_XY_INSUFFICIENT) return "INS";
   return "UNK";
}

string FP_HookP06ShortQualityBucketName(const FP_HookPhase06QualityBucket q)
{
   if(q == FP_HOOK_P06_QUALITY_ELITE) return "E";
   if(q == FP_HOOK_P06_QUALITY_HIGH) return "H";
   if(q == FP_HOOK_P06_QUALITY_MEDIUM) return "M";
   if(q == FP_HOOK_P06_QUALITY_LOW) return "L";
   if(q == FP_HOOK_P06_QUALITY_INVALID) return "INV";
   return "UNK";
}

color FP_HookP06XYColor(const FP_HookPhase06Config &cfg,
                        const FP_HookPhase06XYClosureState s)
{
   if(s == FP_HOOK_P06_XY_CLOSED) return cfg.xy_closed_color;
   if(s == FP_HOOK_P06_XY_X_ONLY) return cfg.x_only_color;
   if(s == FP_HOOK_P06_XY_Y_ONLY) return cfg.y_only_color;
   if(s == FP_HOOK_P06_XY_OPEN) return cfg.open_color;
   return cfg.insufficient_color;
}

string FP_HookP06BaseName(const FP_HookPhase06Config &cfg,
                          const FP_HookPhase06Record &record)
{
   string name = cfg.object_prefix;
   name += FP_HookP02DirectionName(record.p05.p04.p03.sequence.direction);
   name += "_L" + IntegerToString(record.p05.p04.p03.sequence.scale_l);
   name += "_S" + IntegerToString(record.p05.p04.p03.sequence.sequence_id);
   name += "_O" + IntegerToString(record.p05.p04.p03.sequence.origin_node_id);
   return name;
}

bool FP_HookP06CreateText(const string name,
                          const datetime t,
                          const double price,
                          const string text,
                          const color c,
                          const int font_size,
                          FP_HookPhase06Report &report)
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

bool FP_HookP06CreateArrow(const string name,
                           const datetime t,
                           const double price,
                           const color c,
                           const int arrow_code,
                           const int width,
                           FP_HookPhase06Report &report)
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

bool FP_HookP06CreateTrend(const string name,
                           const datetime t1,
                           const double p1,
                           const datetime t2,
                           const double p2,
                           const color c,
                           const int width,
                           const ENUM_LINE_STYLE style,
                           FP_HookPhase06Report &report)
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

bool FP_HookP06DrawOneRecord(const FP_HookPhase06Config &cfg,
                             const FP_HookPhase06Record &record,
                             FP_HookPhase06Report &report)
{
   if(!record.valid)
      return false;

   string base = FP_HookP06BaseName(cfg, record);
   FP_HookPhase02Sequence seq = record.p05.p04.p03.sequence;
   FP_HookPhase03YAxis y = record.p05.p04.p03.y_axis;
   FP_HookPhase06Score s = record.score;
   color c = FP_HookP06XYColor(cfg, s.xy_state);

   if(cfg.draw_xy_anchor && s.anchor_time > 0)
   {
      int arrow_code = 108;
      if(s.xy_state == FP_HOOK_P06_XY_CLOSED)
         arrow_code = 110;
      else if(s.xy_state == FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN)
         arrow_code = 251;
      else if(s.xy_state == FP_HOOK_P06_XY_INSUFFICIENT)
         arrow_code = 159;

      FP_HookP06CreateArrow(base + "_XY_ANCHOR",
                            s.anchor_time, s.anchor_price,
                            c, arrow_code,
                            cfg.marker_width + 1, report);
   }

   if(cfg.draw_quality_label && s.anchor_time > 0)
   {
      string dir_short = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? "+" : "-");
      string txt = "Q " + FP_HookP06ShortXYStateName(s.xy_state) + dir_short +
                   " " + FP_HookP06ShortQualityBucketName(s.quality_bucket) +
                   " " + DoubleToString(s.quality_score, 2);

      FP_HookP06CreateText(base + "_QUALITY_LABEL",
                           s.anchor_time, s.anchor_price,
                           txt, c,
                           cfg.label_font_size, report);
   }

   if(cfg.draw_projection_lines)
   {
      if(y.has_y01 && y.has_y12)
      {
         FP_HookP06CreateTrend(base + "_Y_STEP_01_12",
                               y.y01_time, y.y01_price,
                               y.y12_time, y.y12_price,
                               cfg.projection_color, cfg.line_width,
                               STYLE_DASH, report);
      }

      if(y.has_y12 && y.has_y23)
      {
         FP_HookP06CreateTrend(base + "_Y_STEP_12_23",
                               y.y12_time, y.y12_price,
                               y.y23_time, y.y23_price,
                               cfg.projection_color, cfg.line_width,
                               STYLE_DASH, report);
      }

      if(y.has_y23 && y.has_y34)
      {
         FP_HookP06CreateTrend(base + "_Y_STEP_23_34",
                               y.y23_time, y.y23_price,
                               y.y34_time, y.y34_price,
                               cfg.projection_color, cfg.line_width,
                               STYLE_DASH, report);
      }
   }

   if(cfg.draw_labels)
   {
      string logic_txt = "P06 x=" + DoubleToString(s.x_strength, 2) +
                         " y=" + DoubleToString(s.y_strength, 2) +
                         " type=" + DoubleToString(s.type_strength, 2) +
                         " life=" + DoubleToString(s.lifecycle_strength, 2) +
                         " " + s.reason;

      FP_HookP06CreateText(base + "_LOGIC_LABEL",
                           seq.origin_time, seq.origin_price,
                           logic_txt, cfg.label_color,
                           cfg.label_font_size, report);
   }

   return true;
}

int FP_HookP06DrawRecords(const FP_HookPhase06Config &cfg,
                          const FP_HookPhase06Record &records[],
                          FP_HookPhase06Report &report)
{
   report.objects_deleted += FP_HookPhase06DeleteObjects(cfg.object_prefix);

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
      if(FP_HookP06DrawOneRecord(cfg, records[i], report))
         drawn++;
   }

   report.records_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE06_VISUAL_MQH__
