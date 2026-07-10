//+------------------------------------------------------------------+
//| CGWF_Splitter.mqh                                                |
//| Phase 11 — Time-ordered walk-forward split builder               |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_SPLITTER_MQH__
#define __CGWF_SPLITTER_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>

class CCGWF_Splitter
{
private:
   int CountRowsInWindow(SCGWFModelRow &rows[], const datetime start_t, const datetime end_t)
   {
      int count = 0;
      for(int i=0;i<ArraySize(rows);i++)
         if(rows[i].confirmation_time >= start_t && rows[i].confirmation_time < end_t)
            count++;
      return count;
   }

public:
   void SortByTime(SCGWFModelRow &rows[])
   {
      int n = ArraySize(rows);
      for(int i=0;i<n-1;i++)
      {
         int best = i;
         for(int j=i+1;j<n;j++)
            if(rows[j].confirmation_time < rows[best].confirmation_time)
               best = j;
         if(best != i)
         {
            SCGWFModelRow tmp = rows[i];
            rows[i] = rows[best];
            rows[best] = tmp;
         }
      }
   }

   bool BuildFolds(SCGWFModelRow &rows[], const SCGWFConfig &cfg, SCGWFFold &folds[], string &diagnostic)
   {
      ArrayResize(folds,0);
      diagnostic = "";
      int n = ArraySize(rows);
      if(n <= 0)
      {
         diagnostic = "no_rows_for_walk_forward";
         return false;
      }

      SortByTime(rows);
      datetime first_t = rows[0].confirmation_time;
      datetime last_t = rows[n-1].confirmation_time;
      int train_sec = MathMax(1,cfg.train_days) * 86400;
      int test_sec = MathMax(1,cfg.test_days) * 86400;
      int step_sec = MathMax(1,cfg.step_days) * 86400;
      int embargo_sec = MathMax(0,cfg.embargo_days) * 86400;

      datetime start_t = first_t;
      int fold_id = 1;
      while(start_t + train_sec + embargo_sec + test_sec <= last_t + 60)
      {
         SCGWFFold f;
         f.fold_id = fold_id;
         f.train_start = start_t;
         f.train_end = start_t + train_sec;
         f.embargo_start = f.train_end;
         f.embargo_end = f.train_end + embargo_sec;
         f.test_start = f.embargo_end;
         f.test_end = f.test_start + test_sec;
         f.train_count = CountRowsInWindow(rows,f.train_start,f.train_end);
         f.test_count = CountRowsInWindow(rows,f.test_start,f.test_end);
         f.usable = (f.train_count >= cfg.minimum_train_rows && f.test_count >= cfg.minimum_test_rows);
         f.status = f.usable ? "usable" : "insufficient_sample";

         int m = ArraySize(folds);
         ArrayResize(folds,m+1);
         folds[m] = f;

         fold_id++;
         start_t += step_sec;
         if(fold_id > 10000) break;
      }

      diagnostic = "folds_built=" + IntegerToString(ArraySize(folds)) + ";first=" + CGWF_Dt(first_t) + ";last=" + CGWF_Dt(last_t);
      return (ArraySize(folds) > 0);
   }
};

#endif
