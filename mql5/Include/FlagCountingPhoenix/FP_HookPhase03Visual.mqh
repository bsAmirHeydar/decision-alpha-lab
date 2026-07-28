#ifndef __FP_HOOK_PHASE03_VISUAL_MQH__
#define __FP_HOOK_PHASE03_VISUAL_MQH__
#property strict

#include "FP_HookPhase03Rules.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

int FP_HookPhase03DeleteObjects(const string prefix)
{
   return AL_UC04DeleteObjectsByPrefix(0, prefix);
}

color FP_HookP03YColor(const FP_HookPhase03Config &cfg,
                       const FP_HookPhase02Direction direction)
{
   if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.positive_y_color;
   return cfg.negative_y_color;
}

string FP_HookP03BaseName(const FP_HookPhase03Config &cfg,
                          const FP_HookPhase03Record &record)
{
   string name = cfg.object_prefix;
   name += FP_HookP02DirectionName(record.sequence.direction);
   name += "_L" + IntegerToString(record.sequence.scale_l);
   name += "_S" + IntegerToString(record.sequence.sequence_id);
   name += "_O" + IntegerToString(record.sequence.origin_node_id);
   return name;
}

bool FP_HookP03CreateText(const string name,
                          const datetime t,
                          const double price,
                          const string text,
                          const color c,
                          const int font_size,
                          FP_HookPhase03Report &report)
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

bool FP_HookP03CreateArrow(const string name,
                           const datetime t,
                           const double price,
                           const color c,
                           const int arrow_code,
                           const int width,
                           FP_HookPhase03Report &report)
{
   return AL_UC04CreateArrow(
      0,
      name,
      t,
      price,
      c,
      arrow_code,
      width,
      report.objects_created
   );
}

bool FP_HookP03CreateTrend(const string name,
                           const datetime t1,
                           const double p1,
                           const datetime t2,
                           const double p2,
                           const color c,
                           const int width,
                           const ENUM_LINE_STYLE style,
                           FP_HookPhase03Report &report)
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

bool FP_HookP03GetYPoint(const FP_HookPhase03YAxis &y,
                         const int slot,
                         datetime &t,
                         double &price,
                         string &label)
{
   if(slot == 1 && y.has_y01)
   {
      t = y.y01_time;
      price = y.y01_price;
      label = "Y01";
      return true;
   }
   if(slot == 2 && y.has_y12)
   {
      t = y.y12_time;
      price = y.y12_price;
      label = "Y12";
      return true;
   }
   if(slot == 3 && y.has_y23)
   {
      t = y.y23_time;
      price = y.y23_price;
      label = "Y23";
      return true;
   }
   if(slot == 4 && y.has_y34)
   {
      t = y.y34_time;
      price = y.y34_price;
      label = "Y34";
      return true;
   }
   return false;
}

bool FP_HookP03DrawOneRecord(const FP_HookPhase03Config &cfg,
                             const FP_HookPhase03Record &record,
                             FP_HookPhase03Report &report)
{
   if(!record.valid)
      return false;

   string base = FP_HookP03BaseName(cfg, record);
   color y_color = FP_HookP03YColor(cfg, record.sequence.direction);

   if(cfg.draw_y_extremes)
   {
      for(int slot=1; slot<=4; slot++)
      {
         datetime t;
         double price;
         string label;

         if(FP_HookP03GetYPoint(record.y_axis, slot, t, price, label))
         {
            FP_HookP03CreateArrow(base + "_" + label + "_EXTREME",
                                  t, price, y_color, 159, cfg.marker_width, report);

            if(cfg.draw_labels)
               FP_HookP03CreateText(base + "_" + label + "_LABEL",
                                    t, price, label, cfg.label_color,
                                    cfg.label_font_size, report);
         }
      }
   }

   if(cfg.draw_y_lines)
   {
      datetime prev_t = 0;
      double prev_p = 0.0;
      string prev_label = "";

      for(int slot=1; slot<=4; slot++)
      {
         datetime t;
         double price;
         string label;

         if(!FP_HookP03GetYPoint(record.y_axis, slot, t, price, label))
            continue;

         if(prev_t > 0)
         {
            FP_HookP03CreateTrend(base + "_YLINE_" + prev_label + "_" + label,
                                  prev_t, prev_p, t, price,
                                  y_color, cfg.line_width, STYLE_DASH, report);
         }

         prev_t = t;
         prev_p = price;
         prev_label = label;
      }
   }

   if(cfg.draw_x_reference)
   {
      for(int p=0; p<record.sequence.x_count && p<4; p++)
      {
         datetime t1, t2;
         double price1, price2;
         string label1, label2;

         if(FP_HookP02GetPoint(record.sequence, p, t1, price1, label1) &&
            FP_HookP02GetPoint(record.sequence, p+1, t2, price2, label2))
         {
            FP_HookP03CreateTrend(base + "_XREF_" + label1 + "_" + label2,
                                  t1, price1, t2, price2,
                                  cfg.x_reference_color, cfg.line_width, STYLE_DOT, report);
         }
      }
   }

   if(cfg.draw_labels)
   {
      datetime anchor_t = record.sequence.origin_time;
      double anchor_p = record.sequence.origin_price;
      string txt = "P03 " + FP_HookP02DirectionName(record.sequence.direction) +
                   " L" + IntegerToString(record.sequence.scale_l) +
                   " S" + IntegerToString(record.sequence.sequence_id) +
                   " Y" + IntegerToString(record.y_axis.y_count) +
                   " " + FP_HookP03YStateName(record.y_axis.y_state);

      FP_HookP03CreateText(base + "_Y_STATE_LABEL",
                           anchor_t, anchor_p, txt,
                           cfg.label_color, cfg.label_font_size, report);
   }

   return true;
}

int FP_HookP03DrawRecords(const FP_HookPhase03Config &cfg,
                          const FP_HookPhase03Record &records[],
                          FP_HookPhase03Report &report)
{
   report.objects_deleted += FP_HookPhase03DeleteObjects(cfg.object_prefix);

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
      if(FP_HookP03DrawOneRecord(cfg, records[i], report))
         drawn++;
   }

   report.records_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE03_VISUAL_MQH__
