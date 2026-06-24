#property strict
#property version   "1.00"
#property description "Decision Alpha Lab EXP0012 - Distribution Engineering Cluster Miner demo"
#property description "Research-only. Does not send orders."

#include <Research/DAL_DistributionExecutionAdapter.mqh>

input bool   InpExportCsv       = true;
input string InpExportCsvName   = "EXP0012_distribution_cluster_miner_demo.csv";
input int    InpSyntheticTrades = 350;
input double InpWinThresholdR   = 3.0;

DAL_DEClusterMiner g_miner;

string BuildSyntheticFeatureKey(const int i)
{
   string key = DAL_DEAdapter_BaseFeatureKey("DEMO_DONCHIAN_ATR", _Symbol, PERIOD_M1);

   // Two engineered regimes: one noisy, one cluster-friendly.
   if((i % 11) <= 5)
   {
      key = DAL_DE_KeyAppend(key, "atr", "high");
      key = DAL_DE_KeyAppend(key, "donchian_width", "high");
      key = DAL_DE_KeyAppend(key, "htf_aligned", "true");
      key = DAL_DE_KeyAppend(key, "path_clean", "true");
   }
   else
   {
      key = DAL_DE_KeyAppend(key, "atr", "low");
      key = DAL_DE_KeyAppend(key, "donchian_width", "mid");
      key = DAL_DE_KeyAppend(key, "htf_aligned", "false");
      key = DAL_DE_KeyAppend(key, "path_clean", "false");
   }

   key = DAL_DEAdapter_AddDirectionFeature(key, (i % 2 == 0 ? 1 : -1));
   return key;
}

double SyntheticR(const int i)
{
   // This is only a deterministic demo, not a market model.
   // Creates visible clusters in the high/high/aligned/clean feature group.
   bool cluster_regime = ((i % 11) <= 5);
   if(cluster_regime)
   {
      int j = i % 7;
      if(j == 0 || j == 1 || j == 2 || j == 3)
         return 3.0;
      if(j == 4)
         return -1.0;
      return 3.0;
   }

   int k = i % 6;
   if(k == 0 || k == 4)
      return 3.0;
   if(k == 1 || k == 2 || k == 3)
      return -1.0;
   return 0.0;
}

int OnInit()
{
   DAL_DEClusterMiner_Reset(g_miner, "EXP0012_DEMO", "DEMO_DONCHIAN_ATR");

   DAL_DEExecutionAdapterConfig cfg;
   DAL_DEExecutionAdapterConfig_Default(cfg, "DEMO_DONCHIAN_ATR", "EXP0012_Demo");
   cfg.symbol = _Symbol;
   cfg.timeframe = PERIOD_M1;
   cfg.magic = 12012;
   cfg.win_threshold_r = InpWinThresholdR;
   cfg.loss_threshold_r = -1.0;
   cfg.use_decided_thresholds = true;

   datetime t0 = TimeCurrent() - InpSyntheticTrades * 60;

   for(int i = 0; i < InpSyntheticTrades; i++)
   {
      string feature_key = BuildSyntheticFeatureKey(i);
      double r = SyntheticR(i);
      double risk_money = 100.0;
      double net_profit = r * risk_money;

      DAL_DEAdapter_RecordOutcomeFromMoney(
         g_miner,
         cfg,
         feature_key,
         DAL_DE_LAYER_LIVE,
         (i % 2 == 0 ? 1 : -1),
         t0 + i * 60,
         t0 + (i + 3) * 60,
         100.0,
         100.0 + r,
         99.0,
         103.0,
         risk_money,
         0.10,
         net_profit,
         0.0,
         0.0,
         MathMax(0.0, r),
         MathMin(0.0, r),
         3,
         (ulong)i,
         (ulong)(100000 + i)
      );
   }

   Print(DAL_DEClusterMiner_Report(g_miner, 20));

   DAL_DEClusterFilterConfig fcfg;
   DAL_DEClusterFilterConfig_Default(fcfg);
   fcfg.min_total = 20;
   fcfg.min_decided_total = 20;
   fcfg.min_clusters_ge_3 = 1;
   fcfg.min_win_rate_decided = 0.45;
   fcfg.min_lift_vs_raw = 1.05;
   fcfg.min_p_win_after_1w = 0.50;

   string eligible_keys[];
   DAL_DEClusterFilterDecision decisions[];
   int eligible_count = DAL_DEClusterFilter_CollectEligibleKeys(g_miner, fcfg, eligible_keys, decisions);

   Print("EXP0012 eligible feature groups: ", eligible_count);
   for(int e = 0; e < eligible_count; e++)
      Print(DAL_DEClusterFilterDecision_ToLine(decisions[e]));

   if(InpExportCsv)
   {
      bool ok = DAL_DEClusterMiner_ExportCsv(g_miner, InpExportCsvName);
      Print("EXP0012 CSV export ", (ok ? "OK" : "FAILED"), " file=", InpExportCsvName);
   }

   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Research demo only.
}
