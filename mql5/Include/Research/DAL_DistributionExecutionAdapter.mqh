#ifndef __DAL_DISTRIBUTION_EXECUTION_ADAPTER_MQH__
#define __DAL_DISTRIBUTION_EXECUTION_ADAPTER_MQH__

#include <Research/DAL_DistributionClusterFilter.mqh>

// Decision Alpha Lab
// Distribution Execution Adapter
// Thin helper layer for plugging the Distribution Engineering miner into any EA.
// It does not place trades. It only builds outcomes and feature keys.

struct DAL_DEExecutionAdapterConfig
{
   string          strategy_id;
   string          execution_id;
   string          symbol;
   ENUM_TIMEFRAMES timeframe;
   long            magic;

   double          win_threshold_r;       // e.g. 3.0 for jackpot 3R tests
   double          loss_threshold_r;      // usually -1.0
   bool            use_decided_thresholds;
};

void DAL_DEExecutionAdapterConfig_Default(
   DAL_DEExecutionAdapterConfig &cfg,
   const string strategy_id = "UNKNOWN",
   const string execution_id = "UNKNOWN"
)
{
   cfg.strategy_id = strategy_id;
   cfg.execution_id = execution_id;
   cfg.symbol = _Symbol;
   cfg.timeframe = PERIOD_CURRENT;
   cfg.magic = 0;
   cfg.win_threshold_r = 1.0;
   cfg.loss_threshold_r = -1.0;
   cfg.use_decided_thresholds = true;
}

string DAL_DEAdapter_BaseFeatureKey(
   const string strategy_id,
   const string symbol,
   const ENUM_TIMEFRAMES timeframe
)
{
   string key = "";
   key = DAL_DE_KeyAppend(key, "strategy", strategy_id);
   key = DAL_DE_KeyAppend(key, "symbol", symbol);
   key = DAL_DE_KeyAppend(key, "tf", DAL_DE_TfText(timeframe));
   return key;
}

string DAL_DEAdapter_AddDirectionFeature(const string key, const int direction)
{
   if(direction > 0)
      return DAL_DE_KeyAppend(key, "dir", "buy");
   if(direction < 0)
      return DAL_DE_KeyAppend(key, "dir", "sell");
   return DAL_DE_KeyAppend(key, "dir", "unknown");
}

string DAL_DEAdapter_AddHourFeature(const string key, const datetime t)
{
   int h = DAL_DE_HourOf(t);
   if(h < 0)
      return DAL_DE_KeyAppend(key, "hour", "NA");
   return DAL_DE_KeyAppendInt(key, "hour", h);
}

string DAL_DEAdapter_AddSessionFeature(const string key, const datetime t)
{
   int h = DAL_DE_HourOf(t);
   if(h < 0)
      return DAL_DE_KeyAppend(key, "session", "NA");

   string session = "asia";
   if(h >= 7 && h < 12)
      session = "london_open";
   else if(h >= 12 && h < 17)
      session = "london_ny_overlap";
   else if(h >= 17 && h < 22)
      session = "ny_late";

   return DAL_DE_KeyAppend(key, "session", session);
}

string DAL_DEAdapter_AddRegimeBuckets(
   string key,
   const double atr_ratio,
   const double donchian_width_ratio,
   const double htf_slope,
   const bool htf_aligned,
   const bool path_clean
)
{
   key = DAL_DE_KeyAppendDoubleBucket(key, "atr", atr_ratio, 0.90, 1.20);
   key = DAL_DE_KeyAppendDoubleBucket(key, "donchian_width", donchian_width_ratio, 0.90, 1.20);
   key = DAL_DE_KeyAppendDoubleBucket(key, "htf_slope", htf_slope, -0.10, 0.10);
   key = DAL_DE_KeyAppendBool(key, "htf_aligned", htf_aligned);
   key = DAL_DE_KeyAppendBool(key, "path_clean", path_clean);
   return key;
}

bool DAL_DEAdapter_BuildOutcomeFromMoney(
   const DAL_DEExecutionAdapterConfig &cfg,
   const string feature_key,
   const DAL_DETradeLayer layer,
   const int direction,
   const datetime entry_time,
   const datetime exit_time,
   const double entry_price,
   const double exit_price,
   const double stop_price,
   const double target_price,
   const double risk_money,
   const double volume,
   const double gross_profit,
   const double commission,
   const double swap,
   const double mfe_r,
   const double mae_r,
   const int bars_to_exit,
   const ulong position_id,
   const ulong deal_id,
   DAL_DETradeOutcome &outcome
)
{
   DAL_DETradeOutcome_Reset(outcome);

   outcome.strategy_id  = cfg.strategy_id;
   outcome.execution_id = cfg.execution_id;
   outcome.symbol       = cfg.symbol;
   outcome.timeframe    = cfg.timeframe;
   outcome.magic        = cfg.magic;

   outcome.position_id  = position_id;
   outcome.deal_id      = deal_id;
   outcome.direction    = direction;
   DAL_DETradeOutcome_SetLayer(outcome, layer);

   outcome.entry_time   = entry_time;
   outcome.exit_time    = exit_time;
   outcome.entry_price  = entry_price;
   outcome.exit_price   = exit_price;
   outcome.stop_price   = stop_price;
   outcome.target_price = target_price;
   outcome.risk_money   = risk_money;
   outcome.volume       = volume;

   outcome.gross_profit = gross_profit;
   outcome.commission   = commission;
   outcome.swap         = swap;
   outcome.net_profit   = gross_profit + commission + swap;

   outcome.mfe_r        = mfe_r;
   outcome.mae_r        = mae_r;
   outcome.bars_to_exit = bars_to_exit;
   if(entry_time > 0 && exit_time > 0)
      outcome.seconds_to_exit = (int)(exit_time - entry_time);

   outcome.feature_key  = feature_key;

   DAL_DETradeOutcome_SetRFromMoney(outcome);

   if(cfg.use_decided_thresholds)
      DAL_DETradeOutcome_ClassifyByR(outcome, cfg.win_threshold_r, cfg.loss_threshold_r);
   else
      DAL_DETradeOutcome_ClassifyByR(outcome, 0.0000001, -0.0000001);

   return true;
}

bool DAL_DEAdapter_RecordOutcomeFromMoney(
   DAL_DEClusterMiner &miner,
   const DAL_DEExecutionAdapterConfig &cfg,
   const string feature_key,
   const DAL_DETradeLayer layer,
   const int direction,
   const datetime entry_time,
   const datetime exit_time,
   const double entry_price,
   const double exit_price,
   const double stop_price,
   const double target_price,
   const double risk_money,
   const double volume,
   const double gross_profit,
   const double commission,
   const double swap,
   const double mfe_r,
   const double mae_r,
   const int bars_to_exit,
   const ulong position_id = 0,
   const ulong deal_id = 0
)
{
   DAL_DETradeOutcome outcome;
   if(!DAL_DEAdapter_BuildOutcomeFromMoney(
      cfg,
      feature_key,
      layer,
      direction,
      entry_time,
      exit_time,
      entry_price,
      exit_price,
      stop_price,
      target_price,
      risk_money,
      volume,
      gross_profit,
      commission,
      swap,
      mfe_r,
      mae_r,
      bars_to_exit,
      position_id,
      deal_id,
      outcome
   ))
      return false;

   return DAL_DEClusterMiner_AddOutcome(miner, outcome);
}

bool DAL_DEAdapter_IsFeatureEligible(
   const DAL_DEClusterMiner &miner,
   const string feature_key,
   const DAL_DEClusterFilterConfig &cfg,
   DAL_DEClusterFilterDecision &decision
)
{
   return DAL_DEClusterFilter_EvaluateKey(miner, feature_key, cfg, decision);
}

#endif // __DAL_DISTRIBUTION_EXECUTION_ADAPTER_MQH__
