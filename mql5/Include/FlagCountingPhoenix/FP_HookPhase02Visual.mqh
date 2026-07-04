#ifndef __FP_HOOK_PHASE02_VISUAL_MQH__
#define __FP_HOOK_PHASE02_VISUAL_MQH__
#property strict

#include "FP_HookPhase02Rules.mqh"

int FP_HookPhase02DeleteObjects(const string prefix)
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

color FP_HookP02SequenceColor(const FP_HookPhase02Config &cfg,
                              const FP_HookPhase02Sequence &seq)
{
   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.positive_color;
   return cfg.negative_color;
}

string FP_HookP02BaseName(const FP_HookPhase02Config &cfg,
                          const FP_HookPhase02Sequence &seq)
{
   string name = cfg.object_prefix;
   name += FP_HookP02DirectionName(seq.direction);
   name += "_L" + IntegerToString(seq.scale_l);
   name += "_S" + IntegerToString(seq.sequence_id);
   name += "_O" + IntegerToString(seq.origin_node_id);
   return name;
}

bool FP_HookP02CreateText(const string name,
                          const datetime t,
                          const double price,
                          const string text,
                          const color c,
                          const int font_size,
                          FP_HookPhase02Report &report)
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

bool FP_HookP02CreateArrow(const string name,
                           const datetime t,
                           const double price,
                           const color c,
                           const int arrow_code,
                           const int width,
                           FP_HookPhase02Report &report)
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

bool FP_HookP02CreateTrend(const string name,
                           const datetime t1,
                           const double p1,
                           const datetime t2,
                           const double p2,
                           const color c,
                           const int width,
                           const ENUM_LINE_STYLE style,
                           FP_HookPhase02Report &report)
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

bool FP_HookP02GetPoint(const FP_HookPhase02Sequence &seq,
                        const int point_index,
                        datetime &t,
                        double &price,
                        string &label)
{
   if(point_index == 0)
   {
      t = seq.origin_time;
      price = seq.origin_price;
      label = "O";
      return true;
   }
   if(point_index == 1 && seq.x_count >= 1)
   {
      t = seq.x1_time;
      price = seq.x1_price;
      label = "X1";
      return true;
   }
   if(point_index == 2 && seq.x_count >= 2)
   {
      t = seq.x2_time;
      price = seq.x2_price;
      label = "X2";
      return true;
   }
   if(point_index == 3 && seq.x_count >= 3)
   {
      t = seq.x3_time;
      price = seq.x3_price;
      label = "X3";
      return true;
   }
   if(point_index == 4 && seq.x_count >= 4)
   {
      t = seq.x4_time;
      price = seq.x4_price;
      label = "X4";
      return true;
   }
   return false;
}

bool FP_HookP02DrawOneSequence(const FP_HookPhase02Config &cfg,
                               const FP_HookPhase02Sequence &seq,
                               FP_HookPhase02Report &report)
{
   if(!seq.valid)
      return false;

   string base = FP_HookP02BaseName(cfg, seq);
   color seq_color = FP_HookP02SequenceColor(cfg, seq);

   if(cfg.draw_origin)
   {
      FP_HookP02CreateArrow(base + "_ORIGIN", seq.origin_time, seq.origin_price,
                            cfg.origin_color, 159, cfg.marker_width + 1, report);
   }

   if(cfg.draw_labels)
   {
      string main_label = "H02 " + FP_HookP02DirectionName(seq.direction) +
                          " L" + IntegerToString(seq.scale_l) +
                          " S" + IntegerToString(seq.sequence_id) +
                          " " + FP_HookP02StateName(seq.state) +
                          " X" + IntegerToString(seq.x_count);
      FP_HookP02CreateText(base + "_LABEL", seq.origin_time, seq.origin_price,
                           main_label, cfg.label_color, cfg.label_font_size, report);
   }

   if(cfg.draw_x_nodes)
   {
      for(int p=1; p<=seq.x_count && p<=4; p++)
      {
         datetime t;
         double price;
         string label;
         if(FP_HookP02GetPoint(seq, p, t, price, label))
         {
            int arrow_code = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? 233 : 234);
            FP_HookP02CreateArrow(base + "_" + label + "_NODE", t, price,
                                  seq_color, arrow_code, cfg.marker_width, report);

            if(cfg.draw_labels)
               FP_HookP02CreateText(base + "_" + label + "_LABEL", t, price,
                                    label, cfg.label_color, cfg.label_font_size, report);
         }
      }
   }

   if(cfg.draw_x_lines)
   {
      for(int p=0; p<seq.x_count && p<4; p++)
      {
         datetime t1, t2;
         double price1, price2;
         string label1, label2;

         if(FP_HookP02GetPoint(seq, p, t1, price1, label1) &&
            FP_HookP02GetPoint(seq, p+1, t2, price2, label2))
         {
            FP_HookP02CreateTrend(base + "_LINE_" + label1 + "_" + label2,
                                  t1, price1, t2, price2,
                                  seq_color, cfg.line_width, STYLE_SOLID, report);
         }
      }
   }

   if(cfg.draw_death_boundary)
   {
      datetime end_time = seq.last_x_time;
      if(end_time <= 0)
         end_time = seq.origin_time;
      FP_HookP02CreateTrend(base + "_DEATH_BOUNDARY",
                            seq.origin_time, seq.death_boundary_price,
                            end_time, seq.death_boundary_price,
                            cfg.death_color, cfg.line_width, STYLE_DOT, report);

      if(cfg.draw_labels)
         FP_HookP02CreateText(base + "_DEATH_LABEL", end_time, seq.death_boundary_price,
                              "DEATH/O", cfg.death_color, cfg.label_font_size, report);
   }

   return true;
}

int FP_HookP02DrawSequences(const FP_HookPhase02Config &cfg,
                            const FP_HookPhase02Sequence &sequences[],
                            FP_HookPhase02Report &report)
{
   if(!cfg.draw_sequences)
      return 0;

   report.objects_deleted += FP_HookPhase02DeleteObjects(cfg.object_prefix);

   int n = ArraySize(sequences);
   int max_draw = cfg.max_sequences_to_draw;
   if(max_draw <= 0 || max_draw > n)
      max_draw = n;

   int start = n - max_draw;
   if(start < 0)
      start = 0;

   int drawn = 0;
   for(int i=start; i<n; i++)
   {
      if(FP_HookP02DrawOneSequence(cfg, sequences[i], report))
         drawn++;
   }

   report.sequences_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE02_VISUAL_MQH__
