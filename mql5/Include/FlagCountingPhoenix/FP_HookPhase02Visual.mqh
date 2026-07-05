#ifndef __FP_HOOK_PHASE02_VISUAL_MQH__
#define __FP_HOOK_PHASE02_VISUAL_MQH__
#property strict

#include "FP_HookPhase02Rules.mqh"

// ============================================================================
// Phase 02 Visual — Contract-aligned Hook/ND semantic renderer
// ----------------------------------------------------------------------------
// Semantic minimal view:
// - no straight sequence wiring by default
// - no heavy node markers by default
// - one Hook envelope curve per Hook-origin context
// - branch numbers 1..4 only, old-to-new
// - low-side numbers below valleys, high-side numbers above peaks
// - same branch sequence = same number color
// - deterministic stacked labels for shared nodes
// ============================================================================

datetime g_fp_hook_p02_label_cluster_times[];
double   g_fp_hook_p02_label_cluster_prices[];
int      g_fp_hook_p02_label_cluster_sides[];
int      g_fp_hook_p02_label_counts[];

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

void FP_HookP02ResetLabelCollisionState()
{
   ArrayResize(g_fp_hook_p02_label_cluster_times, 0);
   ArrayResize(g_fp_hook_p02_label_cluster_prices, 0);
   ArrayResize(g_fp_hook_p02_label_cluster_sides, 0);
   ArrayResize(g_fp_hook_p02_label_counts, 0);
}

int FP_HookP02ConsumeLabelStackSlot(const FP_HookPhase02Config &cfg,
                                    const datetime t,
                                    const double price,
                                    const bool place_below)
{
   int side = (place_below ? 1 : 0);

   int time_window = cfg.label_time_cluster_seconds;
   if(time_window <= 0)
   {
      time_window = PeriodSeconds(_Period);
      if(time_window <= 0)
         time_window = 60;
   }

   int price_window_points = cfg.label_price_cluster_points;
   if(price_window_points <= 0)
      price_window_points = 24;

   for(int i=0; i<ArraySize(g_fp_hook_p02_label_cluster_times); i++)
   {
      if(g_fp_hook_p02_label_cluster_sides[i] != side)
         continue;

      double dt = MathAbs((double)((long)t - (long)g_fp_hook_p02_label_cluster_times[i]));
      double dp = MathAbs(price - g_fp_hook_p02_label_cluster_prices[i]);
      if(dt <= (double)time_window && dp <= _Point * (double)price_window_points)
      {
         int slot = g_fp_hook_p02_label_counts[i];
         g_fp_hook_p02_label_counts[i] = slot + 1;
         return slot;
      }
   }

   int n = ArraySize(g_fp_hook_p02_label_cluster_times);
   ArrayResize(g_fp_hook_p02_label_cluster_times, n + 1);
   ArrayResize(g_fp_hook_p02_label_cluster_prices, n + 1);
   ArrayResize(g_fp_hook_p02_label_cluster_sides, n + 1);
   ArrayResize(g_fp_hook_p02_label_counts, n + 1);
   g_fp_hook_p02_label_cluster_times[n] = t;
   g_fp_hook_p02_label_cluster_prices[n] = price;
   g_fp_hook_p02_label_cluster_sides[n] = side;
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

string FP_HookP02FormattedNodeLabel(const FP_HookPhase02Config &cfg,
                                  const FP_HookPhase02Sequence &seq,
                                  const int branch_ordinal,
                                  const int point_index,
                                  const string fallback_label)
{
   string core = FP_HookP02NodeDisplayLabel(cfg, point_index, fallback_label);
   if(StringLen(core) <= 0)
      return "";

   if(!cfg.show_hook_sequence_ids_in_labels)
      return core;

   int branch_id = branch_ordinal;
   if(branch_id <= 0)
      branch_id = seq.sequence_id;

   return "H" + IntegerToString(seq.origin_node_id) + "B" + IntegerToString(branch_id) + ":" + core;
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

double FP_HookP02StackedLabelPrice(const FP_HookPhase02Config &cfg,
                                   const double anchor_price,
                                   const bool place_below,
                                   const int stack_slot)
{
   double base_points = (double)cfg.node_number_offset_points;
   if(base_points < 0.0)
      base_points = 0.0;

   double stack_points = 0.0;
   if(cfg.stack_node_labels_on_collisions && stack_slot > 0 && cfg.node_label_stack_step_points > 0)
      stack_points = (double)(stack_slot * cfg.node_label_stack_step_points);

   double total_points = base_points + stack_points;
   if(total_points <= 0.0)
      return anchor_price;

   double sign = (place_below ? -1.0 : 1.0);
   return anchor_price + sign * _Point * total_points;
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
   if(StringLen(text) <= 0)
      return false;

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
   if(t1 <= 0 || t2 <= 0 || t2 <= t1)
      return false;

   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, true);
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
   t = 0;
   price = 0.0;
   label = "";

   if(point_index == 0)
   {
      t = seq.origin_time;
      price = seq.origin_price;
      label = "O";
      return (t > 0);
   }
   if(point_index == 1 && seq.x1_time > 0)
   {
      t = seq.x1_time;
      price = seq.x1_price;
      label = "X1";
      return true;
   }
   if(point_index == 2 && seq.x2_time > 0)
   {
      t = seq.x2_time;
      price = seq.x2_price;
      label = "X2";
      return true;
   }
   if(point_index == 3 && seq.x3_time > 0)
   {
      t = seq.x3_time;
      price = seq.x3_price;
      label = "X3";
      return true;
   }
   if(point_index == 4 && seq.x4_time > 0)
   {
      t = seq.x4_time;
      price = seq.x4_price;
      label = "X4";
      return true;
   }

   return false;
}

bool FP_HookP02GetLastCountedPoint(const FP_HookPhase02Sequence &seq,
                                   datetime &t,
                                   double &price)
{
   string label;
   int n = seq.x_count;
   if(n > 4)
      n = 4;
   for(int p=n; p>=1; p--)
   {
      if(FP_HookP02GetPoint(seq, p, t, price, label))
         return true;
   }
   return false;
}

bool FP_HookP02SameOriginGroup(const FP_HookPhase02Sequence &a,
                               const FP_HookPhase02Sequence &b)
{
   return (a.direction == b.direction &&
           a.scale_l == b.scale_l &&
           a.origin_node_id == b.origin_node_id &&
           a.origin_time == b.origin_time &&
           a.origin_price == b.origin_price);
}

bool FP_HookP02GroupSeenBefore(const FP_HookPhase02Sequence &seed,
                               const FP_HookPhase02Sequence &sequences[],
                               const int &indexes[],
                               const int before_pos)
{
   for(int a=0; a<before_pos; a++)
   {
      int j = indexes[a];
      if(j < 0 || j >= ArraySize(sequences))
         continue;
      if(FP_HookP02SameOriginGroup(seed, sequences[j]))
         return true;
   }
   return false;
}

bool FP_HookP02GetOriginGroupEnvelope(const FP_HookPhase02Sequence &seed,
                                      const FP_HookPhase02Sequence &sequences[],
                                      const int &indexes[],
                                      datetime &start_time,
                                      double &start_price,
                                      datetime &crown_time,
                                      double &crown_price,
                                      datetime &end_time,
                                      double &end_price)
{
   start_time = seed.origin_time;
   start_price = seed.origin_price;
   crown_time = 0;
   crown_price = 0.0;
   end_time = 0;
   end_price = 0.0;

   if(start_time <= 0 || !seed.render_eligible || !seed.near_death_confirmed || seed.hook_failed)
      return false;

   bool crown_found = false;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;
      FP_HookPhase02Sequence seq = sequences[i];
      if(!seq.render_eligible || !seq.near_death_confirmed || seq.hook_failed)
         continue;
      if(!FP_HookP02SameOriginGroup(seed, seq))
         continue;
      if(!seq.cycle_crown_valid || seq.cycle_crown_time <= start_time)
         continue;

      if(!crown_found)
      {
         crown_found = true;
         crown_time = seq.cycle_crown_time;
         crown_price = seq.cycle_crown_price;
         continue;
      }

      if(seed.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         if(seq.cycle_crown_price > crown_price ||
            (seq.cycle_crown_price == crown_price && seq.cycle_crown_time < crown_time))
         {
            crown_time = seq.cycle_crown_time;
            crown_price = seq.cycle_crown_price;
         }
      }
      else
      {
         if(seq.cycle_crown_price < crown_price ||
            (seq.cycle_crown_price == crown_price && seq.cycle_crown_time < crown_time))
         {
            crown_time = seq.cycle_crown_time;
            crown_price = seq.cycle_crown_price;
         }
      }
   }

   if(!crown_found)
      return false;

   // Lifecycle-aligned: draw only to confirmed Near-Death resolve nodes.
   bool end_found = false;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;
      FP_HookPhase02Sequence seq = sequences[i];
      if(!seq.render_eligible || !seq.near_death_confirmed || seq.hook_failed)
         continue;
      if(!FP_HookP02SameOriginGroup(seed, seq))
         continue;
      if(!seq.resolve_confirmed || seq.resolve_time <= crown_time)
         continue;

      if(!end_found)
      {
         end_found = true;
         end_time = seq.resolve_time;
         end_price = seq.resolve_price;
         continue;
      }

      if(seed.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         if(seq.resolve_price < end_price || (seq.resolve_price == end_price && seq.resolve_time > end_time))
         {
            end_time = seq.resolve_time;
            end_price = seq.resolve_price;
         }
      }
      else
      {
         if(seq.resolve_price > end_price || (seq.resolve_price == end_price && seq.resolve_time > end_time))
         {
            end_time = seq.resolve_time;
            end_price = seq.resolve_price;
         }
      }
   }

   if(!end_found || end_time <= crown_time)
      return false;

   return true;
}

bool FP_HookP02CreateHookEnvelopeCurve(const string base,
                                       const datetime start_time,
                                       const double start_price,
                                       const datetime crown_time,
                                       const double crown_price,
                                       const datetime end_time,
                                       const double end_price,
                                       const color curve_color,
                                       const int line_width,
                                       FP_HookPhase02Report &report)
{
   if(start_time <= 0 || crown_time <= start_time || end_time <= crown_time)
      return false;

   int half_segments = 14;
   datetime prev_t = start_time;
   double prev_p = start_price;

   for(int k=1; k<=half_segments; k++)
   {
      double u = (double)k / (double)half_segments;
      double eased = MathSin(u * 1.5707963267948966);
      datetime cur_t = (datetime)((long)MathRound((double)start_time + ((double)(crown_time - start_time) * u)));
      double cur_p = start_price + (crown_price - start_price) * eased;
      if(cur_t <= prev_t)
         cur_t = (datetime)(prev_t + 1);

      FP_HookP02CreateTrend(base + "_ENV_A_" + IntegerToString(k),
                            prev_t, prev_p, cur_t, cur_p,
                            curve_color, line_width, STYLE_SOLID, report);
      prev_t = cur_t;
      prev_p = cur_p;
   }

   prev_t = crown_time;
   prev_p = crown_price;
   for(int k=1; k<=half_segments; k++)
   {
      double u = (double)k / (double)half_segments;
      double eased = 1.0 - MathCos(u * 1.5707963267948966);
      datetime cur_t = (datetime)((long)MathRound((double)crown_time + ((double)(end_time - crown_time) * u)));
      double cur_p = crown_price + (end_price - crown_price) * eased;
      if(cur_t <= prev_t)
         cur_t = (datetime)(prev_t + 1);

      FP_HookP02CreateTrend(base + "_ENV_B_" + IntegerToString(k),
                            prev_t, prev_p, cur_t, cur_p,
                            curve_color, line_width, STYLE_SOLID, report);
      prev_t = cur_t;
      prev_p = cur_p;
   }

   return true;
}

bool FP_HookP02DrawOneSequenceNumbers(const FP_HookPhase02Config &cfg,
                                      const FP_HookPhase02Sequence &seq,
                                      const int branch_ordinal,
                                      FP_HookPhase02Report &report)
{
   if(!cfg.draw_x_nodes || !cfg.draw_labels)
      return true;

   string base = FP_HookP02BaseName(cfg, seq);
   color seq_color = FP_HookP02SequenceColor(cfg, seq);
   bool place_below = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE);

   for(int p=1; p<=seq.x_count && p<=4; p++)
   {
      datetime t;
      double price;
      string label;
      if(!FP_HookP02GetPoint(seq, p, t, price, label))
         continue;

      if(cfg.draw_node_markers)
      {
         int arrow_code = (cfg.use_minimal_node_markers ? cfg.minimal_node_marker_arrow_code : 159);
         FP_HookP02CreateArrow(base + "_" + label + "_NODE", t, price, seq_color, arrow_code, cfg.marker_width, report);
      }

      string node_display = FP_HookP02FormattedNodeLabel(cfg, seq, branch_ordinal, p, label);
      if(StringLen(node_display) <= 0)
         continue;

      color node_color = (cfg.color_node_labels_with_sequence ? seq_color : cfg.label_color);
      node_color = FP_HookP02NodeNumberColor(cfg, p, node_color);
      int stack_slot = (cfg.stack_node_labels_on_collisions ? FP_HookP02ConsumeLabelStackSlot(cfg, t, price, place_below) : 0);
      double label_price = FP_HookP02StackedLabelPrice(cfg, price, place_below, stack_slot);

      FP_HookP02CreateText(base + "_" + label + "_LABEL", t, label_price,
                           node_display, node_color, cfg.label_font_size, report);
   }

   if(cfg.draw_x_lines)
   {
      for(int p=1; p<seq.x_count && p<4; p++)
      {
         datetime t1, t2;
         double price1, price2;
         string label1, label2;
         if(FP_HookP02GetPoint(seq, p, t1, price1, label1) &&
            FP_HookP02GetPoint(seq, p+1, t2, price2, label2))
         {
            FP_HookP02CreateTrend(base + "_DEBUG_LINE_" + label1 + "_" + label2,
                                  t1, price1, t2, price2,
                                  seq_color, cfg.line_width, STYLE_DOT, report);
         }
      }
   }

   return true;
}

bool FP_HookP02SequencePassesDrawFilter(const FP_HookPhase02Config &cfg,
                                        const FP_HookPhase02Sequence &seq)
{
   if(!seq.valid)
      return false;

   if(!seq.render_eligible)
      return false;

   if(cfg.min_x_count_to_draw > 0 && seq.x_count < cfg.min_x_count_to_draw)
      return false;

   if(cfg.sequence_draw_direction != 0 && (int)seq.direction != cfg.sequence_draw_direction)
      return false;

   if(cfg.sequence_draw_scale_l > 0 && seq.scale_l != cfg.sequence_draw_scale_l)
      return false;

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

   int m = ArraySize(indexes);
   for(int a=0; a<m/2; a++)
   {
      int b = m - 1 - a;
      int tmp = indexes[a];
      indexes[a] = indexes[b];
      indexes[b] = tmp;
   }
}

int FP_HookP02DrawOriginGroupEnvelopes(const FP_HookPhase02Config &cfg,
                                       const FP_HookPhase02Sequence &sequences[],
                                       const int &indexes[],
                                       FP_HookPhase02Report &report)
{
   if(!cfg.draw_cycle_arc)
      return 0;

   int arcs_drawn = 0;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      FP_HookPhase02Sequence seed = sequences[i];
      if(FP_HookP02GroupSeenBefore(seed, sequences, indexes, s))
         continue;

      datetime start_time, crown_time, end_time;
      double start_price, crown_price, end_price;
      if(!FP_HookP02GetOriginGroupEnvelope(seed, sequences, indexes,
                                           start_time, start_price,
                                           crown_time, crown_price,
                                           end_time, end_price))
         continue;

      string base = cfg.object_prefix + "HOOKENV_L" + IntegerToString(seed.scale_l) +
                    "_D" + IntegerToString((int)seed.direction) +
                    "_O" + IntegerToString(seed.origin_node_id);

      color arc_color = (cfg.cycle_arc_use_sequence_color ? FP_HookP02SequenceColor(cfg, seed) : cfg.cycle_arc_color);
      if(FP_HookP02CreateHookEnvelopeCurve(base, start_time, start_price,
                                           crown_time, crown_price,
                                           end_time, end_price,
                                           arc_color, cfg.line_width, report))
         arcs_drawn++;
   }

   return arcs_drawn;
}


int FP_HookP02BranchOrdinalInOriginGroup(const FP_HookPhase02Sequence &sequences[],
                                         const int &indexes[],
                                         const int selected_slot)
{
   if(selected_slot < 0 || selected_slot >= ArraySize(indexes))
      return 0;

   int current_index = indexes[selected_slot];
   if(current_index < 0 || current_index >= ArraySize(sequences))
      return 0;

   FP_HookPhase02Sequence current = sequences[current_index];
   int ordinal = 1;
   for(int s=0; s<selected_slot; s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;
      if(FP_HookP02SameOriginGroup(current, sequences[i]))
         ordinal++;
   }
   return ordinal;
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

   FP_HookP02DrawOriginGroupEnvelopes(cfg, sequences, indexes, report);

   int drawn = 0;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      int branch_ordinal = FP_HookP02BranchOrdinalInOriginGroup(sequences, indexes, s);
      if(FP_HookP02DrawOneSequenceNumbers(cfg, sequences[i], branch_ordinal, report))
         drawn++;
   }

   report.sequences_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE02_VISUAL_MQH__
