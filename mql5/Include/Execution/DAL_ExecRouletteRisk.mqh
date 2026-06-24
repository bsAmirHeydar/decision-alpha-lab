#ifndef __DAL_EXEC_ROULETTE_RISK_MQH__
#define __DAL_EXEC_ROULETTE_RISK_MQH__

// Decision Alpha Lab — reusable Roulette risk module.
//
// Roulette logic:
// 1) Lock the account balance at the start of a cycle.
// 2) Base risk = locked_balance * initial_risk_percent / 100.
// 3) Floor balance = locked_balance - base_risk.
// 4) While balance is not above the locked balance, next risk is the base risk.
// 5) Once balance is above the locked balance, riskable pool = balance - floor_balance.
// 6) Next risk = max(base_risk, riskable_pool * save_profit_factor).
// 7) On any realized balance drop, reset the cycle by locking the new balance.
//
// The module is execution-agnostic and can be reused by E0001/E0002/... modules.

struct DALExecRouletteRiskState
{
   bool initialized;
   bool persist_state;
   bool reset_on_balance_drop;
   bool last_sync_reset;
   string key;
   string reason;

   double initial_risk_percent;
   double save_profit_factor;
   double locked_balance;
   double floor_balance;
   double base_risk_cash;
   double last_balance;
   double current_balance;
   double current_risk_cash;
};

void DAL_ExecRouletteResetState(DALExecRouletteRiskState &s)
{
   s.initialized = false;
   s.persist_state = true;
   s.reset_on_balance_drop = true;
   s.last_sync_reset = false;
   s.key = "";
   s.reason = "not_initialized";

   s.initial_risk_percent = 10.0;
   s.save_profit_factor = 0.50;
   s.locked_balance = 0.0;
   s.floor_balance = 0.0;
   s.base_risk_cash = 0.0;
   s.last_balance = 0.0;
   s.current_balance = 0.0;
   s.current_risk_cash = 0.0;
}

double DAL_ExecRouletteClamp(const double value, const double lo, const double hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string DAL_ExecRouletteSanitizeKey(const string raw_key)
{
   string out = "";
   int n = StringLen(raw_key);
   for(int i = 0; i < n; i++)
   {
      ushort ch = StringGetCharacter(raw_key, i);
      bool ok = ((ch >= '0' && ch <= '9') || (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || ch == '_');
      if(ok)
         out += ShortToString(ch);
      else
         out += "_";
   }

   if(out == "")
      out = "default";

   if(StringLen(out) > 38)
      out = StringSubstr(out, 0, 38);

   return out;
}

string DAL_ExecRouletteGVName(const string key, const string field)
{
   return "DAL_RLT_" + DAL_ExecRouletteSanitizeKey(key) + "_" + field;
}

bool DAL_ExecRouletteGVGet(const string key, const string field, double &value)
{
   string name = DAL_ExecRouletteGVName(key, field);
   if(!GlobalVariableCheck(name))
      return false;
   value = GlobalVariableGet(name);
   return true;
}

void DAL_ExecRouletteGVSet(const string key, const string field, const double value)
{
   string name = DAL_ExecRouletteGVName(key, field);
   GlobalVariableSet(name, value);
}

void DAL_ExecRoulettePersist(const DALExecRouletteRiskState &s)
{
   if(!s.persist_state || s.key == "")
      return;

   DAL_ExecRouletteGVSet(s.key, "init", 1.0);
   DAL_ExecRouletteGVSet(s.key, "lock", s.locked_balance);
   DAL_ExecRouletteGVSet(s.key, "floor", s.floor_balance);
   DAL_ExecRouletteGVSet(s.key, "base", s.base_risk_cash);
   DAL_ExecRouletteGVSet(s.key, "last", s.last_balance);
   DAL_ExecRouletteGVSet(s.key, "risk", s.current_risk_cash);
   DAL_ExecRouletteGVSet(s.key, "pct", s.initial_risk_percent);
   DAL_ExecRouletteGVSet(s.key, "save", s.save_profit_factor);
}

bool DAL_ExecRouletteLoad(DALExecRouletteRiskState &s)
{
   if(!s.persist_state || s.key == "")
      return false;

   double init = 0.0;
   if(!DAL_ExecRouletteGVGet(s.key, "init", init) || init < 0.5)
      return false;

   double locked = 0.0;
   double floor_balance = 0.0;
   double base_risk = 0.0;
   double last_balance = 0.0;
   double risk_cash = 0.0;

   if(!DAL_ExecRouletteGVGet(s.key, "lock", locked))
      return false;
   if(!DAL_ExecRouletteGVGet(s.key, "floor", floor_balance))
      return false;
   if(!DAL_ExecRouletteGVGet(s.key, "base", base_risk))
      return false;
   if(!DAL_ExecRouletteGVGet(s.key, "last", last_balance))
      return false;
   DAL_ExecRouletteGVGet(s.key, "risk", risk_cash);

   if(locked <= 0.0 || base_risk <= 0.0)
      return false;

   s.initialized = true;
   s.locked_balance = locked;
   s.floor_balance = floor_balance;
   s.base_risk_cash = base_risk;
   s.last_balance = last_balance;
   s.current_risk_cash = risk_cash;
   s.reason = "loaded_persisted_state";
   return true;
}

void DAL_ExecRouletteLockCycle(
   DALExecRouletteRiskState &s,
   const double balance,
   const double initial_risk_percent,
   const double save_profit_factor,
   const string reset_reason
)
{
   s.initial_risk_percent = DAL_ExecRouletteClamp(initial_risk_percent, 0.01, 100.0);
   s.save_profit_factor = DAL_ExecRouletteClamp(save_profit_factor, 0.0, 1.0);
   s.locked_balance = MathMax(0.0, balance);
   s.base_risk_cash = s.locked_balance * s.initial_risk_percent / 100.0;
   s.floor_balance = s.locked_balance - s.base_risk_cash;
   s.last_balance = s.locked_balance;
   s.current_balance = s.locked_balance;
   s.current_risk_cash = s.base_risk_cash;
   s.initialized = true;
   s.last_sync_reset = true;
   s.reason = reset_reason;
   DAL_ExecRoulettePersist(s);
}

bool DAL_ExecRouletteInit(
   DALExecRouletteRiskState &s,
   const string storage_key,
   const double initial_risk_percent,
   const double save_profit_factor,
   const bool persist_state,
   const bool reset_on_balance_drop
)
{
   DAL_ExecRouletteResetState(s);
   s.key = storage_key;
   s.persist_state = persist_state;
   s.reset_on_balance_drop = reset_on_balance_drop;
   s.initial_risk_percent = DAL_ExecRouletteClamp(initial_risk_percent, 0.01, 100.0);
   s.save_profit_factor = DAL_ExecRouletteClamp(save_profit_factor, 0.0, 1.0);

   if(DAL_ExecRouletteLoad(s))
      return true;

   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   if(balance <= 0.0)
   {
      s.reason = "invalid_account_balance";
      return false;
   }

   DAL_ExecRouletteLockCycle(s, balance, s.initial_risk_percent, s.save_profit_factor, "initialized_new_cycle");
   return true;
}

bool DAL_ExecRouletteSync(
   DALExecRouletteRiskState &s,
   const double initial_risk_percent,
   const double save_profit_factor
)
{
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   if(balance <= 0.0)
   {
      s.reason = "invalid_account_balance";
      return false;
   }

   if(!s.initialized)
   {
      DAL_ExecRouletteLockCycle(s, balance, initial_risk_percent, save_profit_factor, "sync_initialized_new_cycle");
      return true;
   }

   s.last_sync_reset = false;
   s.current_balance = balance;
   s.initial_risk_percent = DAL_ExecRouletteClamp(initial_risk_percent, 0.01, 100.0);
   s.save_profit_factor = DAL_ExecRouletteClamp(save_profit_factor, 0.0, 1.0);

   double eps = MathMax(0.01, MathAbs(s.last_balance) * 1.0e-8);

   if(s.reset_on_balance_drop && balance < s.last_balance - eps)
   {
      DAL_ExecRouletteLockCycle(s, balance, s.initial_risk_percent, s.save_profit_factor, "balance_drop_reset_cycle");
      return true;
   }

   // Recalculate base/floor from the locked balance and the current input percentage.
   s.base_risk_cash = s.locked_balance * s.initial_risk_percent / 100.0;
   s.floor_balance = s.locked_balance - s.base_risk_cash;

   if(balance <= s.locked_balance + eps)
   {
      s.current_risk_cash = s.base_risk_cash;
      s.reason = "base_risk_until_profit";
   }
   else
   {
      double riskable_pool = MathMax(0.0, balance - s.floor_balance);
      double profit_scaled_risk = riskable_pool * s.save_profit_factor;
      s.current_risk_cash = MathMax(s.base_risk_cash, profit_scaled_risk);
      s.reason = "profit_scaled_risk";
   }

   s.last_balance = balance;
   DAL_ExecRoulettePersist(s);
   return true;
}

bool DAL_ExecRouletteRiskCash(
   DALExecRouletteRiskState &s,
   const double initial_risk_percent,
   const double save_profit_factor,
   double &risk_cash,
   string &reason
)
{
   risk_cash = 0.0;
   reason = "not_calculated";

   if(!DAL_ExecRouletteSync(s, initial_risk_percent, save_profit_factor))
   {
      reason = s.reason;
      return false;
   }

   if(s.current_risk_cash <= 0.0)
   {
      reason = "non_positive_roulette_risk";
      return false;
   }

   risk_cash = s.current_risk_cash;
   reason = s.reason;
   return true;
}

string DAL_ExecRouletteStateToString(const DALExecRouletteRiskState &s)
{
   return "key=" + s.key
      + "*reason=" + s.reason
      + "*locked=" + DoubleToString(s.locked_balance, 2)
      + "*floor=" + DoubleToString(s.floor_balance, 2)
      + "*baseRisk=" + DoubleToString(s.base_risk_cash, 2)
      + "*balance=" + DoubleToString(s.current_balance, 2)
      + "*lastBalance=" + DoubleToString(s.last_balance, 2)
      + "*risk=" + DoubleToString(s.current_risk_cash, 2)
      + "*pct=" + DoubleToString(s.initial_risk_percent, 2)
      + "*saveFactor=" + DoubleToString(s.save_profit_factor, 2)
      + "*reset=" + (s.last_sync_reset ? "true" : "false");
}

#endif // __DAL_EXEC_ROULETTE_RISK_MQH__
