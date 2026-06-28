#ifndef __DAL_STC_UTILS_MQH__
#define __DAL_STC_UTILS_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Types.mqh>

string STC_BoolText(const bool value)
{
   return value ? "true" : "false";
}

string STC_TimeText(const datetime value)
{
   if(value <= 0) return "";
   return TimeToString(value, TIME_DATE | TIME_SECONDS);
}

string STC_CleanPath(string path)
{
   StringReplace(path, "\\", "/");
   while(StringFind(path, "//") >= 0)
      StringReplace(path, "//", "/");
   while(StringLen(path) > 0 && StringSubstr(path, 0, 1) == "/")
      path = StringSubstr(path, 1);
   while(StringLen(path) > 0 && StringSubstr(path, StringLen(path) - 1, 1) == "/")
      path = StringSubstr(path, 0, StringLen(path) - 1);
   return path;
}

string STC_JoinPath(const string left, const string right)
{
   string l = STC_CleanPath(left);
   string r = STC_CleanPath(right);
   if(l == "") return r;
   if(r == "") return l;
   return l + "/" + r;
}

bool STC_EnsureCommonFolderTree(const string folder)
{
   string clean = STC_CleanPath(folder);
   if(clean == "") return true;

   string parts[];
   int n = StringSplit(clean, StringGetCharacter("/", 0), parts);
   if(n <= 0)
      return FolderCreate(clean, FILE_COMMON) || GetLastError() == 5019;

   string current = "";
   for(int i = 0; i < n; i++)
   {
      if(parts[i] == "") continue;
      current = (current == "") ? parts[i] : current + "/" + parts[i];
      ResetLastError();
      if(!FolderCreate(current, FILE_COMMON))
      {
         int err = GetLastError();
         // 5019 is commonly returned when the folder already exists.
         if(err != 5019)
         {
            // FileOpen later will still be the final truth; keep this helper tolerant across terminals.
            ResetLastError();
         }
      }
   }
   return true;
}

string STC_SafeId(string text)
{
   StringReplace(text, " ", "_");
   StringReplace(text, "/", "_");
   StringReplace(text, "\\", "_");
   StringReplace(text, ":", "_");
   StringReplace(text, ";", "_");
   StringReplace(text, ",", "_");
   StringReplace(text, ".", "_");
   StringReplace(text, "-", "_");
   return text;
}

string STC_MakeLockName(const STC_Config &cfg)
{
   string account = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
   string terminal = IntegerToString(TerminalInfoInteger(TERMINAL_BUILD));
   string key = "DAL_STC_LOCK_" + account + "_" + terminal + "_" + cfg.strategy_id + "_" + cfg.symbol1 + "_" + cfg.symbol2 + "_" + IntegerToString(cfg.magic_number);
   return STC_SafeId(key);
}

bool STC_IsAllowedCheckMinutes(const int minutes)
{
   return (minutes == 1 || minutes == 3 || minutes == 5 || minutes == 10 || minutes == 15 || minutes == 30);
}

bool STC_TrySelectSymbol(const string symbol, string &warning)
{
   if(symbol == "")
   {
      warning = warning + "empty symbol; ";
      return false;
   }
   ResetLastError();
   if(SymbolSelect(symbol, true)) return true;
   int err = GetLastError();
   warning = warning + "SymbolSelect failed for " + symbol + " err=" + IntegerToString(err) + "; ";
   return false;
}

bool STC_ValidateConfig(STC_Config &cfg, string &error, string &warning)
{
   error = "";
   warning = "";

   cfg.output_root_common = STC_CleanPath(cfg.output_root_common);
   cfg.check_minutes = (int)cfg.check_tf;
   if(cfg.timer_seconds < 1) cfg.timer_seconds = 1;
   if(cfg.heartbeat_seconds < 1) cfg.heartbeat_seconds = 60;
   if(cfg.hard_close_retry_seconds < 1) cfg.hard_close_retry_seconds = 5;
   if(cfg.instance_lock_stale_seconds < 10) cfg.instance_lock_stale_seconds = 10;
   if(cfg.max_check_backfill_on_init < 0) cfg.max_check_backfill_on_init = 0;
   if(cfg.max_check_backfill_on_init > 500) cfg.max_check_backfill_on_init = 500;
   if(cfg.max_check_catchup_per_pulse < 1) cfg.max_check_catchup_per_pulse = 1;
   if(cfg.max_check_catchup_per_pulse > 500) cfg.max_check_catchup_per_pulse = 500;
   if(cfg.max_w_level_backfill_on_init < 0) cfg.max_w_level_backfill_on_init = 0;
   if(cfg.max_w_level_backfill_on_init > 12) cfg.max_w_level_backfill_on_init = 12;
   if(cfg.max_w_level_catchup_per_pulse < 1) cfg.max_w_level_catchup_per_pulse = 1;
   if(cfg.max_w_level_catchup_per_pulse > 12) cfg.max_w_level_catchup_per_pulse = 12;
   if(cfg.max_hunt_backfill_on_init < 0) cfg.max_hunt_backfill_on_init = 0;
   if(cfg.max_hunt_backfill_on_init > 500) cfg.max_hunt_backfill_on_init = 500;
   if(cfg.max_hunt_catchup_per_pulse < 1) cfg.max_hunt_catchup_per_pulse = 1;
   if(cfg.max_hunt_catchup_per_pulse > 500) cfg.max_hunt_catchup_per_pulse = 500;

   if(cfg.strategy_id == "") error = error + "strategy_id is empty; ";
   if(cfg.run_id == "")      error = error + "run_id is empty; ";
   if(cfg.symbol1 == "")     error = error + "symbol1 is empty; ";
   if(cfg.symbol2 == "")     error = error + "symbol2 is empty; ";
   if(cfg.symbol1 == cfg.symbol2) error = error + "symbol1 and symbol2 must be different; ";
   if(cfg.final_reward_r <= 0.0) error = error + "final_reward_r must be positive; ";
   if(cfg.risk_percent <= 0.0) error = error + "risk_percent must be positive; ";
   if(cfg.contract_size <= 0.0) error = error + "contract_size must be positive; ";
   if(cfg.magic_number <= 0) error = error + "magic_number must be positive; ";
   if(cfg.output_root_common == "") error = error + "output_root_common is empty; ";
   if(!STC_IsAllowedCheckMinutes(cfg.check_minutes)) error = error + "unsupported check candle minutes; ";

   bool s1 = STC_TrySelectSymbol(cfg.symbol1, warning);
   bool s2 = STC_TrySelectSymbol(cfg.symbol2, warning);
   if(cfg.strict_symbol_validation)
   {
      if(!s1) error = error + "symbol1 is not selectable; ";
      if(!s2) error = error + "symbol2 is not selectable; ";
   }

   return error == "";
}

bool STC_AcquireInstanceLock(STC_Config &cfg, STC_RuntimeState &state)
{
   if(!cfg.use_instance_lock)
   {
      state.lock_acquired = false;
      return true;
   }

   state.lock_name = STC_MakeLockName(cfg);
   double now_value = (double)TimeCurrent();
   if(GlobalVariableCheck(state.lock_name))
   {
      double existing_value = GlobalVariableGet(state.lock_name);
      if(now_value - existing_value < (double)cfg.instance_lock_stale_seconds)
      {
         state.init_status = STC_INIT_INSTANCE_LOCK_ERROR;
         state.init_error = "fresh duplicate instance lock exists: " + state.lock_name;
         return false;
      }
   }
   GlobalVariableSet(state.lock_name, now_value);
   state.lock_acquired = true;
   return true;
}

void STC_RefreshInstanceLock(STC_Config &cfg, STC_RuntimeState &state)
{
   if(cfg.use_instance_lock && state.lock_acquired && state.lock_name != "")
      GlobalVariableSet(state.lock_name, (double)TimeCurrent());
}

void STC_ReleaseInstanceLock(STC_Config &cfg, STC_RuntimeState &state)
{
   if(cfg.use_instance_lock && state.lock_acquired && state.lock_name != "")
      GlobalVariableDel(state.lock_name);
   state.lock_acquired = false;
}

#endif
