#ifndef __DAL_EXEC_ROULETTE_RISK_MQH__
#define __DAL_EXEC_ROULETTE_RISK_MQH__

// Decision Alpha Lab — reusable Roulette risk module.
// Pure MQL5. No Python or external scripts.
//
// Correct cycle rule:
// - The locked balance is fixed at cycle start.
// - Base risk is fixed as initial_risk_percent of locked balance.
// - Losing movement below the protected floor does NOT reduce risk.
// - Risk stays at base risk until the cycle first becomes profitable.
// - After profit, risk can expand from current_balance - floor_balance.
// - If profit was active and a realized balance drop occurs, the cycle resets
//   to the balance after the loss. Further losses keep that new base risk.

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

   return (st.initialized && st.locked_balance > 0.0 && st.base_risk > 0.0);
}

void DAL_ExecRouletteStartNewCycle(
   const DALExecRouletteRiskConfig &cfg,
   DALExecRouletteRiskState &st,
   const double balance
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

   if(cfg.print_logs)
   {
      Print("DAL_ROULETTE_RESET *** cycle=", st.cycle_id,
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
   DAL_ExecRouletteStartNewCycle(cfg, st, balance);
   return true;
}

double DAL_ExecRouletteRiskMoney(const DALExecRouletteRiskConfig &cfg, const DALExecRouletteRiskState &st)
{
   if(!st.initialized)
      return 0.0;

   double risk = st.base_risk;
   double current_balance = AccountInfoDouble(ACCOUNT_BALANCE);

   if(st.profit_active && current_balance > st.locked_balance)
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

   // The only automatic reset rule:
   // reset after the cycle has already been in profit and balance then drops.
   if(st.profit_active && current_balance < st.last_balance - eps)
   {
      DAL_ExecRouletteStartNewCycle(cfg, st, current_balance);
      return;
   }

   if(current_balance > st.locked_balance + eps)
      st.profit_active = true;

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
