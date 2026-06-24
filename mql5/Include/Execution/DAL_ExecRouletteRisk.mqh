#ifndef __DAL_EXEC_ROULETTE_RISK_MQH__
#define __DAL_EXEC_ROULETTE_RISK_MQH__

// Decision Alpha Lab — reusable Roulette risk module.
// Pure MQL5. No Python. No external scripts.
//
// Roulette cycle rule, corrected:
// 1) At cycle start, lock the current account balance.
// 2) Base risk is fixed as initial_risk_percent of locked_balance.
// 3) floor_balance = locked_balance - base_risk.
// 4) While balance is between floor_balance and locked_balance, risk remains base_risk.
// 5) If balance breaks below floor_balance before profit, the cycle is re-locked downward:
//      locked_balance = current_balance
//      base_risk      = current_balance * initial_risk_percent / 100
//      floor_balance  = locked_balance - base_risk
//    This means the base account used for volume calculation follows the account down only
//    after the protected floor is broken.
// 6) The cycle becomes profit-active only after balance rises above locked_balance.
// 7) While profit-active and above locked_balance, risk may expand from:
//      current_balance - floor_balance, multiplied by save_profit_factor.
// 8) If the cycle was profit-active and a realized balance drop occurs,
//    reset/re-lock the cycle to the balance after that loss.
// 9) After any re-lock, losses above the new floor keep the new base_risk fixed.
//    If the new floor is broken again, the base re-locks downward again.
//
// This module only returns money risk. It never sends orders and never decides entries.

struct DALExecRouletteRiskConfig
{
   double initial_risk_percent;
   double save_profit_factor;
   bool persist_state;
   string state_key;
   bool print_logs;
};

struct DALExecRouletteRiskState
{
   bool initialized;
   bool profit_active;
   int cycle_id;
   double locked_balance;
   double base_risk;
   double floor_balance;
   double last_balance;
   double peak_balance;
   double last_risk_cash;
   string last_reason;
};

string DAL_ExecRouletteBoolToString(const bool v)
{
   return (v ? "true" : "false");
}

void DAL_ExecRouletteRiskDefaults(DALExecRouletteRiskConfig &cfg)
{
   cfg.initial_risk_percent = 10.0;
   cfg.save_profit_factor = 0.50;
   cfg.persist_state = true;
   cfg.state_key = "default";
   cfg.print_logs = false;
}

void DAL_ExecRouletteRiskResetState(DALExecRouletteRiskState &st)
{
   st.initialized = false;
   st.profit_active = false;
   st.cycle_id = 0;
   st.locked_balance = 0.0;
   st.base_risk = 0.0;
   st.floor_balance = 0.0;
   st.last_balance = 0.0;
   st.peak_balance = 0.0;
   st.last_risk_cash = 0.0;
   st.last_reason = "not_initialized";
}

string DAL_ExecRoulettePrefix(const DALExecRouletteRiskConfig &cfg)
{
   long login = (long)AccountInfoInteger(ACCOUNT_LOGIN);
   string key = cfg.state_key;
   if(key == "")
      key = "default";
   return "DAL_ROULETTE_" + IntegerToString((int)login) + "_" + key;
}

void DAL_ExecRouletteSave(const DALExecRouletteRiskConfig &cfg, const DALExecRouletteRiskState &st)
{
   if(!cfg.persist_state)
      return;

   string p = DAL_ExecRoulettePrefix(cfg);
   GlobalVariableSet(p + "_initialized", st.initialized ? 1.0 : 0.0);
   GlobalVariableSet(p + "_profit_active", st.profit_active ? 1.0 : 0.0);
   GlobalVariableSet(p + "_cycle_id", (double)st.cycle_id);
   GlobalVariableSet(p + "_locked_balance", st.locked_balance);
   GlobalVariableSet(p + "_base_risk", st.base_risk);
   GlobalVariableSet(p + "_floor_balance", st.floor_balance);
   GlobalVariableSet(p + "_last_balance", st.last_balance);
   GlobalVariableSet(p + "_peak_balance", st.peak_balance);
   GlobalVariableSet(p + "_last_risk_cash", st.last_risk_cash);
}

bool DAL_ExecRouletteLoad(const DALExecRouletteRiskConfig &cfg, DALExecRouletteRiskState &st)
{
   if(!cfg.persist_state)
      return false;

   string p = DAL_ExecRoulettePrefix(cfg);
   if(!GlobalVariableCheck(p + "_initialized"))
      return false;

   st.initialized = (GlobalVariableGet(p + "_initialized") > 0.5);
   st.profit_active = (GlobalVariableGet(p + "_profit_active") > 0.5);
   st.cycle_id = (int)GlobalVariableGet(p + "_cycle_id");
   st.locked_balance = GlobalVariableGet(p + "_locked_balance");
   st.base_risk = GlobalVariableGet(p + "_base_risk");
   st.floor_balance = GlobalVariableGet(p + "_floor_balance");
   st.last_balance = GlobalVariableGet(p + "_last_balance");
   st.peak_balance = GlobalVariableGet(p + "_peak_balance");
   st.last_risk_cash = GlobalVariableGet(p + "_last_risk_cash");
   st.last_reason = "loaded";

   return (st.initialized && st.locked_balance > 0.0 && st.base_risk > 0.0);
}

void DAL_ExecRouletteStartNewCycle(
   const DALExecRouletteRiskConfig &cfg,
   DALExecRouletteRiskState &st,
   const double balance,
   const string reason
)
{
   double b = MathMax(0.0, balance);
   double pct = MathMax(0.0, cfg.initial_risk_percent) / 100.0;

   int next_cycle = st.cycle_id + 1;
   st.initialized = true;
   st.profit_active = false;
   st.cycle_id = next_cycle;
   st.locked_balance = b;
   st.base_risk = b * pct;
   st.floor_balance = st.locked_balance - st.base_risk;
   st.last_balance = b;
   st.peak_balance = b;
   st.last_risk_cash = st.base_risk;
   st.last_reason = reason;

   if(cfg.print_logs)
   {
      Print("DAL_ROULETTE_RELOCK *** reason=", reason,
         "*cycle=", st.cycle_id,
         "*locked=", DoubleToString(st.locked_balance, 2),
         "*baseRisk=", DoubleToString(st.base_risk, 2),
         "*floor=", DoubleToString(st.floor_balance, 2));
   }

   DAL_ExecRouletteSave(cfg, st);
}

bool DAL_ExecRouletteInit(DALExecRouletteRiskConfig &cfg, DALExecRouletteRiskState &st)
{
   if(cfg.initial_risk_percent < 0.0)
      cfg.initial_risk_percent = 0.0;
   if(cfg.save_profit_factor < 0.0)
      cfg.save_profit_factor = 0.0;

   DAL_ExecRouletteRiskResetState(st);
   if(DAL_ExecRouletteLoad(cfg, st))
      return true;

   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   DAL_ExecRouletteStartNewCycle(cfg, st, balance, "initial_lock");
   return true;
}

double DAL_ExecRouletteRiskMoney(const DALExecRouletteRiskConfig &cfg, const DALExecRouletteRiskState &st)
{
   if(!st.initialized)
      return 0.0;

   double risk = st.base_risk;
   double current_balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double pct = MathMax(0.0, cfg.initial_risk_percent) / 100.0;

   // If the protected floor has already been broken but Update() has not run yet,
   // return the prospective downside re-locked risk for volume safety.
   if(current_balance > 0.0 && current_balance < st.floor_balance)
   {
      risk = current_balance * pct;
   }
   else if(st.profit_active && current_balance > st.locked_balance)
   {
      double pool = current_balance - st.floor_balance;
      double raw = pool * MathMax(0.0, cfg.save_profit_factor);
      risk = MathMax(st.base_risk, raw);
   }

   if(!MathIsValidNumber(risk) || risk < 0.0)
      risk = st.base_risk;

   return MathMax(0.0, risk);
}

void DAL_ExecRouletteUpdate(DALExecRouletteRiskConfig &cfg, DALExecRouletteRiskState &st)
{
   if(!st.initialized)
   {
      DAL_ExecRouletteInit(cfg, st);
      return;
   }

   double current_balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double eps = MathMax(0.01, MathAbs(st.locked_balance) * 0.0000001);

   // Profit-then-loss reset has priority. Once the cycle was in profit,
   // the first realized balance drop re-locks the base at the post-loss balance.
   if(st.profit_active && current_balance < st.last_balance - eps)
   {
      DAL_ExecRouletteStartNewCycle(cfg, st, current_balance, "profit_then_loss_relock");
      return;
   }

   // Downside floor break. Before a profit-active cycle exists, ordinary loss inside
   // [floor_balance, locked_balance] keeps the base risk fixed. But once the balance
   // breaks below floor_balance, the base account used for volume calculation follows
   // the account down and the cycle is re-locked at the current balance.
   if(current_balance < st.floor_balance - eps)
   {
      DAL_ExecRouletteStartNewCycle(cfg, st, current_balance, "downside_floor_break_relock");
      return;
   }

   if(current_balance > st.locked_balance + eps)
   {
      st.profit_active = true;
      st.last_reason = "profit_active_scaled";
   }
   else
   {
      st.last_reason = "base_risk_inside_floor_band";
   }

   if(current_balance > st.peak_balance)
      st.peak_balance = current_balance;

   st.last_balance = current_balance;
   st.last_risk_cash = DAL_ExecRouletteRiskMoney(cfg, st);

   DAL_ExecRouletteSave(cfg, st);
}

string DAL_ExecRouletteStateToLog(const DALExecRouletteRiskConfig &cfg, const DALExecRouletteRiskState &st)
{
   double current_balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double risk = DAL_ExecRouletteRiskMoney(cfg, st);
   return "rouletteInitialized=" + DAL_ExecRouletteBoolToString(st.initialized)
      + "*rouletteReason=" + st.last_reason
      + "*rouletteProfitActive=" + DAL_ExecRouletteBoolToString(st.profit_active)
      + "*rouletteCycle=" + IntegerToString(st.cycle_id)
      + "*balance=" + DoubleToString(current_balance, 2)
      + "*locked=" + DoubleToString(st.locked_balance, 2)
      + "*baseRisk=" + DoubleToString(st.base_risk, 2)
      + "*floor=" + DoubleToString(st.floor_balance, 2)
      + "*peak=" + DoubleToString(st.peak_balance, 2)
      + "*saveFactor=" + DoubleToString(cfg.save_profit_factor, 4)
      + "*riskMoney=" + DoubleToString(risk, 2);
}

#endif
