#ifndef __FP_HOOK_PHASE02_VISUAL_MQH__
#define __FP_HOOK_PHASE02_VISUAL_MQH__
#property strict

#include "FP_HookPhase02Rules.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

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
int      g_fp_hook_p02_label_cluster_shifts[];
double   g_fp_hook_p02_label_cluster_prices[];
int      g_fp_hook_p02_label_cluster_sides[];
int      g_fp_hook_p02_label_counts[];

datetime g_fp_hook_p02_bar_shift_cache_times[];
int      g_fp_hook_p02_bar_shift_cache_values[];
int      g_fp_hook_p02_range_cache_shifts[];
int      g_fp_hook_p02_range_cache_lookbacks[];
double   g_fp_hook_p02_range_cache_values[];

int FP_HookPhase02DeleteObjects(const string prefix)
{
   return AL_UC04DeleteObjectsByPrefix(0, prefix);
}

void FP_HookP02ResetLabelCollisionState()
{
   ArrayResize(g_fp_hook_p02_label_cluster_times, 0);
   ArrayResize(g_fp_hook_p02_label_cluster_shifts, 0);
   ArrayResize(g_fp_hook_p02_label_cluster_prices, 0);
   ArrayResize(g_fp_hook_p02_label_cluster_sides, 0);
   ArrayResize(g_fp_hook_p02_label_counts, 0);
   ArrayResize(g_fp_hook_p02_bar_shift_cache_times, 0);
   ArrayResize(g_fp_hook_p02_bar_shift_cache_values, 0);
   ArrayResize(g_fp_hook_p02_range_cache_shifts, 0);
   ArrayResize(g_fp_hook_p02_range_cache_lookbacks, 0);
   ArrayResize(g_fp_hook_p02_range_cache_values, 0);
}

int FP_HookP02BarShiftFromTime(const datetime t)
{
   if(t <= 0)
      return -1;

   for(int i=0; i<ArraySize(g_fp_hook_p02_bar_shift_cache_times); i++)
   {
      if(g_fp_hook_p02_bar_shift_cache_times[i] == t)
         return g_fp_hook_p02_bar_shift_cache_values[i];
   }

   int shift = iBarShift(_Symbol, _Period, t, false);
   if(shift < 0)
      shift = iBarShift(_Symbol, _Period, t, true);

   int n = ArraySize(g_fp_hook_p02_bar_shift_cache_times);
   ArrayResize(g_fp_hook_p02_bar_shift_cache_times, n + 1);
   ArrayResize(g_fp_hook_p02_bar_shift_cache_values, n + 1);
   g_fp_hook_p02_bar_shift_cache_times[n] = t;
   g_fp_hook_p02_bar_shift_cache_values[n] = shift;
   return shift;
}

datetime FP_HookP02TimeFromBarShift(const int shift)
{
   if(shift < 0)
      return 0;
   return iTime(_Symbol, _Period, shift);
}

int FP_HookP02ClampNonNegative(const int value)
{
   if(value < 0)
      return 0;
   return value;
}

int FP_HookP02ConsumeLabelStackSlot(const FP_HookPhase02Config &cfg,
                                    const datetime t,
                                    const double price,
                                    const bool place_below)
{
   int side = (place_below ? 1 : 0);
   int anchor_shift = FP_HookP02BarShiftFromTime(t);

   int time_window_seconds = cfg.label_time_cluster_seconds;
   if(time_window_seconds < 0)
      time_window_seconds = 0;

   int time_window_bars = cfg.label_time_cluster_bars;
   if(time_window_bars < 0)
      time_window_bars = 0;

   int price_window_points = cfg.label_price_cluster_points;
   if(price_window_points <= 0)
      price_window_points = 24;

   for(int i=0; i<ArraySize(g_fp_hook_p02_label_cluster_times); i++)
   {
      if(g_fp_hook_p02_label_cluster_sides[i] != side)
         continue;

      bool time_match = false;
      if(anchor_shift >= 0 && g_fp_hook_p02_label_cluster_shifts[i] >= 0)
      {
         int dbar = MathAbs(anchor_shift - g_fp_hook_p02_label_cluster_shifts[i]);
         if(dbar <= time_window_bars)
            time_match = true;
      }

      if(!time_match)
      {
         double dt = MathAbs((double)((long)t - (long)g_fp_hook_p02_label_cluster_times[i]));
         if(dt <= (double)time_window_seconds)
            time_match = true;
      }

      if(!time_match)
         continue;

      double dp = MathAbs(price - g_fp_hook_p02_label_cluster_prices[i]);
      if(dp > _Point * (double)price_window_points)
         continue;

      int slot = g_fp_hook_p02_label_counts[i];
      g_fp_hook_p02_label_counts[i] = slot + 1;
      return slot;
   }

   int n = ArraySize(g_fp_hook_p02_label_cluster_times);
   ArrayResize(g_fp_hook_p02_label_cluster_times, n + 1);
   ArrayResize(g_fp_hook_p02_label_cluster_shifts, n + 1);
   ArrayResize(g_fp_hook_p02_label_cluster_prices, n + 1);
   ArrayResize(g_fp_hook_p02_label_cluster_sides, n + 1);
   ArrayResize(g_fp_hook_p02_label_counts, n + 1);
   g_fp_hook_p02_label_cluster_times[n] = t;
   g_fp_hook_p02_label_cluster_shifts[n] = anchor_shift;
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
                                  const string fallback_label,
                                  const string family_tag)
{
   string core = FP_HookP02NodeDisplayLabel(cfg, point_index, fallback_label);
   if(StringLen(core) <= 0)
      return "";

   string label = core;
   if(cfg.show_hook_sequence_ids_in_labels)
   {
      int branch_id = branch_ordinal;
      if(branch_id <= 0)
         branch_id = seq.sequence_id;

      label = "H" + IntegerToString(seq.origin_node_id) + "B" + IntegerToString(branch_id) + ":" + core;
   }

   if(cfg.show_only_valid_hooks && StringLen(family_tag) > 0)
      return family_tag + " " + label;

   return label;
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

int FP_HookP02ClampPoints(const int value,
                             const int min_value,
                             const int max_value)
{
   int v = value;
   if(v < min_value)
      v = min_value;
   if(max_value > 0 && v > max_value)
      v = max_value;
   return v;
}

double FP_HookP02AverageLocalBarRangePoints(const int anchor_shift,
                                            const int lookback_bars)
{
   if(anchor_shift < 0)
      return 0.0;

   int lookback = lookback_bars;
   if(lookback <= 0)
      lookback = 12;

   for(int c=0; c<ArraySize(g_fp_hook_p02_range_cache_shifts); c++)
   {
      if(g_fp_hook_p02_range_cache_shifts[c] == anchor_shift &&
         g_fp_hook_p02_range_cache_lookbacks[c] == lookback)
         return g_fp_hook_p02_range_cache_values[c];
   }

   int bars_total = Bars(_Symbol, _Period);
   if(bars_total <= 0)
      return 0.0;

   int end_shift = anchor_shift + lookback - 1;
   if(end_shift >= bars_total)
      end_shift = bars_total - 1;

   int count = 0;
   double sum_points = 0.0;
   for(int shift = anchor_shift; shift <= end_shift; shift++)
   {
      double hi = iHigh(_Symbol, _Period, shift);
      double lo = iLow(_Symbol, _Period, shift);
      if(hi <= 0.0 || lo <= 0.0 || hi < lo)
         continue;
      sum_points += (hi - lo) / _Point;
      count++;
   }

   double value = 0.0;
   if(count > 0)
      value = sum_points / (double)count;

   int n = ArraySize(g_fp_hook_p02_range_cache_shifts);
   ArrayResize(g_fp_hook_p02_range_cache_shifts, n + 1);
   ArrayResize(g_fp_hook_p02_range_cache_lookbacks, n + 1);
   ArrayResize(g_fp_hook_p02_range_cache_values, n + 1);
   g_fp_hook_p02_range_cache_shifts[n] = anchor_shift;
   g_fp_hook_p02_range_cache_lookbacks[n] = lookback;
   g_fp_hook_p02_range_cache_values[n] = value;

   return value;
}

void FP_HookP02ResolveResponsiveLabelDistances(const FP_HookPhase02Config &cfg,
                                               const datetime anchor_time,
                                               int &base_points,
                                               int &step_points)
{
   base_points = cfg.node_number_offset_points;
   step_points = cfg.node_label_stack_step_points;

   if(base_points < 0)
      base_points = 0;
   if(step_points < 0)
      step_points = 0;

   if(!cfg.responsive_label_offsets)
      return;

   int anchor_shift = FP_HookP02BarShiftFromTime(anchor_time);
   double avg_range_points = FP_HookP02AverageLocalBarRangePoints(anchor_shift, cfg.responsive_label_lookback_bars);
   if(avg_range_points <= 0.0)
      return;

   int dynamic_base = (int)MathRound(avg_range_points * cfg.responsive_label_offset_range_ratio);
   int dynamic_step = (int)MathRound(avg_range_points * cfg.responsive_label_step_range_ratio);

   dynamic_base = FP_HookP02ClampPoints(dynamic_base,
                                        cfg.responsive_label_min_offset_points,
                                        cfg.responsive_label_max_offset_points);
   dynamic_step = FP_HookP02ClampPoints(dynamic_step,
                                        cfg.responsive_label_min_step_points,
                                        cfg.responsive_label_max_step_points);

   // Keep manual values as absolute floors if the operator wants larger spacing.
   if(dynamic_base < base_points)
      dynamic_base = base_points;
   if(dynamic_step < step_points)
      dynamic_step = step_points;

   base_points = dynamic_base;
   step_points = dynamic_step;
}

double FP_HookP02StackedLabelPrice(const FP_HookPhase02Config &cfg,
                                   const datetime anchor_time,
                                   const double anchor_price,
                                   const bool place_below,
                                   const int stack_slot)
{
   int base_points, step_points;
   FP_HookP02ResolveResponsiveLabelDistances(cfg, anchor_time, base_points, step_points);

   double stack_points = 0.0;
   if(cfg.stack_node_labels_on_collisions && stack_slot > 0 && step_points > 0)
      stack_points = (double)(stack_slot * step_points);

   double total_points = (double)base_points + stack_points;
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

bool FP_HookP02ValidOnlyRequiresSemanticReadiness(const FP_HookPhase02Config &cfg)
{
   if(!cfg.show_only_valid_hooks)
      return true;
   return cfg.valid_only_require_near_death;
}

bool FP_HookP02SequenceStructurallyDrawable(const FP_HookPhase02Config &cfg,
                                            const FP_HookPhase02Sequence &seq)
{
   if(!seq.valid)
      return false;
   if(seq.hook_failed)
      return false;

   if(FP_HookP02ValidOnlyRequiresSemanticReadiness(cfg))
   {
      if(!seq.render_eligible)
         return false;
   }

   return true;
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

bool FP_HookP02GetOriginGroupEnvelope(const FP_HookPhase02Config &cfg,
                                      const FP_HookPhase02Sequence &seed,
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

   bool require_semantic = FP_HookP02ValidOnlyRequiresSemanticReadiness(cfg);

   if(start_time <= 0 || !seed.valid || seed.hook_failed)
      return false;
   if(require_semantic && (!seed.render_eligible || !seed.near_death_confirmed))
      return false;

   bool crown_found = false;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;
      FP_HookPhase02Sequence seq = sequences[i];
      if(!seq.valid || seq.hook_failed)
         continue;
      if(require_semantic && (!seq.render_eligible || !seq.near_death_confirmed))
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
      if(!seq.valid || seq.hook_failed)
         continue;
      if(require_semantic && (!seq.render_eligible || !seq.near_death_confirmed))
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
                                       const FP_HookPhase02Config &cfg,
                                       FP_HookPhase02Report &report)
{
   if(start_time <= 0 || crown_time <= start_time || end_time <= crown_time)
      return false;

   if(cfg.cycle_arc_align_to_bar_index)
   {
      int start_shift = FP_HookP02BarShiftFromTime(start_time);
      int crown_shift = FP_HookP02BarShiftFromTime(crown_time);
      int end_shift   = FP_HookP02BarShiftFromTime(end_time);

      if(start_shift >= 0 && crown_shift >= 0 && end_shift >= 0 && start_shift > crown_shift && crown_shift > end_shift)
      {
         datetime prev_t = start_time;
         double prev_p = start_price;
         bool has_prev = true;

         for(int shift = start_shift - 1; shift >= end_shift; shift--)
         {
            datetime cur_t = FP_HookP02TimeFromBarShift(shift);
            if(cur_t <= 0)
               continue;

            double u = 0.0;
            double cur_p = 0.0;
            if(shift >= crown_shift)
            {
               int total_a = start_shift - crown_shift;
               int done_a = start_shift - shift;
               if(total_a <= 0)
                  u = 1.0;
               else
                  u = (double)done_a / (double)total_a;
               if(u < 0.0) u = 0.0;
               if(u > 1.0) u = 1.0;
               double eased = MathSin(u * 1.5707963267948966);
               cur_p = start_price + (crown_price - start_price) * eased;
            }
            else
            {
               int total_b = crown_shift - end_shift;
               int done_b = crown_shift - shift;
               if(total_b <= 0)
                  u = 1.0;
               else
                  u = (double)done_b / (double)total_b;
               if(u < 0.0) u = 0.0;
               if(u > 1.0) u = 1.0;
               double eased = 1.0 - MathCos(u * 1.5707963267948966);
               cur_p = crown_price + (end_price - crown_price) * eased;
            }

            if(has_prev && cur_t > prev_t)
            {
               FP_HookP02CreateTrend(base + "_ENV_BAR_" + IntegerToString(shift),
                                     prev_t, prev_p, cur_t, cur_p,
                                     curve_color, line_width, STYLE_SOLID, report);
            }
            prev_t = cur_t;
            prev_p = cur_p;
            has_prev = true;
         }
         return true;
      }
   }

   int half_segments = 12;
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
                                      const string family_tag,
                                      const color family_color,
                                      FP_HookPhase02Report &report)
{
   if(!cfg.draw_x_nodes || !cfg.draw_labels)
      return true;

   string base = FP_HookP02BaseName(cfg, seq);
   color seq_color = family_color;
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

      string node_display = FP_HookP02FormattedNodeLabel(cfg, seq, branch_ordinal, p, label, family_tag);
      if(StringLen(node_display) <= 0)
         continue;

      color node_color = (cfg.color_node_labels_with_sequence ? seq_color : cfg.label_color);
      node_color = FP_HookP02NodeNumberColor(cfg, p, node_color);
      int stack_slot = (cfg.stack_node_labels_on_collisions ? FP_HookP02ConsumeLabelStackSlot(cfg, t, price, place_below) : 0);
      double label_price = FP_HookP02StackedLabelPrice(cfg, t, price, place_below, stack_slot);

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

bool FP_HookP02SequencePassesBaseDrawFilter(const FP_HookPhase02Config &cfg,
                                            const FP_HookPhase02Sequence &seq,
                                            const bool enforce_sequence_id)
{
   if(!FP_HookP02SequenceStructurallyDrawable(cfg, seq))
      return false;

   if(cfg.min_x_count_to_draw > 0 && seq.x_count < cfg.min_x_count_to_draw)
      return false;

   if(cfg.sequence_draw_direction != 0 && (int)seq.direction != cfg.sequence_draw_direction)
      return false;

   if(cfg.sequence_draw_scale_l > 0 && seq.scale_l != cfg.sequence_draw_scale_l)
      return false;

   if(enforce_sequence_id && cfg.sequence_draw_mode == FP_HOOK_P02_DRAW_BY_SEQUENCE_ID)
   {
      if(cfg.sequence_draw_sequence_id < 0)
         return false;
      if(seq.sequence_id != cfg.sequence_draw_sequence_id)
         return false;
   }

   return true;
}

bool FP_HookP02SequencePassesDrawFilter(const FP_HookPhase02Config &cfg,
                                        const FP_HookPhase02Sequence &seq)
{
   if(!FP_HookP02SequencePassesBaseDrawFilter(cfg, seq, true))
      return false;

   if(cfg.show_only_valid_hooks && !seq.valid_hook_family)
      return false;

   return true;
}

bool FP_HookP02IndexAlreadySelected(const int &indexes[],
                                    const int candidate_index)
{
   for(int i=0; i<ArraySize(indexes); i++)
   {
      if(indexes[i] == candidate_index)
         return true;
   }
   return false;
}

int FP_HookP02FindSequenceIndexBySequenceId(const FP_HookPhase02Sequence &sequences[],
                                            const int sequence_id)
{
   for(int i=0; i<ArraySize(sequences); i++)
   {
      if(sequences[i].sequence_id == sequence_id)
         return i;
   }
   return -1;
}


bool FP_HookP02IsParentCompanionInVisibleSet(const FP_HookPhase02Sequence &seq,
                                             const FP_HookPhase02Sequence &sequences[],
                                             const int &indexes[])
{
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      FP_HookPhase02Sequence child = sequences[i];
      if(!child.valid_after_hook)
         continue;
      if(child.previous_hook_sequence_id < 0)
         continue;
      if(child.previous_hook_sequence_id == seq.sequence_id)
         return true;
   }
   return false;
}

string FP_HookP02CanonicalFamilyTag(const FP_HookPhase02Config &cfg,
                                    const FP_HookPhase02Sequence &seq,
                                    const bool parent_companion)
{
   if(!cfg.show_only_valid_hooks)
      return "";

   if(seq.valid_after_hook && seq.valid_after_opposing_f3)
   {
      if(seq.post_f3_subfamily == "F3H_DIRECT_STRUCTURAL") return "F3H-D-S+HH";
      if(seq.post_f3_subfamily == "F3H_DIRECT_GEOMETRIC_80") return "F3H-D80+HH";
      if(seq.post_f3_subfamily == "F3H_DELAYED_STRUCTURAL") return "F3H-R-S+HH";
      if(seq.post_f3_subfamily == "F3H_DELAYED_GEOMETRIC_80") return "F3H-R80+HH";
      return "F3H+HH";
   }
   if(seq.valid_after_opposing_f3)
   {
      if(seq.post_f3_subfamily == "F3H_DIRECT_STRUCTURAL") return "F3H-D-S";
      if(seq.post_f3_subfamily == "F3H_DIRECT_GEOMETRIC_80") return "F3H-D80";
      if(seq.post_f3_subfamily == "F3H_DELAYED_STRUCTURAL") return "F3H-R-S";
      if(seq.post_f3_subfamily == "F3H_DELAYED_GEOMETRIC_80") return "F3H-R80";
      return "F3H";
   }
   if(seq.valid_after_hook)
      return "HH";
   if(parent_companion)
      return "PARENT";

   return "";
}

color FP_HookP02CanonicalFamilyColor(const FP_HookPhase02Config &cfg,
                                     const FP_HookPhase02Sequence &seq,
                                     const bool parent_companion,
                                     const color fallback_color)
{
   if(!cfg.show_only_valid_hooks)
      return fallback_color;

   // Canonical production-view colors:
   // F3H    = Hook after opposing F3
   // HH     = second Hook after a same-genus Hook
   // PARENT = first Hook shown only as the required companion of HH
   if(seq.valid_after_hook && seq.valid_after_opposing_f3)
      return clrGold;
   if(seq.valid_after_opposing_f3)
   {
      if(seq.post_f3_subfamily == "F3H_DIRECT_STRUCTURAL") return clrMediumSeaGreen;
      if(seq.post_f3_subfamily == "F3H_DIRECT_GEOMETRIC_80") return clrLimeGreen;
      if(seq.post_f3_subfamily == "F3H_DELAYED_STRUCTURAL") return clrDarkTurquoise;
      if(seq.post_f3_subfamily == "F3H_DELAYED_GEOMETRIC_80") return clrAqua;
      return clrMediumSeaGreen;
   }
   if(seq.valid_after_hook)
      return clrDeepSkyBlue;
   if(parent_companion)
      return clrSilver;

   return fallback_color;
}

void FP_HookP02SortSelectedIndexesBySequenceId(const FP_HookPhase02Sequence &sequences[],
                                               int &indexes[])
{
   int n = ArraySize(indexes);
   for(int i=0; i<n-1; i++)
   {
      for(int j=i+1; j<n; j++)
      {
         int ai = indexes[i];
         int bi = indexes[j];
         if(ai < 0 || ai >= ArraySize(sequences) || bi < 0 || bi >= ArraySize(sequences))
            continue;

         if(sequences[bi].sequence_id < sequences[ai].sequence_id)
         {
            int tmp = indexes[i];
            indexes[i] = indexes[j];
            indexes[j] = tmp;
         }
      }
   }
}

void FP_HookP02ExpandSelectionWithHookAfterHookParents(const FP_HookPhase02Config &cfg,
                                                      const FP_HookPhase02Sequence &sequences[],
                                                      int &indexes[])
{
   if(!cfg.show_only_valid_hooks)
      return;

   // Doctrine: when the visible valid family is Hook-after-Hook, the second
   // Hook is the valid Hook, but its immediately chained first Hook is part of
   // the readable structure. The first Hook is allowed into the production view
   // only as this required parent companion, not as an independent valid Hook.
   int original_count = ArraySize(indexes);
   for(int s=0; s<original_count; s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      FP_HookPhase02Sequence child = sequences[i];
      if(!child.valid_after_hook)
         continue;
      if(child.previous_hook_sequence_id < 0)
         continue;

      int parent_index = FP_HookP02FindSequenceIndexBySequenceId(sequences, child.previous_hook_sequence_id);
      if(parent_index < 0 || parent_index >= ArraySize(sequences))
         continue;
      if(FP_HookP02IndexAlreadySelected(indexes, parent_index))
         continue;

      FP_HookPhase02Sequence parent = sequences[parent_index];
      if(!FP_HookP02SequencePassesBaseDrawFilter(cfg, parent, false))
         continue;

      int k = ArraySize(indexes);
      ArrayResize(indexes, k + 1);
      indexes[k] = parent_index;
   }

   FP_HookP02SortSelectedIndexesBySequenceId(sequences, indexes);
}


void FP_HookP02ExpandSelectionWithSameHookGroupMembers(const FP_HookPhase02Config &cfg,
                                                       const FP_HookPhase02Sequence &sequences[],
                                                       int &indexes[])
{
   // Canon correction, Phase 47:
   // valid-only production is NOT an origin-group expansion view.
   // A selected valid Hook may draw only its own sequence row. The only
   // non-valid row allowed into the visible set is the explicit parent
   // companion of a valid Hook-after-Hook child, handled by
   // FP_HookP02ExpandSelectionWithHookAfterHookParents.
   //
   // The older origin-group expansion was the source of the chart leakage: once
   // one valid sequence in an origin group was selected, all sibling structural
   // sequences from that group were drawn and labelled. That is exactly what the
   // production canon forbids.
   return;
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

   if(cfg.show_only_valid_hooks && cfg.valid_only_fallback_to_structural && ArraySize(indexes) == 0)
   {
      // Debug-only fallback. Production doctrine is strict valid-only:
      // if no valid Hook family is selected, draw nothing. Turn this on only
      // when diagnosing why the valid-family annotator returned zero candidates.
      if(cfg.sequence_draw_mode == FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION)
      {
         int selected_scales_fb[];
         int selected_dirs_fb[];
         int selected_count_fb = 0;
         for(int i=n-1; i>=0 && ArraySize(indexes)<max_draw; i--)
         {
            if(!FP_HookP02SequencePassesBaseDrawFilter(cfg, sequences[i], true))
               continue;
            int dir = (int)sequences[i].direction;
            if(FP_HookP02AlreadySelectedScaleDirection(selected_scales_fb, selected_dirs_fb,
                                                       selected_count_fb,
                                                       sequences[i].scale_l, dir))
               continue;
            ArrayResize(selected_scales_fb, selected_count_fb + 1);
            ArrayResize(selected_dirs_fb, selected_count_fb + 1);
            selected_scales_fb[selected_count_fb] = sequences[i].scale_l;
            selected_dirs_fb[selected_count_fb] = dir;
            selected_count_fb++;

            int k = ArraySize(indexes);
            ArrayResize(indexes, k + 1);
            indexes[k] = i;
         }
      }
      else
      {
         for(int i=n-1; i>=0 && ArraySize(indexes)<max_draw; i--)
         {
            if(!FP_HookP02SequencePassesBaseDrawFilter(cfg, sequences[i], true))
               continue;
            int k = ArraySize(indexes);
            ArrayResize(indexes, k + 1);
            indexes[k] = i;
         }
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

   FP_HookP02ExpandSelectionWithHookAfterHookParents(cfg, sequences, indexes);
   FP_HookP02ExpandSelectionWithSameHookGroupMembers(cfg, sequences, indexes);
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
      if(!FP_HookP02GetOriginGroupEnvelope(cfg, seed, sequences, indexes,
                                           start_time, start_price,
                                           crown_time, crown_price,
                                           end_time, end_price))
         continue;

      string base = cfg.object_prefix + "HOOKENV_L" + IntegerToString(seed.scale_l) +
                    "_D" + IntegerToString((int)seed.direction) +
                    "_O" + IntegerToString(seed.origin_node_id);

      bool parent_companion = FP_HookP02IsParentCompanionInVisibleSet(seed, sequences, indexes);
      color base_arc_color = (cfg.cycle_arc_use_sequence_color ? FP_HookP02SequenceColor(cfg, seed) : cfg.cycle_arc_color);
      color arc_color = FP_HookP02CanonicalFamilyColor(cfg, seed, parent_companion, base_arc_color);
      if(FP_HookP02CreateHookEnvelopeCurve(base, start_time, start_price,
                                           crown_time, crown_price,
                                           end_time, end_price,
                                           arc_color, cfg.line_width, cfg, report))
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

   if(cfg.show_only_valid_hooks)
   {
      report.invalid_family_filtered = 0;
      for(int i=0; i<ArraySize(sequences); i++)
      {
         if(sequences[i].valid && sequences[i].render_eligible && !sequences[i].valid_hook_family)
            report.invalid_family_filtered++;
      }
   }

   int indexes[];
   FP_HookP02SelectSequenceIndexes(cfg, sequences, indexes);

   FP_HookP02DrawOriginGroupEnvelopes(cfg, sequences, indexes, report);

   int drawn = 0;
   for(int s=0; s<ArraySize(indexes); s++)
   {
      int i = indexes[s];
      if(i < 0 || i >= ArraySize(sequences))
         continue;

      bool parent_companion = FP_HookP02IsParentCompanionInVisibleSet(sequences[i], sequences, indexes);
      string family_tag = FP_HookP02CanonicalFamilyTag(cfg, sequences[i], parent_companion);
      color family_color = FP_HookP02CanonicalFamilyColor(cfg, sequences[i], parent_companion, FP_HookP02SequenceColor(cfg, sequences[i]));
      int branch_ordinal = FP_HookP02BranchOrdinalInOriginGroup(sequences, indexes, s);
      if(FP_HookP02DrawOneSequenceNumbers(cfg, sequences[i], branch_ordinal, family_tag, family_color, report))
         drawn++;
   }

   report.sequences_drawn = drawn;
   return drawn;
}

#endif // __FP_HOOK_PHASE02_VISUAL_MQH__
