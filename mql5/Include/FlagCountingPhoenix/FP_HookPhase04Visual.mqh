#ifndef __FP_HOOK_PHASE04_VISUAL_MQH__
#define __FP_HOOK_PHASE04_VISUAL_MQH__
#property strict

#include "FP_HookPhase04Rules.mqh"

int FP_HookPhase04DeleteObjects(const string prefix)
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

datetime FP_HookP04LatestRelevantTime(const FP_HookPhase04Record &record)
{
   datetime latest_time = record.p03.sequence.origin_time;

   if(record.p03.sequence.last_x_time > latest_time)
      latest_time = record.p03.sequence.last_x_time;
   if(record.p03.y_axis.y01_time > latest_time)
      latest_time = record.p03.y_axis.y01_time;
   if(record.p03.y_axis.y12_time > latest_time)
      latest_time = record.p03.y_axis.y12_time;
   if(record.p03.y_axis.y23_time > latest_time)
      latest_time = record.p03.y_axis.y23_time;
   if(record.p03.y_axis.y34_time > latest_time)
      latest_time = record.p03.y_axis.y34_time;
   if(record.lifecycle.nd_time > latest_time)
      latest_time = record.lifecycle.nd_time;
   if(record.lifecycle.death_time > latest_time)
      latest_time = record.lifecycle.death_time;
   if(record.lifecycle.x_closure_time > latest_time)
      latest_time = record.lifecycle.x_closure_time;
   return latest_time;
}

string FP_HookP04BaseName(const FP_HookPhase04Config &cfg,
                          const FP_HookPhase04Record &record)
{
   string name = cfg.object_prefix;
   name += FP_HookP02DirectionName(record.p03.sequence.direction);
   name += "_L" + IntegerToString(record.p03.sequence.scale_l);
   name += "_S" + IntegerToString(record.p03.sequence.sequence_id);
   name += "_O" + IntegerToString(record.p03.sequence.origin_node_id);
   return name;
}

bool FP_HookP04CreateText(const string name,
                          const datetime t,
                          const double price,
                          const string text,
                          const color c,
                          const int font_size,
                          FP_HookPhase04Report &report)
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

bool FP_HookP04CreateArrow(const string name,
                           const datetime t,
                           const double price,
                           const color c,
                           const int arrow_code,
                           const int width,
                           FP_HookPhase04Report &report)
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

bool FP_HookP04CreateTrend(const string name,
                           const datetime t1,
                           const double p1,
                           const datetime t2,
                           const double p2,
                           const color c,
                           const int width,
                           const ENUM_LINE_STYLE style,
                           FP_HookPhase04Report &report)
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

void FP_HookP04DrawHorizontalThreshold(const string base,
                                       const string suffix,
                                       const datetime t1,
                                       const datetime t2,
                                       const double price,
                                       const string label,
                                       const color c,
                                       const FP_HookPhase04Config &cfg,
                                       FP_HookPhase04Report &report)
{
   if(t1 <= 0 || t2 <= 0 || t1 == t2)
      return;

   FP_HookP04CreateTrend(base + "_" + suffix + "_LINE",
                         t1, price, t2, price,
                         c, cfg.line_width, STYLE_DOT, report);

   if(cfg.draw_labels)
      FP_HookP04CreateText(base + "_" + suffix + "_LABEL",
                           t2, price, label, c, cfg.label_font_size, report);
}

bool FP_HookP04DrawOneRecord(const FP_HookPhase04Config &cfg,
                             const FP_HookPhase04Record &record,
                             FP_HookPhase04Report &report)
{
   if(!record.valid)
      return false;

   string base = FP_HookP04BaseName(cfg, record);
   FP_HookPhase02Sequence seq = record.p03.sequence;
   FP_HookPhase04Lifecycle life = record.lifecycle;

   datetime last_x_time = FP_HookP04LatestXTime(seq);
   if(last_x_time <= 0)
      last_x_time = seq.origin_time;

   if(cfg.draw_thresholds)
   {
      datetime threshold_end_time = FP_HookP04LatestRelevantTime(record);
      if(threshold_end_time <= 0)
         threshold_end_time = last_x_time;
      if(threshold_end_time <= 0)
         threshold_end_time = seq.origin_time;

      FP_HookP04DrawHorizontalThreshold(base, "ND_THRESHOLD",
                                        last_x_time, threshold_end_time,
                                        life.nd_threshold_price,
                                        "ND TH",
                                        cfg.threshold_color, cfg, report);

      if(life.x_closure_threshold_price != 0.0)
         FP_HookP04DrawHorizontalThreshold(base, "X_CLOSURE_THRESHOLD",
                                           life.x_closure_reference_y_time,
                                           threshold_end_time,
                                           life.x_closure_threshold_price,
                                           "X CLOSE 50%",
                                           cfg.threshold_color, cfg, report);

      FP_HookP04DrawHorizontalThreshold(base, "DEATH_BOUNDARY",
                                        seq.origin_time, threshold_end_time,
                                        seq.origin_price,
                                        "ORIGIN/DEATH",
                                        cfg.death_color, cfg, report);
   }

   if(cfg.draw_nd && life.nd_detected)
   {
      FP_HookP04CreateArrow(base + "_ND_MARKER",
                            life.nd_time, life.nd_price,
                            cfg.nd_color, 159, cfg.marker_width + 1, report);

      if(cfg.draw_labels)
         FP_HookP04CreateText(base + "_ND_LABEL",
                              life.nd_time, life.nd_price,
                              "ND",
                              cfg.nd_color, cfg.label_font_size, report);
   }

   if(cfg.draw_death && life.origin_return_penetrated)
   {
      FP_HookP04CreateArrow(base + "_DEATH_MARKER",
                            life.death_time, life.death_price,
                            cfg.death_color, 251, cfg.marker_width + 1, report);

      if(cfg.draw_labels)
         FP_HookP04CreateText(base + "_DEATH_LABEL",
                              life.death_time, life.death_price,
                              "DEATH",
                              cfg.death_color, cfg.label_font_size, report);
   }

   if(cfg.draw_x_closure && life.x_closed)
   {
      FP_HookP04CreateArrow(base + "_X_CLOSED_MARKER",
                            life.x_closure_time, life.x_closure_price,
                            cfg.closure_color, 108, cfg.marker_width + 1, report);

      if(cfg.draw_labels)
         FP_HookP04CreateText(base + "_X_CLOSED_LABEL",
                              life.x_closure_time, life.x_closure_price,
                              "X CLOSED",
                              cfg.closure_color, cfg.label_font_size, report);
   }

   if(cfg.draw_labels)
   {
      string txt = "P04 " + FP_HookP02DirectionName(seq.direction) +
                   " L" + IntegerToString(seq.scale_l) +
                   " S" + IntegerToString(seq.sequence_id) +
                   " " + FP_HookP04LifecycleStateName(life.state);

      FP_HookP04CreateText(base + "_STATE_LABEL",
                           seq.origin_time, seq.origin_price,
                           txt, cfg.label_color, cfg.label_font_size, report);
   }

   return true;
}

int FP_HookP04DrawRecords(const FP_HookPhase04Config &cfg,
                          const FP_HookPhase04Record &records[],
                          FP_HookPhase04Report &report)
{
   report.objects_deleted += FP_HookPhase04DeleteObjects(cfg.object_prefix);

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
      if(FP_HookP04DrawOneRecord(cfg, records[i], report))
         drawn++;
   }

   report.records_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE04_VISUAL_MQH__
