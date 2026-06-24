#ifndef __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__
#define __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__

#include <Research/DAL_DistributionClusterMiner.mqh>

// Decision Alpha Lab
// Distribution Cluster Filter
// Converts mined distribution stats into an execution permission decision.
// Research-only: it does not send orders.

struct DAL_DEClusterFilterConfig
{
   int    min_total;
   int    min_decided_total;
   int    min_clusters_ge_3;
   int    min_clusters_ge_5;
   int    min_max_win_streak;

   double min_win_rate_decided;
   double min_mean_r;
   double min_profit_factor;
   double min_lift_vs_raw;
   double min_p_win_after_1w;
   double min_p_win_after_2w;
   double min_p_win_after_3w;
   double max_loss_hazard_after_1w;

   bool   require_positive_expectancy;
   bool   require_sequence_lift;
};

struct DAL_DEClusterFilterDecision
{
   bool   allowed;
   string key;
   string reason;

   int    total;
   int    decided_total;
   int    max_win_streak;
   int    clusters_ge_3;
   int    clusters_ge_5;
   int    clusters_ge_7;
   int    clusters_ge_10;

   double raw_win_rate;
   double filtered_win_rate;
   double lift_vs_raw;
   double mean_r;
   double profit_factor;
   double p_win_after_1w;
   double p_win_after_2w;
   double p_win_after_3w;
   double loss_hazard_after_1w;
   double sequence_lift_after_1w;
   double score;
};

void DAL_DEClusterFilterConfig_Default(DAL_DEClusterFilterConfig &cfg)
{
   cfg.min_total              = 200;
   cfg.min_decided_total      = 150;
   cfg.min_clusters_ge_3      = 3;
   cfg.min_clusters_ge_5      = 0;
   cfg.min_max_win_streak     = 3;

   cfg.min_win_rate_decided   = 0.50;
   cfg.min_mean_r             = 0.0;
   cfg.min_profit_factor      = 1.00;
   cfg.min_lift_vs_raw        = 1.10;
   cfg.min_p_win_after_1w     = 0.55;
   cfg.min_p_win_after_2w     = 0.00;
   cfg.min_p_win_after_3w     = 0.00;
   cfg.max_loss_hazard_after_1w = 1.00;

   cfg.require_positive_expectancy = true;
   cfg.require_sequence_lift       = true;
}

void DAL_DEClusterFilterDecision_Reset(DAL_DEClusterFilterDecision &d)
{
   d.allowed = false;
   d.key = "";
   d.reason = "";

   d.total = 0;
   d.decided_total = 0;
   d.max_win_streak = 0;
   d.clusters_ge_3 = 0;
   d.clusters_ge_5 = 0;
   d.clusters_ge_7 = 0;
   d.clusters_ge_10 = 0;

   d.raw_win_rate = 0.0;
   d.filtered_win_rate = 0.0;
   d.lift_vs_raw = 0.0;
   d.mean_r = 0.0;
   d.profit_factor = 0.0;
   d.p_win_after_1w = 0.0;
   d.p_win_after_2w = 0.0;
   d.p_win_after_3w = 0.0;
   d.loss_hazard_after_1w = 0.0;
   d.sequence_lift_after_1w = 0.0;
   d.score = 0.0;
}

void DAL_DEClusterFilterDecision_FillMetrics(
   DAL_DEClusterFilterDecision &d,
   const DAL_DEClusterStats &s,
   const DAL_DEClusterStats &base
)
{
   d.key             = s.key;
   d.total           = s.total;
   d.decided_total   = DAL_DEClusterStats_DecidedTotal(s);
   d.max_win_streak  = s.max_win_streak;
   d.clusters_ge_3   = s.clusters_ge[3];
   d.clusters_ge_5   = s.clusters_ge[5];
   d.clusters_ge_7   = s.clusters_ge[7];
   d.clusters_ge_10  = s.clusters_ge[10];

   d.raw_win_rate          = DAL_DEClusterStats_DecidedWinRate(base);
   d.filtered_win_rate     = DAL_DEClusterStats_DecidedWinRate(s);
   d.lift_vs_raw           = DAL_DEClusterStats_LiftVsBase(s, base);
   d.mean_r                = DAL_DEClusterStats_MeanR(s);
   d.profit_factor         = DAL_DEClusterStats_ProfitFactor(s);
   d.p_win_after_1w        = DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 1);
   d.p_win_after_2w        = DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 2);
   d.p_win_after_3w        = DAL_DEClusterStats_CondWinRateAfterAtLeast(s, 3);
   d.loss_hazard_after_1w  = DAL_DEClusterStats_LossHazardAfterAtLeast(s, 1);
   d.sequence_lift_after_1w= DAL_DEClusterStats_SequenceLiftVsOwnWinRate(s, 1);
   d.score                 = DAL_DEClusterStats_Score(s, base);
}

bool DAL_DEClusterFilter_EvaluateStats(
   const DAL_DEClusterStats &s,
   const DAL_DEClusterStats &base,
   const DAL_DEClusterFilterConfig &cfg,
   DAL_DEClusterFilterDecision &d
)
{
   DAL_DEClusterFilterDecision_Reset(d);
   DAL_DEClusterFilterDecision_FillMetrics(d, s, base);

   if(d.total < cfg.min_total)
   {
      d.reason = "reject:min_total";
      return false;
   }

   if(d.decided_total < cfg.min_decided_total)
   {
      d.reason = "reject:min_decided_total";
      return false;
   }

   if(d.filtered_win_rate < cfg.min_win_rate_decided)
   {
      d.reason = "reject:min_win_rate_decided";
      return false;
   }

   if(cfg.require_positive_expectancy && d.mean_r < cfg.min_mean_r)
   {
      d.reason = "reject:min_mean_r";
      return false;
   }

   if(d.profit_factor < cfg.min_profit_factor)
   {
      d.reason = "reject:min_profit_factor";
      return false;
   }

   if(d.lift_vs_raw < cfg.min_lift_vs_raw)
   {
      d.reason = "reject:min_lift_vs_raw";
      return false;
   }

   if(d.max_win_streak < cfg.min_max_win_streak)
   {
      d.reason = "reject:min_max_win_streak";
      return false;
   }

   if(d.clusters_ge_3 < cfg.min_clusters_ge_3)
   {
      d.reason = "reject:min_clusters_ge_3";
      return false;
   }

   if(d.clusters_ge_5 < cfg.min_clusters_ge_5)
   {
      d.reason = "reject:min_clusters_ge_5";
      return false;
   }

   if(cfg.require_sequence_lift)
   {
      if(d.p_win_after_1w < cfg.min_p_win_after_1w)
      {
         d.reason = "reject:min_p_win_after_1w";
         return false;
      }

      if(cfg.min_p_win_after_2w > 0.0 && d.p_win_after_2w < cfg.min_p_win_after_2w)
      {
         d.reason = "reject:min_p_win_after_2w";
         return false;
      }

      if(cfg.min_p_win_after_3w > 0.0 && d.p_win_after_3w < cfg.min_p_win_after_3w)
      {
         d.reason = "reject:min_p_win_after_3w";
         return false;
      }
   }

   if(d.loss_hazard_after_1w > cfg.max_loss_hazard_after_1w)
   {
      d.reason = "reject:max_loss_hazard_after_1w";
      return false;
   }

   d.allowed = true;
   d.reason  = "allow:distribution_cluster_eligible";
   return true;
}

bool DAL_DEClusterFilter_EvaluateKey(
   const DAL_DEClusterMiner &m,
   const string key,
   const DAL_DEClusterFilterConfig &cfg,
   DAL_DEClusterFilterDecision &d
)
{
   DAL_DEClusterStats s;
   if(!DAL_DEClusterMiner_GetGroupStats(m, key, s))
   {
      DAL_DEClusterFilterDecision_Reset(d);
      d.key = key;
      d.reason = "reject:key_not_found";
      return false;
   }

   return DAL_DEClusterFilter_EvaluateStats(s, m.all, cfg, d);
}

int DAL_DEClusterFilter_CollectEligibleKeys(
   const DAL_DEClusterMiner &m,
   const DAL_DEClusterFilterConfig &cfg,
   string &keys[],
   DAL_DEClusterFilterDecision &decisions[]
)
{
   ArrayResize(keys, 0);
   ArrayResize(decisions, 0);

   int count = 0;
   for(int i = 0; i < m.group_count; i++)
   {
      DAL_DEClusterFilterDecision d;
      if(DAL_DEClusterFilter_EvaluateStats(m.groups[i].stats, m.all, cfg, d))
      {
         ArrayResize(keys, count + 1);
         ArrayResize(decisions, count + 1);
         keys[count] = m.groups[i].key;
         decisions[count] = d;
         count++;
      }
   }

   return count;
}

string DAL_DEClusterFilterDecision_ToLine(const DAL_DEClusterFilterDecision &d)
{
   return StringFormat(
      "%s | allowed=%s reason=%s n=%d decided=%d wr=%.4f raw=%.4f lift=%.3f meanR=%.4f pf=%.3f P(W|W)=%.4f P(W|WW)=%.4f maxW=%d c3=%d c5=%d score=%.4f",
      d.key,
      DAL_DE_BoolText(d.allowed),
      d.reason,
      d.total,
      d.decided_total,
      d.filtered_win_rate,
      d.raw_win_rate,
      d.lift_vs_raw,
      d.mean_r,
      d.profit_factor,
      d.p_win_after_1w,
      d.p_win_after_2w,
      d.max_win_streak,
      d.clusters_ge_3,
      d.clusters_ge_5,
      d.score
   );
}

#endif // __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__
