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

string g_fp_hook_p02_label_keys[];
int    g_fp_hook_p02_label_counts[];

void FP_HookP02ResetLabelCollisionState()
{
   ArrayResize(g_fp_hook_p02_label_keys, 0);
   ArrayResize(g_fp_hook_p02_label_counts, 0);
}

int FP_HookP02ConsumeLabelStackSlot(const datetime t,
                                    const double price)
{
   string key = IntegerToString((int)t) + "|" + DoubleToString(price, _Digits);
   for(int i=0; i<ArraySize(g_fp_hook_p02_label_keys); i++)
   {
      if(g_fp_hook_p02_label_keys[i] == key)
      {
         int slot = g_fp_hook_p02_label_counts[i];
         g_fp_hook_p02_label_counts[i] = slot + 1;
         return slot;
      }
   }

   int n = ArraySize(g_fp_hook_p02_label_keys);
   ArrayResize(g_fp_hook_p02_label_keys, n + 1);
   ArrayResize(g_fp_hook_p02_label_counts, n + 1);
   g_fp_hook_p02_label_keys[n] = key;
   g_fp_hook_p02_label_counts[n] = 1;
   return 0;
}

color FP_HookP02ColorFromPalette(const int index)
{
   static color palette[16] =
   {
      clrDeepSkyBlue, clrTomato, clrGold, clrMediumSeaGreen,
      clrOrchid, clrOrange, clrAqua, clrDodgerBlue,
      clrHotPink, clrLimeGreen, clrSandyBrown, clrViolet,
      clrTurquoise, clrSalmon, clrKhaki, clrPlum
   };

   int n = ArraySize(palette);
   if(n <= 0)
      return clrSilver;

   int k = index % n;
   if(k < 0)
      k += n;
   return palette[k];
}

color FP_HookP02SequenceColor(const FP_HookPhase02Config &cfg,
                              const FP_HookPhase02Sequence &seq)
{
   if(cfg.use_sequence_palette_colors)
      return FP_HookP02ColorFromPalette(seq.sequence_id + seq.scale_l * 3 + (int)seq.direction * 7);

   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.positive_color;
   return cfg.negative_color;
}

string FP_HookP02NodeDisplayLabel(const FP_HookPhase02Config &cfg,
                                  const int point_index,
                                  const string fallback_label)
{
   if(cfg.node_label_mode == FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ZERO)
      return IntegerToString(point_index);
   if(cfg.node_label_mode == FP_HOOK_P02_NODE_LABEL_NUMBERS_WITH_O)
   {
      if(point_index == 0)
         return "O";
      return IntegerToString(point_index);
   }
   if(cfg.node_label_mode == FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN)
   {
      if(point_index == 0)
         return "";
      return IntegerToString(point_index);
   }
   return fallback_label;
}

color FP_HookP02NodeNumberColor(const FP_HookPhase02Config &cfg,
                                  const int point_index,
                                  const color fallback_color)
{
   if(!cfg.color_node_numbers_by_index)
      return fallback_color;

   if(point_index == 1) return cfg.node1_label_color;
   if(point_index == 2) return cfg.node2_label_color;
   if(point_index == 3) return cfg.node3_label_color;
   if(point_index == 4) return cfg.node4_label_color;
   return fallback_color;
}

double FP_HookP02NodeLabelPrice(const FP_HookPhase02Config &cfg,
                                const FP_HookPhase02Sequence &seq,
                                const double price,
                                const int point_index,
                                const int stack_slot)
{
   if(cfg.node_number_offset_points <= 0 && (!cfg.stack_node_labels_on_collisions || cfg.node_label_stack_step_points <= 0))
      return price;

   double sign = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? -1.0 : 1.0);
   if(point_index == 0)
      sign *= 1.25;

   double total_points = (double)cfg.node_number_offset_points;
   if(cfg.stack_node_labels_on_collisions && stack_slot > 0 && cfg.node_label_stack_step_points > 0)
      total_points += (double)(stack_slot * cfg.node_label_stack_step_points);

   return price + sign * _Point * total_points;
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

bool FP_HookP02GetCycleEndPoint(const FP_HookPhase02Sequence &seq,
                                datetime &t,
                                double &price,
                                string &label)
{
   t = 0;
   price = 0.0;
   label = "";

   if(seq.x_count >= 4 && seq.x4_time > 0)
   {
      t = seq.x4_time;
      price = seq.x4_price;
      label = "X4";
      return true;
   }
   if(seq.x_count >= 3 && seq.x3_time > 0)
   {
      t = seq.x3_time;
      price = seq.x3_price;
      label = "X3";
      return true;
   }
   if(seq.x_count >= 2 && seq.x2_time > 0)
   {
      t = seq.x2_time;
      price = seq.x2_price;
      label = "X2";
      return true;
   }
   if(seq.x_count >= 1 && seq.x1_time > 0)
   {
      t = seq.x1_time;
      price = seq.x1_price;
      label = "X1";
      return true;
   }

   return false;
}

double FP_HookP02CycleArcHeight(const FP_HookPhase02Sequence &seq,
                                const FP_HookPhase02Config &cfg,
                                const double end_price)
{
   double span = MathAbs(end_price - seq.origin_price);
   double min_height = _Point * 20.0;
   double h = span * cfg.cycle_arc_height_ratio;

   if(h < min_height)
      h = min_height;

   if(cfg.cycle_arc_max_height_points > 0)
   {
      double max_height = _Point * (double)cfg.cycle_arc_max_height_points;
      if(max_height > 0.0 && h > max_height)
         h = max_height;
   }
   return h;
}

bool FP_HookP02CreateCycleArc(const string base,
                              const FP_HookPhase02Sequence &seq,
                              const FP_HookPhase02Config &cfg,
                              FP_HookPhase02Report &report)
{
   datetime end_time = 0;
   double end_price = 0.0;
   string end_label = "";

   if(!FP_HookP02GetCycleEndPoint(seq, end_time, end_price, end_label))
      return false;

   if(seq.origin_time <= 0 || end_time <= seq.origin_time)
      return false;

   int segments = cfg.cycle_arc_segments;
   if(segments < 4)
      segments = 4;
   if(segments > 64)
      segments = 64;

   long t0 = (long)seq.origin_time;
   long dt = (long)(end_time - seq.origin_time);
   if(dt <= 0)
      return false;

   double h = FP_HookP02CycleArcHeight(seq, cfg, end_price);
   double sign = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? -1.0 : 1.0);
   double pi = 3.14159265358979323846;

   for(int k=0; k<segments; k++)
   {
      double f1 = (double)k / (double)segments;
      double f2 = (double)(k + 1) / (double)segments;

      datetime t1 = (datetime)(t0 + (long)MathRound((double)dt * f1));
      datetime t2 = (datetime)(t0 + (long)MathRound((double)dt * f2));

      double base1 = seq.origin_price + (end_price - seq.origin_price) * f1;
      double base2 = seq.origin_price + (end_price - seq.origin_price) * f2;

      double p1 = base1 + sign * h * MathSin(pi * f1);
      double p2 = base2 + sign * h * MathSin(pi * f2);

      color arc_color = (cfg.use_sequence_palette_colors ? FP_HookP02SequenceColor(cfg, seq) : cfg.cycle_arc_color);
      FP_HookP02CreateTrend(base + "_CYCLE_ARC_" + IntegerToString(k),
                            t1, p1, t2, p2,
                            arc_color, cfg.line_width,
                            STYLE_SOLID, report);
   }

   return true;
}

bool FP_HookP02DrawSequenceCountLabel(const string base,
                                      const FP_HookPhase02Sequence &seq,
                                      const FP_HookPhase02Config &cfg,
                                      FP_HookPhase02Report &report)
{
   datetime end_time = 0;
   double end_price = 0.0;
   string end_label = "";

   if(!FP_HookP02GetCycleEndPoint(seq, end_time, end_price, end_label))
      return false;

   long t0 = (long)seq.origin_time;
   long dt = (long)(end_time - seq.origin_time);
   if(dt <= 0)
      return false;

   double h = FP_HookP02CycleArcHeight(seq, cfg, end_price);
   double sign = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? -1.0 : 1.0);
   datetime mid_t = (datetime)(t0 + dt / 2);
   double mid_p = (seq.origin_price + end_price) * 0.5 + sign * h * 1.10;

   string dir_short = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? "+" : "-");
   string txt = "C" + IntegerToString(seq.sequence_id) + dir_short +
                " L" + IntegerToString(seq.scale_l) +
                " " + end_label +
                " n=" + IntegerToString(seq.x_count);

   return FP_HookP02CreateText(base + "_CYCLE_COUNT_LABEL",
                               mid_t, mid_p,
                               txt, cfg.sequence_count_label_color,
                               cfg.label_font_size + 1, report);
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

   color origin_marker_color = (cfg.color_origin_with_sequence ? seq_color : cfg.origin_color);

   if(cfg.draw_origin)
   {
      int origin_arrow_code = (cfg.use_minimal_node_markers ? cfg.minimal_node_marker_arrow_code : 159);
      FP_HookP02CreateArrow(base + "_ORIGIN", seq.origin_time, seq.origin_price,
                            origin_marker_color, origin_arrow_code, cfg.marker_width + 1, report);
   }

   if(cfg.draw_labels && !cfg.minimal_numbers_only)
   {
      string main_label = "H02 " + FP_HookP02DirectionName(seq.direction) +
                          " L" + IntegerToString(seq.scale_l) +
                          " S" + IntegerToString(seq.sequence_id) +
                          " " + FP_HookP02StateName(seq.state) +
                          " X" + IntegerToString(seq.x_count);
      FP_HookP02CreateText(base + "_LABEL", seq.origin_time, seq.origin_price,
                           main_label, cfg.label_color, cfg.label_font_size, report);
   }

   if(cfg.draw_labels && cfg.minimal_numbers_only)
   {
      color origin_label_color = (cfg.color_node_labels_with_sequence ? seq_color : cfg.label_color);
      string origin_label = FP_HookP02NodeDisplayLabel(cfg, 0, "O");
      if(origin_label != "")
      {
         double origin_label_price = FP_HookP02NodeLabelPrice(cfg, seq, seq.origin_price, 0, 0);
         FP_HookP02CreateText(base + "_ORIGIN_NODE_LABEL", seq.origin_time, origin_label_price,
                              origin_label, origin_label_color, cfg.label_font_size, report);
      }
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
            int arrow_code = (cfg.use_minimal_node_markers ? cfg.minimal_node_marker_arrow_code :
                              (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? 233 : 234));
            FP_HookP02CreateArrow(base + "_" + label + "_NODE", t, price,
                                  seq_color, arrow_code, cfg.marker_width, report);

            if(cfg.draw_labels)
            {
               string node_display = FP_HookP02NodeDisplayLabel(cfg, p, label);
               if(node_display != "")
               {
                  color node_label_color = (cfg.color_node_labels_with_sequence ? seq_color : cfg.label_color);
                  node_label_color = FP_HookP02NodeNumberColor(cfg, p, node_label_color);
                  int stack_slot = (cfg.stack_node_labels_on_collisions ? FP_HookP02ConsumeLabelStackSlot(t, price) : 0);
                  double node_label_price = FP_HookP02NodeLabelPrice(cfg, seq, price, p, stack_slot);
                  FP_HookP02CreateText(base + "_" + label + "_LABEL", t, node_label_price,
                                       node_display, node_label_color, cfg.label_font_size, report);
               }
            }
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

   if(cfg.draw_cycle_arc && seq.x_count >= cfg.arc_min_x_count_to_draw)
      FP_HookP02CreateCycleArc(base, seq, cfg, report);

   if(cfg.draw_sequence_count_label)
      FP_HookP02DrawSequenceCountLabel(base, seq, cfg, report);

   if(cfg.draw_death_boundary)
   {
      datetime end_time = seq.last_x_time;
      if(end_time <= 0)
         end_time = seq.origin_time;
      FP_HookP02CreateTrend(base + "_DEATH_BOUNDARY",
                            seq.origin_time, seq.death_boundary_price,
                            end_time, seq.death_boundary_price,
                            cfg.death_color, cfg.line_width, STYLE_DOT, report);

      if(cfg.draw_labels && !cfg.minimal_numbers_only)
         FP_HookP02CreateText(base + "_DEATH_LABEL", end_time, seq.death_boundary_price,
                              "DEATH/O", cfg.death_color, cfg.label_font_size, report);
   }

   return true;
}

bool FP_HookP02SequencePassesDrawFilter(const FP_HookPhase02Config &cfg,
                                      const FP_HookPhase02Sequence &seq)
{
   if(!seq.valid)
      return false;

   if(cfg.min_x_count_to_draw > 0 && seq.x_count < cfg.min_x_count_to_draw)
      return false;

   if(cfg.sequence_draw_direction != 0 && (int)seq.direction != cfg.sequence_draw_direction)
      return false;

   if(cfg.sequence_draw_mode == FP_HOOK_P02_DRAW_BY_SCALE_RECENT_N ||
      cfg.sequence_draw_scale_l > 0)
   {
      if(cfg.sequence_draw_scale_l > 0 && seq.scale_l != cfg.sequence_draw_scale_l)
         return false;
   }

   if(cfg.sequence_draw_mode == FP_HOOK_P02_DRAW_BY_SEQUENCE_ID)
   {
      if(cfg.sequence_draw_sequence_id < 0)
         return false;
      if(seq.sequence_id != cfg.sequence_draw_sequence_id)
         return false;
   }

   return true;
}

bool FP_HookP02AlreadySelectedScaleDirection(const int &scales[],
                                             const int &directions[],
                                             const int count,
                                             const int scale_l,
                                             const int direction)
{
   for(int i=0; i<count; i++)
   {
      if(scales[i] == scale_l && directions[i] == direction)
         return true;
   }
   return false;
}

void FP_HookP02SelectSequenceIndexes(const FP_HookPhase02Config &cfg,
                                     const FP_HookPhase02Sequence &sequences[],
                                     int &indexes[])
{
   ArrayResize(indexes, 0);

   int n = ArraySize(sequences);
   int max_draw = cfg.max_sequences_to_draw;
   if(max_draw <= 0)
      max_draw = n;
   if(max_draw > n)
      max_draw = n;

   if(cfg.sequence_draw_mode == FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION)
   {
      int selected_scales[];
      int selected_dirs[];
      int selected_count = 0;

      for(int i=n-1; i>=0 && ArraySize(indexes)<max_draw; i--)
      {
         if(!FP_HookP02SequencePassesDrawFilter(cfg, sequences[i]))
            continue;

         int dir = (int)sequences[i].direction;
         if(FP_HookP02AlreadySelectedScaleDirection(selected_scales, selected_dirs,
                                                    selected_count,
                                                    sequences[i].scale_l, dir))
            continue;

         ArrayResize(selected_scales, selected_count + 1);
         ArrayResize(selected_dirs, selected_count + 1);
         selected_scales[selected_count] = sequences[i].scale_l;
         selected_dirs[selected_count] = dir;
         selected_count++;

         int k = ArraySize(indexes);
         ArrayResize(indexes, k + 1);
         indexes[k] = i;
      }
   }
   else
   {
      for(int i=n-1; i>=0 && ArraySize(indexes)<max_draw; i--)
      {
         if(!FP_HookP02SequencePassesDrawFilter(cfg, sequences[i]))
            continue;

         int k = ArraySize(indexes);
         ArrayResize(indexes, k + 1);
         indexes[k] = i;
      }
   }

   // Draw older selected structures first so later/livelier structures remain visually dominant.
   int m = ArraySize(indexes);
   for(int a=0; a<m/2; a++)
   {
      int b = m - 1 - a;
      int tmp = indexes[a];
      indexes[a] = indexes[b];
      indexes[b] = tmp;
   }
}

int FP_HookP02DrawSequences(const FP_HookPhase02Config &cfg,
                            const FP_HookPhase02Sequence &sequences[],
                            FP_HookPhase02Report &report)
{
   if(!cfg.draw_sequences)
      return 0;

   report.objects_deleted += FP_HookPhase02DeleteObjects(cfg.object_prefix);
   FP_HookP02ResetLabelCollisionState();

   int indexes[];
   FP_HookP02SelectSequenceIndexes(cfg, sequences, indexes);

   int drawn = 0;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      if(FP_HookP02DrawOneSequence(cfg, sequences[i], report))
         drawn++;
   }

   report.sequences_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE02_VISUAL_MQH__
