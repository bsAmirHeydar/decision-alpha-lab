#ifndef __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__
#define __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__

#include <Research/DAL_DistributionEngineeringTypes.mqh>

// Decision Alpha Lab
// EXP0012 Distributional Cluster Miner
// This module does not send orders. It only records trade outcomes and computes
// conditional sequence statistics that can be used by execution modules.

struct DAL_DEClusterMiner
{
   string strategy_id;

   int    threshold_3;
   int    threshold_5;
   int    threshold_7;
   int    threshold_10;

   DAL_DEClusterStats overall;
   DAL_DEClusterStats by_key[];

   int    outcomes_recorded;
};

void DAL_DEClusterMiner_Init(
   DAL_DEClusterMiner &m,
   const string strategy_id,
   const int threshold_3 = 3,
   const int threshold_5 = 5,
   const int threshold_7 = 7,
   const int threshold_10 = 10
)
{
   m.strategy_id  = strategy_id;
   m.threshold_3  = threshold_3;
   m.threshold_5  = threshold_5;
   m.threshold_7  = threshold_7;
   m.threshold_10 = threshold_10;

   DAL_DEClusterStats_Reset(m.overall, "ALL");
   ArrayResize(m.by_key, 0);
   m.outcomes_recorded = 0;
}

string DAL_DE_NormalizeKey(const string feature_key)
{
   string k = feature_key;
   StringTrimLeft(k);
   StringTrimRight(k);
   if(k == "")
      return "UNSPECIFIED";
   return k;
}

int DAL_DEClusterMiner_FindKeyIndex(DAL_DEClusterMiner &m, const string feature_key)
{
   const string k = DAL_DE_NormalizeKey(feature_key);
   const int n = ArraySize(m.by_key);
   for(int i = 0; i < n; i++)
   {
      if(m.by_key[i].key == k)
         return i;
   }
   return -1;
}

int DAL_DEClusterMiner_EnsureKey(DAL_DEClusterMiner &m, const string feature_key)
{
   int idx = DAL_DEClusterMiner_FindKeyIndex(m, feature_key);
   if(idx >= 0)
      return idx;

   const int old_n = ArraySize(m.by_key);
   ArrayResize(m.by_key, old_n + 1);
   DAL_DEClusterStats_Reset(m.by_key[old_n], DAL_DE_NormalizeKey(feature_key));
   return old_n;
}

double DAL_DE_SafeRatio(const double numerator, const double denominator)
{
   if(denominator <= 0.0)
      return 0.0;
   return numerator / denominator;
}

double DAL_DE_WinRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeRatio((double)s.wins, (double)s.total);
}

double DAL_DE_AvgR(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeRatio(s.sum_r, (double)s.total);
}

double DAL_DE_AfterOneWinRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeRatio((double)s.win_after_1_win, (double)s.opp_after_1_win);
}

double DAL_DE_AfterTwoWinsRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeRatio((double)s.win_after_2_wins, (double)s.opp_after_2_wins);
}

double DAL_DE_AfterThreeWinsRate(const DAL_DEClusterStats &s)
{
   return DAL_DE_SafeRatio((double)s.win_after_3_wins, (double)s.opp_after_3_wins);
}

void DAL_DEClusterStats_AddOutcome(DAL_DEClusterStats &s, const DAL_DETradeOutcome &o)
{
   const int prior_streak = s.current_win_streak;

   if(prior_streak >= 1)
   {
      s.opp_after_1_win++;
      if(o.is_win)
         s.win_after_1_win++;
   }

   if(prior_streak >= 2)
   {
      s.opp_after_2_wins++;
      if(o.is_win)
         s.win_after_2_wins++;
   }

   if(prior_streak >= 3)
   {
      s.opp_after_3_wins++;
      if(o.is_win)
         s.win_after_3_wins++;
   }

   s.total++;
   s.sum_r     += o.r_result;
   s.sum_mfe_r += o.mfe_r;
   s.sum_mae_r += o.mae_r;

   if(s.min_bars_to_exit == 0 || o.bars_to_exit < s.min_bars_to_exit)
      s.min_bars_to_exit = o.bars_to_exit;
   if(o.bars_to_exit > s.max_bars_to_exit)
      s.max_bars_to_exit = o.bars_to_exit;

   if(o.is_win)
   {
      s.wins++;
      s.current_win_streak++;

      if(s.current_win_streak > s.max_win_streak)
         s.max_win_streak = s.current_win_streak;

      if(s.current_win_streak == 3)
         s.clusters_ge_3++;
      if(s.current_win_streak == 5)
         s.clusters_ge_5++;
      if(s.current_win_streak == 7)
         s.clusters_ge_7++;
      if(s.current_win_streak == 10)
         s.clusters_ge_10++;
   }
   else
   {
      s.losses++;
      s.current_win_streak = 0;
   }
}

void DAL_DEClusterMiner_AddOutcome(DAL_DEClusterMiner &m, const DAL_DETradeOutcome &outcome)
{
   DAL_DETradeOutcome o = outcome;
   o.feature_key = DAL_DE_NormalizeKey(o.feature_key);

   DAL_DEClusterStats_AddOutcome(m.overall, o);

   const int idx = DAL_DEClusterMiner_EnsureKey(m, o.feature_key);
   if(idx >= 0)
      DAL_DEClusterStats_AddOutcome(m.by_key[idx], o);

   m.outcomes_recorded++;
}

double DAL_DEClusterMiner_KeyLift(DAL_DEClusterMiner &m, const string feature_key)
{
   const double raw_wr = DAL_DE_WinRate(m.overall);
   if(raw_wr <= 0.0)
      return 0.0;

   const int idx = DAL_DEClusterMiner_FindKeyIndex(m, feature_key);
   if(idx < 0)
      return 0.0;

   return DAL_DE_WinRate(m.by_key[idx]) / raw_wr;
}

bool DAL_DEClusterMiner_IsEligible(
   DAL_DEClusterMiner &m,
   const string feature_key,
   const int min_trades,
   const double min_win_rate,
   const double min_after_one_win_rate,
   const double min_lift,
   const int min_clusters_ge_3
)
{
   const int idx = DAL_DEClusterMiner_FindKeyIndex(m, feature_key);
   if(idx < 0)
      return false;

   DAL_DEClusterStats s = m.by_key[idx];

   if(s.total < min_trades)
      return false;

   const double wr = DAL_DE_WinRate(s);
   if(wr < min_win_rate)
      return false;

   const double after_1 = DAL_DE_AfterOneWinRate(s);
   if(after_1 < min_after_one_win_rate)
      return false;

   const double lift = DAL_DEClusterMiner_KeyLift(m, feature_key);
   if(lift < min_lift)
      return false;

   if(s.clusters_ge_3 < min_clusters_ge_3)
      return false;

   return true;
}

string DAL_DEClusterStats_Line(DAL_DEClusterStats &s, const double raw_win_rate)
{
   const double wr      = DAL_DE_WinRate(s);
   const double avg_r   = DAL_DE_AvgR(s);
   const double after_1 = DAL_DE_AfterOneWinRate(s);
   const double after_2 = DAL_DE_AfterTwoWinsRate(s);
   const double after_3 = DAL_DE_AfterThreeWinsRate(s);
   const double lift    = (raw_win_rate > 0.0 ? wr / raw_win_rate : 0.0);

   return StringFormat(
      "DE_CLUSTER key=%s total=%d wins=%d losses=%d winRate=%.4f avgR=%.4f lift=%.4f afterW=%.4f afterWW=%.4f afterWWW=%.4f maxStreak=%d c3=%d c5=%d c7=%d c10=%d barsMin=%d barsMax=%d",
      s.key,
      s.total,
      s.wins,
      s.losses,
      wr,
      avg_r,
      lift,
      after_1,
      after_2,
      after_3,
      s.max_win_streak,
      s.clusters_ge_3,
      s.clusters_ge_5,
      s.clusters_ge_7,
      s.clusters_ge_10,
      s.min_bars_to_exit,
      s.max_bars_to_exit
   );
}

void DAL_DEClusterMiner_PrintReport(DAL_DEClusterMiner &m, const int max_keys_to_print = 50)
{
   const double raw_wr = DAL_DE_WinRate(m.overall);

   Print("=== DAL DISTRIBUTION ENGINEERING REPORT ===");
   Print("strategy_id=", m.strategy_id, " outcomes=", m.outcomes_recorded);
   Print(DAL_DEClusterStats_Line(m.overall, raw_wr));

   const int n = ArraySize(m.by_key);
   const int limit = MathMin(n, max_keys_to_print);

   for(int i = 0; i < limit; i++)
      Print(DAL_DEClusterStats_Line(m.by_key[i], raw_wr));

   if(n > limit)
      Print("DE_CLUSTER report truncated keys=", n, " printed=", limit);
}

string DAL_DEFeatureKey_Add(const string base_key, const string name, const string value)
{
   string k = base_key;
   StringTrimLeft(k);
   StringTrimRight(k);

   string part = name + "=" + value;
   if(k == "")
      return part;
   return k + "|" + part;
}

string DAL_DEBucket_Double(
   const double x,
   const double low_thr,
   const double high_thr,
   const string low_name = "low",
   const string mid_name = "mid",
   const string high_name = "high"
)
{
   if(x <= low_thr)
      return low_name;
   if(x >= high_thr)
      return high_name;
   return mid_name;
}

#endif // __DAL_DISTRIBUTION_CLUSTER_MINER_MQH__
