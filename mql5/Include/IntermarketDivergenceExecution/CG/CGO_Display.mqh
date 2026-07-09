#ifndef __CGO_DISPLAY_MQH__
#define __CGO_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGO_Types.mqh>

class CCGO_Display
{
public:
   string BuildSummary(SCGOStudySummary &s)
   {
      string text="EXP0017 Phase07 Outcome Study\n";
      text+=StringFormat("observations=%d confirmed=%d ready=%d written=%d duplicate=%d\n",s.observations,s.confirmed_signals_seen,s.rows_ready,s.rows_written,s.rows_duplicate);
      text+=StringFormat("missing=%d pending=%d zero_risk=%d buys=%d sells=%d stops=%d\n",s.rows_missing_data,s.rows_pending_future,s.rows_zero_risk,s.buy_rows,s.sell_rows,s.stop_hit_rows);
      if(s.rows_ready>0)
         text+=StringFormat("avg_cycle_end_R=%.3f avg_day_end_R=%.3f avg_MFE_R=%.3f",s.average_cycle_end_r,s.average_day_end_r,s.average_mfe_r);
      return text;
   }
};

#endif
