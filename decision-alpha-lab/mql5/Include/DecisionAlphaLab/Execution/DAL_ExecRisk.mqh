#ifndef __DAL_EXEC_RISK_MQH__
#define __DAL_EXEC_RISK_MQH__

// Decision Alpha Lab — execution risk primitives.
// Converts a cash-risk budget into a lot size using stop distance plus an
// optional round-turn commission estimate per 1.00 lot.

#include <DecisionAlphaLab/Common/DAL_Common.mqh>

struct DALExecRiskSizing
{
   bool ok;
   string reason;
   double entry_price;
   double stop_price;
   double stop_distance_price;
   double risk_cash_requested;
   double commission_per_lot_round_turn;
   double tick_size;
   double tick_value_loss;
   double volume_min;
   double volume_max;
   double volume_step;
   double stop_loss_cash_per_lot;
   double total_risk_cash_per_lot;
   double raw_volume;
   double volume;
   double estimated_stop_loss_cash;
   double estimated_commission_cash;
   double estimated_total_risk_cash;
};

void DAL_ExecResetRiskSizing(DALExecRiskSizing &r)
{
   r.ok = false;
   r.reason = "not_calculated";
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.stop_distance_price = 0.0;
   r.risk_cash_requested = 0.0;
   r.commission_per_lot_round_turn = 0.0;
   r.tick_size = 0.0;
   r.tick_value_loss = 0.0;
   r.volume_min = 0.0;
   r.volume_max = 0.0;
   r.volume_step = 0.0;
   r.stop_loss_cash_per_lot = 0.0;
   r.total_risk_cash_per_lot = 0.0;
   r.raw_volume = 0.0;
   r.volume = 0.0;
   r.estimated_stop_loss_cash = 0.0;
   r.estimated_commission_cash = 0.0;
   r.estimated_total_risk_cash = 0.0;
}

int DAL_ExecVolumeDigitsFromStep(const double step)
{
   if(step <= 0.0)
      return 2;
   for(int d = 0; d <= 8; d++)
   {
      double scaled = step * MathPow(10.0, d);
      if(MathAbs(scaled - MathRound(scaled)) < 1e-8)
         return d;
   }
   return 8;
}

double DAL_ExecFloorToStep(const double value, const double step)
{
   if(step <= 0.0)
      return value;
   return MathFloor((value / step) + 1e-12) * step;
}

double DAL_ExecNormalizeVolumeFloor(const string symbol, const double raw_volume)
{
   double vmax = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   double step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   if(step <= 0.0)
      step = 0.01;

   double v = DAL_ExecFloorToStep(raw_volume, step);
   if(v > vmax)
      v = vmax;

   int digits = DAL_ExecVolumeDigitsFromStep(step);
   return NormalizeDouble(v, digits);
}

bool DAL_ExecCalculateRiskVolume(
   const string symbol,
   const double entry_price,
   const double stop_price,
   const double risk_cash,
   const double commission_per_lot_round_turn,
   const bool allow_min_lot_if_risk_too_small,
   DALExecRiskSizing &out
)
{
   DAL_ExecResetRiskSizing(out);
   out.entry_price = entry_price;
   out.stop_price = stop_price;
   out.risk_cash_requested = risk_cash;
   out.commission_per_lot_round_turn = MathMax(0.0, commission_per_lot_round_turn);

   if(symbol == "") { out.reason = "empty_symbol"; return false; }
   if(risk_cash <= 0.0) { out.reason = "risk_cash_must_be_positive"; return false; }

   out.stop_distance_price = MathAbs(entry_price - stop_price);
   if(out.stop_distance_price <= 0.0) { out.reason = "zero_stop_distance"; return false; }

   out.tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   if(out.tick_size <= 0.0)
      out.tick_size = SymbolInfoDouble(symbol, SYMBOL_POINT);

   out.tick_value_loss = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE_LOSS);
   if(out.tick_value_loss <= 0.0)
      out.tick_value_loss = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);

   out.volume_min = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   out.volume_max = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   out.volume_step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

   if(out.tick_size <= 0.0 || out.tick_value_loss <= 0.0)
   {
      out.reason = "invalid_tick_size_or_value";
      return false;
   }
   if(out.volume_min <= 0.0 || out.volume_max <= 0.0 || out.volume_step <= 0.0)
   {
      out.reason = "invalid_volume_specs";
      return false;
   }

   out.stop_loss_cash_per_lot = (out.stop_distance_price / out.tick_size) * out.tick_value_loss;
   out.total_risk_cash_per_lot = out.stop_loss_cash_per_lot + out.commission_per_lot_round_turn;
   if(out.total_risk_cash_per_lot <= 0.0) { out.reason = "invalid_risk_per_lot"; return false; }

   out.raw_volume = risk_cash / out.total_risk_cash_per_lot;
   out.volume = DAL_ExecNormalizeVolumeFloor(symbol, out.raw_volume);

   if(out.volume < out.volume_min)
   {
      if(!allow_min_lot_if_risk_too_small)
      {
         out.reason = "volume_below_min_for_risk_budget";
         return false;
      }
      out.volume = out.volume_min;
   }

   if(out.volume > out.volume_max)
      out.volume = out.volume_max;

   int digits = DAL_ExecVolumeDigitsFromStep(out.volume_step);
   out.volume = NormalizeDouble(out.volume, digits);
   if(out.volume <= 0.0) { out.reason = "normalized_volume_zero"; return false; }

   out.estimated_stop_loss_cash = out.stop_loss_cash_per_lot * out.volume;
   out.estimated_commission_cash = out.commission_per_lot_round_turn * out.volume;
   out.estimated_total_risk_cash = out.estimated_stop_loss_cash + out.estimated_commission_cash;

   if(!allow_min_lot_if_risk_too_small && out.estimated_total_risk_cash - risk_cash > MathMax(0.01, risk_cash * 0.0001))
   {
      out.reason = "estimated_risk_exceeds_budget";
      return false;
   }

   out.ok = true;
   out.reason = "ok";
   return true;
}

string DAL_ExecRiskSizingToLog(const DALExecRiskSizing &r)
{
   return "riskOk=" + DAL_BoolToString(r.ok)
      + "*riskReason=" + r.reason
      + "*riskCash=" + DoubleToString(r.risk_cash_requested, 2)
      + "*entry=" + DoubleToString(r.entry_price, 8)
      + "*stop=" + DoubleToString(r.stop_price, 8)
      + "*stopDistance=" + DoubleToString(r.stop_distance_price, 8)
      + "*commissionPerLotRT=" + DoubleToString(r.commission_per_lot_round_turn, 2)
      + "*stopLossCashPerLot=" + DoubleToString(r.stop_loss_cash_per_lot, 2)
      + "*totalRiskCashPerLot=" + DoubleToString(r.total_risk_cash_per_lot, 2)
      + "*rawVolume=" + DoubleToString(r.raw_volume, 8)
      + "*volume=" + DoubleToString(r.volume, 8)
      + "*estimatedStopLossCash=" + DoubleToString(r.estimated_stop_loss_cash, 2)
      + "*estimatedCommissionCash=" + DoubleToString(r.estimated_commission_cash, 2)
      + "*estimatedTotalRiskCash=" + DoubleToString(r.estimated_total_risk_cash, 2);
}

#endif
