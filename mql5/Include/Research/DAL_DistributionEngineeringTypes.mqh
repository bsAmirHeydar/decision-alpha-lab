#ifndef __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__
#define __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__

// Decision Alpha Lab
// Distribution Engineering / Conditional Sequence Extraction
// MQL5-only reusable research types.

struct DAL_DETradeOutcome
{
   string          strategy_id;
   string          symbol;
   ENUM_TIMEFRAMES timeframe;
   int             direction;          // +1 buy, -1 sell, 0 unknown

   datetime        entry_time;
   datetime        exit_time;

   double          entry_price;
   double          stop_price;
   double          target_price;

   double          r_result;           // realized result in R units
   double          mfe_r;              // maximum favorable excursion in R
   double          mae_r;              // maximum adverse excursion in R
   int             bars_to_exit;

   bool            is_win;             // true if target/win condition was reached
   bool            is_loss;            // true if stop/loss condition was reached

   string          feature_key;         // causal regime/filter key built before entry
   string          note;
};

void DAL_DETradeOutcome_Reset(DAL_DETradeOutcome &o)
{
   o.strategy_id   = "";
   o.symbol        = "";
   o.timeframe     = PERIOD_CURRENT;
   o.direction     = 0;

   o.entry_time    = 0;
   o.exit_time     = 0;

   o.entry_price   = 0.0;
   o.stop_price    = 0.0;
   o.target_price  = 0.0;

   o.r_result      = 0.0;
   o.mfe_r         = 0.0;
   o.mae_r         = 0.0;
   o.bars_to_exit  = 0;

   o.is_win        = false;
   o.is_loss       = false;

   o.feature_key   = "UNSPECIFIED";
   o.note          = "";
}

struct DAL_DEClusterStats
{
   string key;

   int    total;
   int    wins;
   int    losses;

   double sum_r;
   double sum_mfe_r;
   double sum_mae_r;

   int    current_win_streak;
   int    max_win_streak;

   int    clusters_ge_3;
   int    clusters_ge_5;
   int    clusters_ge_7;
   int    clusters_ge_10;

   int    opp_after_1_win;
   int    win_after_1_win;

   int    opp_after_2_wins;
   int    win_after_2_wins;

   int    opp_after_3_wins;
   int    win_after_3_wins;

   int    min_bars_to_exit;
   int    max_bars_to_exit;
};

void DAL_DEClusterStats_Reset(DAL_DEClusterStats &s, const string key = "ALL")
{
   s.key = key;

   s.total  = 0;
   s.wins   = 0;
   s.losses = 0;

   s.sum_r     = 0.0;
   s.sum_mfe_r = 0.0;
   s.sum_mae_r = 0.0;

   s.current_win_streak = 0;
   s.max_win_streak     = 0;

   s.clusters_ge_3  = 0;
   s.clusters_ge_5  = 0;
   s.clusters_ge_7  = 0;
   s.clusters_ge_10 = 0;

   s.opp_after_1_win = 0;
   s.win_after_1_win = 0;

   s.opp_after_2_wins = 0;
   s.win_after_2_wins = 0;

   s.opp_after_3_wins = 0;
   s.win_after_3_wins = 0;

   s.min_bars_to_exit = 0;
   s.max_bars_to_exit = 0;
}

#endif // __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__
