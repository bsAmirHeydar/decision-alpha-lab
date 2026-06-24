#ifndef __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__
#define __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__

#include <Research/DAL_DistributionClusterMiner.mqh>

// Lightweight runtime filter configuration for any execution module.
// The execution builds a causal feature key before entry. This adapter decides
// whether that key is statistically eligible for Roulette / Jackpot mode.

struct DAL_DEClusterFilterConfig
{
   bool   enabled;
   int    min_trades;
   double min_win_rate;
   double min_after_one_win_rate;
   double min_lift;
   int    min_clusters_ge_3;
};

void DAL_DEClusterFilterConfig_Default(DAL_DEClusterFilterConfig &cfg)
{
   cfg.enabled                = true;
   cfg.min_trades             = 200;
   cfg.min_win_rate           = 0.50;
   cfg.min_after_one_win_rate = 0.60;
   cfg.min_lift               = 1.10;
   cfg.min_clusters_ge_3      = 5;
}

bool DAL_DEClusterFilter_Allow(
   DAL_DEClusterMiner &miner,
   const DAL_DEClusterFilterConfig &cfg,
   const string feature_key
)
{
   if(!cfg.enabled)
      return true;

   return DAL_DEClusterMiner_IsEligible(
      miner,
      feature_key,
      cfg.min_trades,
      cfg.min_win_rate,
      cfg.min_after_one_win_rate,
      cfg.min_lift,
      cfg.min_clusters_ge_3
   );
}

string DAL_DEClusterFilter_Reason(
   DAL_DEClusterMiner &miner,
   const DAL_DEClusterFilterConfig &cfg,
   const string feature_key
)
{
   if(!cfg.enabled)
      return "distribution_filter=disabled";

   const int idx = DAL_DEClusterMiner_FindKeyIndex(miner, feature_key);
   if(idx < 0)
      return "distribution_filter=rejected reason=unknown_feature_key key=" + feature_key;

   DAL_DEClusterStats s = miner.by_key[idx];
   const double raw_wr = DAL_DE_WinRate(miner.overall);
   const double wr = DAL_DE_WinRate(s);
   const double after_1 = DAL_DE_AfterOneWinRate(s);
   const double lift = (raw_wr > 0.0 ? wr / raw_wr : 0.0);

   if(s.total < cfg.min_trades)
      return StringFormat("distribution_filter=rejected reason=min_trades key=%s total=%d required=%d", feature_key, s.total, cfg.min_trades);

   if(wr < cfg.min_win_rate)
      return StringFormat("distribution_filter=rejected reason=win_rate key=%s winRate=%.4f required=%.4f", feature_key, wr, cfg.min_win_rate);

   if(after_1 < cfg.min_after_one_win_rate)
      return StringFormat("distribution_filter=rejected reason=after_one_win key=%s afterW=%.4f required=%.4f", feature_key, after_1, cfg.min_after_one_win_rate);

   if(lift < cfg.min_lift)
      return StringFormat("distribution_filter=rejected reason=lift key=%s lift=%.4f required=%.4f", feature_key, lift, cfg.min_lift);

   if(s.clusters_ge_3 < cfg.min_clusters_ge_3)
      return StringFormat("distribution_filter=rejected reason=clusters_ge_3 key=%s c3=%d required=%d", feature_key, s.clusters_ge_3, cfg.min_clusters_ge_3);

   return StringFormat("distribution_filter=allowed key=%s total=%d winRate=%.4f afterW=%.4f lift=%.4f c3=%d", feature_key, s.total, wr, after_1, lift, s.clusters_ge_3);
}

#endif // __DAL_DISTRIBUTION_CLUSTER_FILTER_MQH__
