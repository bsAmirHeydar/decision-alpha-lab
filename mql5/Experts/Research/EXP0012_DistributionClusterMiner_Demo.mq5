#property strict
#property version   "1.00"
#property description "EXP0012 Distributional Cluster Miner demo. Research-only. No trading."

#include <Research/DAL_DistributionClusterMiner.mqh>
#include <Research/DAL_DistributionClusterFilter.mqh>

input bool   InpPrintDemoReport = true;
input string InpDemoStrategyId  = "EXP0012_DEMO";

DAL_DEClusterMiner       g_miner;
DAL_DEClusterFilterConfig g_filter_cfg;

void AddDemoOutcome(const string key, const bool win, const double r_result)
{
   DAL_DETradeOutcome o;
   DAL_DETradeOutcome_Reset(o);

   o.strategy_id  = InpDemoStrategyId;
   o.symbol       = _Symbol;
   o.timeframe    = PERIOD_M1;
   o.direction    = 1;
   o.entry_time   = TimeCurrent();
   o.exit_time    = TimeCurrent();
   o.entry_price  = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   o.stop_price   = o.entry_price - 100.0 * _Point;
   o.target_price = o.entry_price + 300.0 * _Point;
   o.r_result     = r_result;
   o.mfe_r        = (win ? 3.0 : 0.5);
   o.mae_r        = (win ? -0.3 : -1.0);
   o.bars_to_exit = (win ? 8 : 5);
   o.is_win       = win;
   o.is_loss      = !win;
   o.feature_key  = key;

   DAL_DEClusterMiner_AddOutcome(g_miner, o);
}

int OnInit()
{
   DAL_DEClusterMiner_Init(g_miner, InpDemoStrategyId, 3, 5, 7, 10);
   DAL_DEClusterFilterConfig_Default(g_filter_cfg);

   // Synthetic demonstration only. Real execution modules should emit actual
   // closed trade outcomes from their OnTradeTransaction / tester logic.
   string raw_key = "atr=mid|donchian=mid|htf=mixed";
   string cluster_key = "atr=high|donchian=high|htf=aligned";

   for(int i = 0; i < 60; i++)
   {
      bool w = ((i % 3) == 0);
      AddDemoOutcome(raw_key, w, (w ? 3.0 : -1.0));
   }

   // Clustered block: intentionally creates win-after-win behavior.
   for(int j = 0; j < 8; j++)
      AddDemoOutcome(cluster_key, true, 3.0);
   AddDemoOutcome(cluster_key, false, -1.0);

   for(int k = 0; k < 8; k++)
      AddDemoOutcome(cluster_key, true, 3.0);
   AddDemoOutcome(cluster_key, false, -1.0);

   if(InpPrintDemoReport)
      DAL_DEClusterMiner_PrintReport(g_miner, 20);

   Print(DAL_DEClusterFilter_Reason(g_miner, g_filter_cfg, cluster_key));

   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Research-only demo. No trading.
}
