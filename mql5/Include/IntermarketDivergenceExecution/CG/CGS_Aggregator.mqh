//+------------------------------------------------------------------+
//| CGS_Aggregator.mqh                                               |
//| EXP0017 Phase 08 — Statistical Aggregator                        |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_AGGREGATOR_MQH__
#define __EXP0017_CGS_AGGREGATOR_MQH__

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>

class CCGS_Aggregator
{
private:
   ECGSOutcomeWindow m_window;

   double OutcomeR(const SCGSOutcomeSample &s) const
   {
      if(m_window == CGS_WINDOW_CYCLE_END)      return s.cycle_end_r;
      if(m_window == CGS_WINDOW_PLUS_1_CYCLE)   return s.plus1_r;
      if(m_window == CGS_WINDOW_PLUS_2_CYCLE)   return s.plus2_r;
      if(m_window == CGS_WINDOW_PLUS_3_CYCLE)   return s.plus3_r;
      if(m_window == CGS_WINDOW_DAY_END)        return s.day_end_r;
      if(m_window == CGS_WINDOW_MFE)            return s.mfe_r;
      return s.cycle_end_r;
   }

   double OutcomePoints(const SCGSOutcomeSample &s) const
   {
      if(m_window == CGS_WINDOW_CYCLE_END)      return s.cycle_end_points;
      if(m_window == CGS_WINDOW_PLUS_1_CYCLE)   return s.plus1_points;
      if(m_window == CGS_WINDOW_PLUS_2_CYCLE)   return s.plus2_points;
      if(m_window == CGS_WINDOW_PLUS_3_CYCLE)   return s.plus3_points;
      if(m_window == CGS_WINDOW_DAY_END)        return s.day_end_points;
      if(m_window == CGS_WINDOW_MFE)            return s.mfe_points;
      return s.cycle_end_points;
   }

   double OutcomeNorm(const SCGSOutcomeSample &s) const
   {
      if(m_window == CGS_WINDOW_MFE)
         return s.mfe_normalized;
      if(m_window == CGS_WINDOW_DAY_END)
         return s.day_end_normalized;
      return CGS_SafeDiv(OutcomePoints(s), s.daily_range_points);
   }

   int FindGroup(const string key, SCGSGroupStats &groups[]) const
   {
      for(int i=0;i<ArraySize(groups);i++)
      {
         if(groups[i].key == key)
            return i;
      }
      return -1;
   }

   void InitGroup(SCGSGroupStats &g,const string dimension,const string key)
   {
      g.key = key;
      g.dimension_name = dimension;
      g.sample_count = 0;
      g.win_count = 0;
      g.loss_count = 0;
      g.zero_count = 0;
      g.stop_count = 0;
      g.sum_r = 0.0;
      g.sum_points = 0.0;
      g.sum_norm = 0.0;
      g.sum_mfe_r = 0.0;
      g.sum_mae_r = 0.0;
      g.sum_stop_distance = 0.0;
      g.max_r = -999999.0;
      g.min_r = 999999.0;
      g.max_points = -999999999.0;
      g.min_points = 999999999.0;
      g.current_stop_streak = 0;
      g.max_stop_streak = 0;
   }

public:
   void SetWindow(const ECGSOutcomeWindow window)
   {
      m_window = window;
   }

   void AddSample(const string dimension,const string key,const SCGSOutcomeSample &s,SCGSGroupStats &groups[])
   {
      if(key == "")
         return;

      int idx = FindGroup(key, groups);
      if(idx < 0)
      {
         int size = ArraySize(groups);
         ArrayResize(groups, size+1);
         InitGroup(groups[size], dimension, key);
         idx = size;
      }

      double r   = OutcomeR(s);
      double pts = OutcomePoints(s);
      double norm= OutcomeNorm(s);

      SCGSGroupStats g = groups[idx];
      g.sample_count++;
      if(r > 0.0)       g.win_count++;
      else if(r < 0.0)  g.loss_count++;
      else              g.zero_count++;

      if(s.stop_hit)
      {
         g.stop_count++;
         g.current_stop_streak++;
         if(g.current_stop_streak > g.max_stop_streak)
            g.max_stop_streak = g.current_stop_streak;
      }
      else
      {
         g.current_stop_streak = 0;
      }

      g.sum_r += r;
      g.sum_points += pts;
      g.sum_norm += norm;
      g.sum_mfe_r += s.mfe_r;
      g.sum_mae_r += s.mae_r;
      g.sum_stop_distance += s.stop_distance_points;

      if(r > g.max_r) g.max_r = r;
      if(r < g.min_r) g.min_r = r;
      if(pts > g.max_points) g.max_points = pts;
      if(pts < g.min_points) g.min_points = pts;

      groups[idx] = g;
   }

   void BuildOverall(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("overall", "ALL", samples[i], groups);
   }

   void BuildByCG(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("cg", samples[i].cg_name, samples[i], groups);
   }

   void BuildByDirection(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("direction", samples[i].direction, samples[i], groups);
   }

   void BuildByCGDirection(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("cg_direction", samples[i].cg_name + "|" + samples[i].direction, samples[i], groups);
   }

   void BuildByRole(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("role", samples[i].role_key, samples[i], groups);
   }

   void BuildByCGDirectionRole(SCGSOutcomeSample &samples[],SCGSGroupStats &groups[])
   {
      ArrayResize(groups,0);
      for(int i=0;i<ArraySize(samples);i++)
         AddSample("cg_direction_role", samples[i].cg_name + "|" + samples[i].direction + "|" + samples[i].role_key, samples[i], groups);
   }
};

#endif
