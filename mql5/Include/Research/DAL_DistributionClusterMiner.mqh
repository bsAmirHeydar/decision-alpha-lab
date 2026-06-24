#ifndef __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__
#define __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__

#include <Research/DAL_DistributionEngineeringTypes.mqh>

// Decision Alpha Lab
// Distribution Cluster Miner
// Incremental, MQL5-only, no-order research module.
// It can be embedded into any execution EA by calling AddOutcome() after a
// completed real/probe trade outcome is known.

// -----------------------------------------------------------------------------
// Stats structs
// -----------------------------------------------------------------------------

struct DAL_DEClusterStats
{
   string key;

   int    total;
   int    wins;
   int    losses;
   int    flats;

   int    probe_total;
   int    probe_wins;
   int    probe_losses;

   int    live_total;
   int    live_wins;
   int    live_losses;

   int    buy_total;
   int    buy_wins;
   int    sell_total;
   int    sell_wins;

   double sum_r;
   double sum_r2;
   double min_r;
   double max_r;

   double sum_positive_r;
   double sum_negative_r;
   double sum_win_r;
   double sum_loss_r;

   double sum_mfe_r;
   double sum_mae_r;
   double max_mfe_r;
   double min_mae_r;

   double sum_bars_to_exit;
   double sum_seconds_to_exit;
   int    min_bars_to_exit;
   int    max_bars_to_exit;

   int    hour_total[24];
   int    hour_wins[24];

   int    r_bucket_count[DAL_DE_R_BUCKETS];

   int    current_win_streak;
   int    current_loss_streak;
   int    max_win_streak;
   int    max_loss_streak;

   // Count of win-runs that reached at least k.
   // A 7-win run increments clusters_ge[1..7] once each.
   int    clusters_ge[DAL_DE_K_SIZE];

   // Completed runs. Runs longer than max K are capped into index DAL_DE_MAX_K.
   int    completed_win_runs_exact[DAL_DE_K_SIZE];
   int    completed_loss_runs_exact[DAL_DE_K_SIZE];

   // Conditional sequence metrics.
   // opp_after_atleast[k] = count of trades that arrived after >=k consecutive wins.
   // win_after_atleast[k] = count of those trades that were wins.
   int    opp_after_atleast[DAL_DE_K_SIZE];
   int    win_after_atleast[DAL_DE_K_SIZE];
   int    loss_after_atleast[DAL_DE_K_SIZE];

   // Exact-run conditional metrics.
   // opp_after_exact[k] = count of trades that arrived after exactly k consecutive wins.
   int    opp_after_exact[DAL_DE_K_SIZE];
   int    win_after_exact[DAL_DE_K_SIZE];
   int    loss_after_exact[DAL_DE_K_SIZE];

   datetime first_entry_time;
   datetime last_exit_time;
};

struct DAL_DEClusterGroup
{
   string key;
   DAL_DEClusterStats stats;
};

struct DAL_DEClusterMiner
{
   string miner_id;
   string strategy_id;
   int    group_count;
   int    max_groups;
   bool   initialized;

   DAL_DEClusterStats all;
   DAL_DEClusterGroup groups[DAL_DE_MAX_GROUPS];
};

// -----------------------------------------------------------------------------
// Stats lifecycle
// -----------------------------------------------------------------------------

void DAL_DEClusterStats_Reset(DAL_DEClusterStats &s, const string key = "ALL")
{
   s.key = key;

   s.total  = 0;
   s.wins   = 0;
   s.losses = 0;
   s.flats  = 0;

   s.probe_total  = 0;
   s.probe_wins   = 0;
   s.probe_losses = 0;

   s.live_total   = 0;
   s.live_wins    = 0;
   s.live_losses  = 0;

   s.buy_total    = 0;
   s.buy_wins     = 0;
   s.sell_total   = 0;
   s.sell_wins    = 0;

   s.sum_r            = 0.0;
   s.sum_r2           = 0.0;
   s.min_r            = 0.0;
   s.max_r            = 0.0;
   s.sum_positive_r   = 0.0;
   s.sum_negative_r   = 0.0;
   s.sum_win_r        = 0.0;
   s.sum_loss_r       = 0.0;

   s.sum_mfe_r        = 0.0;
   s.sum_mae_r        = 0.0;
   s.max_mfe_r        = 0.0;
   s.min_mae_r        = 0.0;

   s.sum_bars_to_exit    = 0.0;
   s.sum_seconds_to_exit = 0.0;
   s.min_bars_to_exit    = 0;
   s.max_bars_to_exit    = 0;

   for(int h = 0; h < 24; h++)
   {
      s.hour_total[h] = 0;
      s.hour_wins[h]  = 0;
   }

   for(int b = 0; b < DAL_DE_R_BUCKETS; b++)
      s.r_bucket_count[b] = 0;

   s.current_win_streak  = 0;
   s.current_loss_streak = 0;
   s.max_win_streak      = 0;
   s.max_loss_streak     = 0;

   for(int k = 0; k < DAL_DE_K_SIZE; k++)
   {
      s.clusters_ge[k]              = 0;
      s.completed_win_runs_exact[k] = 0;
      s.completed_loss_runs_exact[k]= 0;
      s.opp_after_atleast[k]        = 0;
      s.win_after_atleast[k]        = 0;
      s.loss_after_atleast[k]       = 0;
      s.opp_after_exact[k]          = 0;
      s.win_after_exact[k]          = 0;
      s.loss_after_exact[k]         = 0;
   }

   s.first_entry_time = 0;
   s.last_exit_time   = 0;
}

void DAL_DEClusterStats_Copy(const DAL_DEClusterStats &src, DAL_DEClusterStats &dst)
{
   dst.key = src.key;

   dst.total = src.total;
   dst.wins = src.wins;
   dst.losses = src.losses;
   dst.flats = src.flats;

   dst.probe_total = src.probe_total;
   dst.probe_wins = src.probe_wins;
   dst.probe_losses = src.probe_losses;

   dst.live_total = src.live_total;
   dst.live_wins = src.live_wins;
   dst.live_losses = src.live_losses;

   dst.buy_total = src.buy_total;
   dst.buy_wins = src.buy_wins;
   dst.sell_total = src.sell_total;
   dst.sell_wins = src.sell_wins;

   dst.sum_r = src.sum_r;
   dst.sum_r2 = src.sum_r2;
   dst.min_r = src.min_r;
   dst.max_r = src.max_r;
   dst.sum_positive_r = src.sum_positive_r;
   dst.sum_negative_r = src.sum_negative_r;
   dst.sum_win_r = src.sum_win_r;
   dst.sum_loss_r = src.sum_loss_r;

   dst.sum_mfe_r = src.sum_mfe_r;
   dst.sum_mae_r = src.sum_mae_r;
   dst.max_mfe_r = src.max_mfe_r;
   dst.min_mae_r = src.min_mae_r;

   dst.sum_bars_to_exit = src.sum_bars_to_exit;
   dst.sum_seconds_to_exit = src.sum_seconds_to_exit;
   dst.min_bars_to_exit = src.min_bars_to_exit;
   dst.max_bars_to_exit = src.max_bars_to_exit;

   for(int h = 0; h < 24; h++)
   {
      dst.hour_total[h] = src.hour_total[h];
      dst.hour_wins[h] = src.hour_wins[h];
   }

   for(int b = 0; b < DAL_DE_R_BUCKETS; b++)
      dst.r_bucket_count[b] = src.r_bucket_count[b];

   dst.current_win_streak = src.current_win_streak;
   dst.current_loss_streak = src.current_loss_streak;
   dst.max_win_streak = src.max_win_streak;
   dst.max_loss_streak = src.max_loss_streak;

   for(int k = 0; k < DAL_DE_K_SIZE; k++)
   {
      dst.clusters_ge[k] = src.clusters_ge[k];
      dst.completed_win_runs_exact[k] = src.completed_win_runs_exact[k];
      dst.completed_loss_runs_exact[k] = src.completed_loss_runs_exact[k];
      dst.opp_after_atleast[k] = src.opp_after_atleast[k];
      dst.win_after_atleast[k] = src.win_after_atleast[k];
      dst.loss_after_atleast[k] = src.loss_after_atleast[k];
      dst.opp_after_exact[k] = src.opp_after_exact[k];
      dst.win_after_exact[k] = src.win_after_exact[k];
      dst.loss_after_exact[k] = src.loss_after_exact[k];
   }

   dst.first_entry_time = src.first_entry_time;
   dst.last_exit_time = src.last_exit_time;
}

void DAL_DEClusterStats_FinalizeOpenRuns(DAL_DEClusterStats &s)
{
   // Optional snapshot helper. It records the currently open run as completed.
   // Call only when producing a final offline report. Do not call before every add.
   if(s.current_win_streak > 0)
   {
      int idxw = DAL_DE_MinInt(s.current_win_streak, DAL_DE_MAX_K);
      s.completed_win_runs_exact[idxw]++;
   }
   if(s.current_loss_streak > 0)
   {
      int idxl = DAL_DE_MinInt(s.current_loss_streak, DAL_DE_MAX_K);
      s.completed_loss_runs_exact[idxl]++;
   }
}

// -----------------------------------------------------------------------------
// Derived metrics
// -----------------------------------------------------------------------------

int DAL_DEClusterStats_DecidedTotal(const DAL_DEClusterStats &s)
{
   return s.wins + s.losses;
}

double DAL_DEClusterStats_WinRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv((double)s.wins, (double)s.total, 0.0);
}

double DAL_DEClusterStats_DecidedWinRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv((double)s.wins, (double)DAL_DEClusterStats_DecidedTotal(s), 0.0);
}

double DAL_DEClusterStats_LossRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv((double)s.losses, (double)s.total, 0.0);
}

double DAL_DEClusterStats_MeanR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_r, (double)s.total, 0.0);
}

double DAL_DEClusterStats_VarianceR(const DAL_DEClusterStats &s)
{
   if(s.total <= 1)
      return 0.0;

   double mean = DAL_DEClusterStats_MeanR(s);
   double ex2  = DAL_DE_SafeDiv(s.sum_r2, (double)s.total, 0.0);
   double var  = ex2 - mean * mean;
   if(var < 0.0)
      var = 0.0;
   return var;
}

double DAL_DEClusterStats_StdR(const DAL_DEClusterStats &s)
{
   return MathSqrt(DAL_DEClusterStats_VarianceR(s));
}

double DAL_DEClusterStats_ProfitFactor(const DAL_DEClusterStats &s)
{
   if(MathAbs(s.sum_negative_r) <= 0.0)
   {
      if(s.sum_positive_r > 0.0)
         return DAL_DE_INF;
      return 0.0;
   }
   return s.sum_positive_r / MathAbs(s.sum_negative_r);
}

double DAL_DEClusterStats_AvgWinR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_win_r, (double)s.wins, 0.0);
}

double DAL_DEClusterStats_AvgLossR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_loss_r, (double)s.losses, 0.0);
}

double DAL_DEClusterStats_PayoffRatio(const DAL_DEClusterStats &s)
{
   double avg_loss_abs = MathAbs(DAL_DEClusterStats_AvgLossR(s));
   return DAL_DE_SafeDiv(DAL_DEClusterStats_AvgWinR(s), avg_loss_abs, 0.0);
}

double DAL_DEClusterStats_AvgMfeR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_mfe_r, (double)s.total, 0.0);
}

double DAL_DEClusterStats_AvgMaeR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_mae_r, (double)s.total, 0.0);
}

double DAL_DEClusterStats_AvgBarsToExit(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_bars_to_exit, (double)s.total, 0.0);
}

double DAL_DEClusterStats_AvgSecondsToExit(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeDiv(s.sum_seconds_to_exit, (double)s.total, 0.0);
}

double DAL_DEClusterStats_CondWinRateAfterAtLeast(const DAL_DEClusterStats &s, const int k)
{
   int kk = DAL_DE_MinInt(DAL_DE_MaxInt(k, 1), DAL_DE_MAX_K);
   return DAL_DE_SafeDiv((double)s.win_after_atleast[kk], (double)s.opp_after_atleast[kk], 0.0);
}

double DAL_DEClusterStats_CondWinRateAfterExact(const DAL_DEClusterStats &s, const int k)
{
   int kk = DAL_DE_MinInt(DAL_DE_MaxInt(k, 1), DAL_DE_MAX_K);
   return DAL_DE_SafeDiv((double)s.win_after_exact[kk], (double)s.opp_after_exact[kk], 0.0);
}

double DAL_DEClusterStats_LossHazardAfterAtLeast(const DAL_DEClusterStats &s, const int k)
{
   int kk = DAL_DE_MinInt(DAL_DE_MaxInt(k, 1), DAL_DE_MAX_K);
   return DAL_DE_SafeDiv((double)s.loss_after_atleast[kk], (double)s.opp_after_atleast[kk], 0.0);
}

double DAL_DEClusterStats_ClusterDensityGe(const DAL_DEClusterStats &s, const int k)
{
   int kk = DAL_DE_MinInt(DAL_DE_MaxInt(k, 1), DAL_DE_MAX_K);
   return DAL_DE_SafeDiv((double)s.clusters_ge[kk], (double)s.total, 0.0);
}

double DAL_DEClusterStats_LiftVsBase(const DAL_DEClusterStats &s, const DAL_DEClusterStats &base)
{
   double base_wr = DAL_DEClusterStats_DecidedWinRate(base);
   if(base_wr <= 0.0)
      return 0.0;
   return DAL_DEClusterStats_DecidedWinRate(s) / base_wr;
}

double DAL_DEClusterStats_SequenceLiftVsOwnWinRate(const DAL_DEClusterStats &s, const int k)
{
   double wr = DAL_DEClusterStats_DecidedWinRate(s);
   if(wr <= 0.0)
      return 0.0;
   return DAL_DEClusterStats_CondWinRateAfterAtLeast(s, k) / wr;
}

double DAL_DEClusterStats_Score(const DAL_DEClusterStats &s, const DAL_DEClusterStats &base)
{
   // A simple rank score for exploration, not a proof.
   // Rewards sample size, filtered win-rate lift, win-after-win, and 3+ clusters.
   double n_factor     = MathLog((double)s.total + 1.0);
   double lift         = DAL_DEClusterStats_LiftVsBase(s, base);
   double pww          = DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 1);
   double c3_density   = DAL_DEClusterStats_ClusterDensityGe(s, 3);
   double expectancy   = DAL_DEClusterStats_MeanR(s);
   return n_factor * (lift + pww + 2.0 * c3_density + MathMax(0.0, expectancy));
}

// -----------------------------------------------------------------------------
// Incremental update
// -----------------------------------------------------------------------------

void DAL_DEClusterStats_AddOutcome(DAL_DEClusterStats &s, const DAL_DETradeOutcome &o)
{
   bool is_win  = o.is_win;
   bool is_loss = o.is_loss;
   bool is_flat = o.is_flat;

   if(!is_win && !is_loss && !is_flat)
   {
      if(o.r_result > 0.0)
         is_win = true;
      else if(o.r_result < 0.0)
         is_loss = true;
      else
         is_flat = true;
   }

   int prev_win_streak  = s.current_win_streak;
   int prev_loss_streak = s.current_loss_streak;

   // Conditional opportunities: this trade occurred after an already-known run.
   for(int k = 1; k <= DAL_DE_MAX_K; k++)
   {
      if(prev_win_streak >= k)
      {
         s.opp_after_atleast[k]++;
         if(is_win)
            s.win_after_atleast[k]++;
         else if(is_loss)
            s.loss_after_atleast[k]++;
      }

      if(prev_win_streak == k)
      {
         s.opp_after_exact[k]++;
         if(is_win)
            s.win_after_exact[k]++;
         else if(is_loss)
            s.loss_after_exact[k]++;
      }
   }

   bool was_empty = (s.total == 0);

   s.total++;

   if(is_win)
      s.wins++;
   else if(is_loss)
      s.losses++;
   else
      s.flats++;

   if(o.is_probe || o.layer == DAL_DE_LAYER_PROBE)
   {
      s.probe_total++;
      if(is_win) s.probe_wins++;
      if(is_loss) s.probe_losses++;
   }

   if(o.is_live || o.layer == DAL_DE_LAYER_LIVE)
   {
      s.live_total++;
      if(is_win) s.live_wins++;
      if(is_loss) s.live_losses++;
   }

   if(o.direction > 0)
   {
      s.buy_total++;
      if(is_win) s.buy_wins++;
   }
   else if(o.direction < 0)
   {
      s.sell_total++;
      if(is_win) s.sell_wins++;
   }

   s.sum_r  += o.r_result;
   s.sum_r2 += o.r_result * o.r_result;

   if(was_empty)
   {
      s.min_r = o.r_result;
      s.max_r = o.r_result;
      s.max_mfe_r = o.mfe_r;
      s.min_mae_r = o.mae_r;
      s.min_bars_to_exit = o.bars_to_exit;
      s.max_bars_to_exit = o.bars_to_exit;
      s.first_entry_time = o.entry_time;
   }
   else
   {
      if(o.r_result < s.min_r) s.min_r = o.r_result;
      if(o.r_result > s.max_r) s.max_r = o.r_result;
      if(o.mfe_r > s.max_mfe_r) s.max_mfe_r = o.mfe_r;
      if(o.mae_r < s.min_mae_r) s.min_mae_r = o.mae_r;
      if(o.bars_to_exit < s.min_bars_to_exit) s.min_bars_to_exit = o.bars_to_exit;
      if(o.bars_to_exit > s.max_bars_to_exit) s.max_bars_to_exit = o.bars_to_exit;
   }

   if(o.exit_time > 0)
      s.last_exit_time = o.exit_time;

   if(o.r_result > 0.0)
      s.sum_positive_r += o.r_result;
   if(o.r_result < 0.0)
      s.sum_negative_r += o.r_result;

   if(is_win)
      s.sum_win_r += o.r_result;
   if(is_loss)
      s.sum_loss_r += o.r_result;

   s.sum_mfe_r += o.mfe_r;
   s.sum_mae_r += o.mae_r;

   s.sum_bars_to_exit    += (double)o.bars_to_exit;
   s.sum_seconds_to_exit += (double)o.seconds_to_exit;

   int h = DAL_DE_HourOf(o.entry_time);
   if(h >= 0 && h < 24)
   {
      s.hour_total[h]++;
      if(is_win)
         s.hour_wins[h]++;
   }

   int rb = DAL_DE_RBucketIndex(o.r_result);
   if(rb >= 0 && rb < DAL_DE_R_BUCKETS)
      s.r_bucket_count[rb]++;

   if(is_win)
   {
      if(prev_loss_streak > 0)
      {
         int idxl = DAL_DE_MinInt(prev_loss_streak, DAL_DE_MAX_K);
         s.completed_loss_runs_exact[idxl]++;
      }

      s.current_loss_streak = 0;
      s.current_win_streak  = prev_win_streak + 1;
      if(s.current_win_streak > s.max_win_streak)
         s.max_win_streak = s.current_win_streak;

      for(int k2 = 1; k2 <= DAL_DE_MAX_K; k2++)
      {
         if(s.current_win_streak == k2)
            s.clusters_ge[k2]++;
      }
   }
   else if(is_loss)
   {
      if(prev_win_streak > 0)
      {
         int idxw = DAL_DE_MinInt(prev_win_streak, DAL_DE_MAX_K);
         s.completed_win_runs_exact[idxw]++;
      }

      s.current_win_streak  = 0;
      s.current_loss_streak = prev_loss_streak + 1;
      if(s.current_loss_streak > s.max_loss_streak)
         s.max_loss_streak = s.current_loss_streak;
   }
   else
   {
      if(prev_win_streak > 0)
      {
         int idxwf = DAL_DE_MinInt(prev_win_streak, DAL_DE_MAX_K);
         s.completed_win_runs_exact[idxwf]++;
      }
      if(prev_loss_streak > 0)
      {
         int idxlf = DAL_DE_MinInt(prev_loss_streak, DAL_DE_MAX_K);
         s.completed_loss_runs_exact[idxlf]++;
      }

      s.current_win_streak  = 0;
      s.current_loss_streak = 0;
   }
}

// -----------------------------------------------------------------------------
// Miner lifecycle and group operations
// -----------------------------------------------------------------------------

void DAL_DEClusterMiner_Reset(DAL_DEClusterMiner &m, const string miner_id = "EXP0012", const string strategy_id = "")
{
   m.miner_id    = miner_id;
   m.strategy_id = strategy_id;
   m.group_count = 0;
   m.max_groups  = DAL_DE_MAX_GROUPS;
   m.initialized = true;

   DAL_DEClusterStats_Reset(m.all, "ALL");

   for(int i = 0; i < DAL_DE_MAX_GROUPS; i++)
   {
      m.groups[i].key = "";
      DAL_DEClusterStats_Reset(m.groups[i].stats, "");
   }
}

int DAL_DEClusterMiner_FindGroup(const DAL_DEClusterMiner &m, const string key)
{
   for(int i = 0; i < m.group_count; i++)
   {
      if(m.groups[i].key == key)
         return i;
   }
   return -1;
}

int DAL_DEClusterMiner_EnsureGroup(DAL_DEClusterMiner &m, const string raw_key)
{
   string key = raw_key;
   if(key == "" || key == "UNSPECIFIED")
      key = "UNSPECIFIED";

   int existing = DAL_DEClusterMiner_FindGroup(m, key);
   if(existing >= 0)
      return existing;

   if(m.group_count >= DAL_DE_MAX_GROUPS)
      return -1;

   int idx = m.group_count;
   m.group_count++;

   m.groups[idx].key = key;
   DAL_DEClusterStats_Reset(m.groups[idx].stats, key);
   return idx;
}

bool DAL_DEClusterMiner_AddOutcome(DAL_DEClusterMiner &m, const DAL_DETradeOutcome &o)
{
   if(!m.initialized)
      DAL_DEClusterMiner_Reset(m, "EXP0012", o.strategy_id);

   DAL_DEClusterStats_AddOutcome(m.all, o);

   string key = o.feature_key;
   if(key == "")
      key = "UNSPECIFIED";

   int idx = DAL_DEClusterMiner_EnsureGroup(m, key);
   if(idx < 0)
      return false;

   DAL_DEClusterStats_AddOutcome(m.groups[idx].stats, o);
   return true;
}

bool DAL_DEClusterMiner_GetGroupStats(const DAL_DEClusterMiner &m, const string key, DAL_DEClusterStats &out_stats)
{
   int idx = DAL_DEClusterMiner_FindGroup(m, key);
   if(idx < 0)
      return false;
   DAL_DEClusterStats_Copy(m.groups[idx].stats, out_stats);
   return true;
}

// -----------------------------------------------------------------------------
// Text report and CSV export
// -----------------------------------------------------------------------------

string DAL_DEClusterStats_OneLine(const DAL_DEClusterStats &s, const DAL_DEClusterStats &base)
{
   return StringFormat(
      "%s | n=%d decided=%d winRate=%.4f decidedWR=%.4f lift=%.3f meanR=%.4f pf=%.3f maxW=%d P(W|W)=%.4f P(W|WW)=%.4f P(W|WWW)=%.4f c3=%d c5=%d c7=%d c10=%d score=%.4f",
      s.key,
      s.total,
      DAL_DEClusterStats_DecidedTotal(s),
      DAL_DEClusterStats_WinRate(s),
      DAL_DEClusterStats_DecidedWinRate(s),
      DAL_DEClusterStats_LiftVsBase(s, base),
      DAL_DEClusterStats_MeanR(s),
      DAL_DEClusterStats_ProfitFactor(s),
      s.max_win_streak,
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 1),
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 2),
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 3),
      s.clusters_ge[3],
      s.clusters_ge[5],
      s.clusters_ge[7],
      s.clusters_ge[10],
      DAL_DEClusterStats_Score(s, base)
   );
}

string DAL_DEClusterMiner_Report(const DAL_DEClusterMiner &m, const int max_groups_to_print = 50)
{
   string out = "";
   out += "DAL Distribution Engineering Cluster Miner\n";
   out += "miner_id=" + m.miner_id + " strategy_id=" + m.strategy_id + "\n";
   out += "RAW: " + DAL_DEClusterStats_OneLine(m.all, m.all) + "\n";
   out += "groups=" + IntegerToString(m.group_count) + "\n";

   int limit = max_groups_to_print;
   if(limit > m.group_count)
      limit = m.group_count;

   for(int i = 0; i < limit; i++)
      out += "G" + IntegerToString(i) + ": " + DAL_DEClusterStats_OneLine(m.groups[i].stats, m.all) + "\n";

   return out;
}


void DAL_DEClusterMiner_WriteCsvRow(const int handle, const DAL_DEClusterStats &s, const DAL_DEClusterStats &base)
{
   FileWrite(handle,
      s.key,
      s.total,
      s.wins,
      s.losses,
      s.flats,
      DAL_DEClusterStats_DecidedTotal(s),
      DAL_DEClusterStats_WinRate(s),
      DAL_DEClusterStats_DecidedWinRate(s),
      DAL_DEClusterStats_LiftVsBase(s, base),
      DAL_DEClusterStats_MeanR(s),
      DAL_DEClusterStats_StdR(s),
      s.min_r,
      s.max_r,
      DAL_DEClusterStats_ProfitFactor(s),
      DAL_DEClusterStats_AvgWinR(s),
      DAL_DEClusterStats_AvgLossR(s),
      DAL_DEClusterStats_PayoffRatio(s),
      DAL_DEClusterStats_AvgMfeR(s),
      DAL_DEClusterStats_AvgMaeR(s),
      s.max_mfe_r,
      s.min_mae_r,
      DAL_DEClusterStats_AvgBarsToExit(s),
      s.min_bars_to_exit,
      s.max_bars_to_exit,
      s.probe_total,
      DAL_DE_SafeDiv((double)s.probe_wins, (double)s.probe_total, 0.0),
      s.live_total,
      DAL_DE_SafeDiv((double)s.live_wins, (double)s.live_total, 0.0),
      s.buy_total,
      DAL_DE_SafeDiv((double)s.buy_wins, (double)s.buy_total, 0.0),
      s.sell_total,
      DAL_DE_SafeDiv((double)s.sell_wins, (double)s.sell_total, 0.0),
      s.max_win_streak,
      s.max_loss_streak,
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 1),
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 2),
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 3),
      DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 5),
      DAL_DEClusterStats_LossHazardAfterAtLeast(s, 1),
      DAL_DEClusterStats_LossHazardAfterAtLeast(s, 2),
      DAL_DEClusterStats_LossHazardAfterAtLeast(s, 3),
      s.clusters_ge[3],
      s.clusters_ge[5],
      s.clusters_ge[7],
      s.clusters_ge[10],
      DAL_DEClusterStats_ClusterDensityGe(s, 3),
      DAL_DEClusterStats_Score(s, base)
   );
}

bool DAL_DEClusterMiner_ExportCsv(const DAL_DEClusterMiner &m, const string file_name)
{
   int handle = FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(handle == INVALID_HANDLE)
      return false;

   FileWrite(handle,
      "key",
      "total",
      "wins",
      "losses",
      "flats",
      "decided_total",
      "win_rate_total",
      "win_rate_decided",
      "lift_vs_raw",
      "mean_r",
      "std_r",
      "min_r",
      "max_r",
      "profit_factor",
      "avg_win_r",
      "avg_loss_r",
      "payoff_ratio",
      "avg_mfe_r",
      "avg_mae_r",
      "max_mfe_r",
      "min_mae_r",
      "avg_bars_to_exit",
      "min_bars_to_exit",
      "max_bars_to_exit",
      "probe_total",
      "probe_win_rate",
      "live_total",
      "live_win_rate",
      "buy_total",
      "buy_win_rate",
      "sell_total",
      "sell_win_rate",
      "max_win_streak",
      "max_loss_streak",
      "p_win_after_1w",
      "p_win_after_2w",
      "p_win_after_3w",
      "p_win_after_5w",
      "loss_hazard_after_1w",
      "loss_hazard_after_2w",
      "loss_hazard_after_3w",
      "clusters_ge_3",
      "clusters_ge_5",
      "clusters_ge_7",
      "clusters_ge_10",
      "cluster_density_ge_3",
      "score"
   );

   DAL_DEClusterMiner_WriteCsvRow(handle, m.all, m.all);

   for(int row = 0; row < m.group_count; row++)
      DAL_DEClusterMiner_WriteCsvRow(handle, m.groups[row].stats, m.all);

   FileClose(handle);
   return true;
}

#endif // __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__
