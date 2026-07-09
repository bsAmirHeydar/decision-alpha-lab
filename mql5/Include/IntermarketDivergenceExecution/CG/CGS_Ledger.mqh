//+------------------------------------------------------------------+
//| CGS_Ledger.mqh                                                   |
//| EXP0017 Phase 08 — Report CSV Writer                             |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_LEDGER_MQH__
#define __EXP0017_CGS_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>

class CCGS_ReportWriter
{
private:
   int OpenWrite(const string file_name,const bool common_folder)
   {
      int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
      if(common_folder)
         flags |= FILE_COMMON;
      return FileOpen(file_name, flags, ',');
   }

   void WriteStatsHeader(const int h)
   {
      FileWrite(h,
         "dimension","key","sample_count","win_count","loss_count","zero_count","win_rate_percent",
         "stop_count","stop_rate_percent","max_stop_streak","avg_r","avg_points","avg_normalized",
         "avg_mfe_r","avg_mae_r","avg_stop_distance_points","max_r","min_r","max_points","min_points");
   }

   void WriteStatsRow(const int h,const SCGSGroupStats &g)
   {
      double count = (double)MathMax(g.sample_count,1);
      FileWrite(h,
         g.dimension_name,
         g.key,
         g.sample_count,
         g.win_count,
         g.loss_count,
         g.zero_count,
         DoubleToString(CGS_SafeDiv(g.win_count*100.0,count),2),
         g.stop_count,
         DoubleToString(CGS_SafeDiv(g.stop_count*100.0,count),2),
         g.max_stop_streak,
         DoubleToString(CGS_SafeDiv(g.sum_r,count),4),
         DoubleToString(CGS_SafeDiv(g.sum_points,count),2),
         DoubleToString(CGS_SafeDiv(g.sum_norm,count),6),
         DoubleToString(CGS_SafeDiv(g.sum_mfe_r,count),4),
         DoubleToString(CGS_SafeDiv(g.sum_mae_r,count),4),
         DoubleToString(CGS_SafeDiv(g.sum_stop_distance,count),2),
         DoubleToString(g.max_r,4),
         DoubleToString(g.min_r,4),
         DoubleToString(g.max_points,2),
         DoubleToString(g.min_points,2));
   }

public:
   bool WriteStatsFile(const string file_name,const bool common_folder,SCGSGroupStats &groups[])
   {
      int h = OpenWrite(file_name, common_folder);
      if(h == INVALID_HANDLE)
      {
         Print("EXP0017 Phase08: cannot write report: ", file_name, " error=", GetLastError());
         return false;
      }
      WriteStatsHeader(h);
      for(int i=0;i<ArraySize(groups);i++)
         WriteStatsRow(h, groups[i]);
      FileClose(h);
      return true;
   }

   bool WriteRedFlags(const string file_name,const bool common_folder,SCGSGroupStats &groups[],const SCGSReportConfig &cfg)
   {
      int h = OpenWrite(file_name, common_folder);
      if(h == INVALID_HANDLE)
      {
         Print("EXP0017 Phase08: cannot write red-flag report: ", file_name, " error=", GetLastError());
         return false;
      }
      FileWrite(h,"dimension","key","sample_count","flag_type","value","threshold","note");
      for(int i=0;i<ArraySize(groups);i++)
      {
         SCGSGroupStats g = groups[i];
         if(g.sample_count < cfg.minimum_sample_for_flag)
            continue;

         double count = (double)MathMax(g.sample_count,1);
         double winrate = CGS_SafeDiv(g.win_count*100.0,count);
         double avg_r = CGS_SafeDiv(g.sum_r,count);

         if(winrate <= cfg.bad_winrate_threshold_percent)
            FileWrite(h,g.dimension_name,g.key,g.sample_count,"bad_win_rate",DoubleToString(winrate,2),DoubleToString(cfg.bad_winrate_threshold_percent,2),"win rate below threshold");

         if(avg_r <= cfg.bad_average_r_threshold)
            FileWrite(h,g.dimension_name,g.key,g.sample_count,"bad_average_r",DoubleToString(avg_r,4),DoubleToString(cfg.bad_average_r_threshold,4),"average R below threshold");

         if(g.max_stop_streak >= cfg.bad_stop_streak_threshold)
            FileWrite(h,g.dimension_name,g.key,g.sample_count,"stop_streak",g.max_stop_streak,cfg.bad_stop_streak_threshold,"max stop streak above threshold");
      }
      FileClose(h);
      return true;
   }
};

#endif
