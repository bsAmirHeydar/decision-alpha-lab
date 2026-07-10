
#ifndef __EXP0018_DAYE_SYMBOL_CONTRACT_MQH__
#define __EXP0018_DAYE_SYMBOL_CONTRACT_MQH__

#include <DayeTrader/EXP0018/DAYE_DataTypes.mqh>

string DAYE_DataCleanString(const string value)
{
   string result = value;
   StringTrimLeft(result);
   StringTrimRight(result);
   return result;
}

bool DAYE_ValidateDataSyncConfig(const DAYE_DataSyncConfig &config,string &reason_code)
{
   reason_code = "";
   if(config.schema_version != DAYE_DATA_SCHEMA_VERSION)
   {
      reason_code = "data_schema_version_mismatch";
      return false;
   }
   if(DAYE_DataCleanString(config.broker_symbol_a) == "" || DAYE_DataCleanString(config.broker_symbol_b) == "")
   {
      reason_code = "empty_broker_symbol";
      return false;
   }
   if(config.broker_symbol_a == config.broker_symbol_b)
   {
      reason_code = "symbols_must_be_distinct";
      return false;
   }
   if(PeriodSeconds(config.base_timeframe) <= 0)
   {
      reason_code = "invalid_base_timeframe";
      return false;
   }
   if(config.requested_bars_per_symbol < 2)
   {
      reason_code = "requested_bars_too_small";
      return false;
   }
   if(config.minimum_common_bars < 1 || config.minimum_common_bars > config.requested_bars_per_symbol)
   {
      reason_code = "invalid_minimum_common_bars";
      return false;
   }
   if(config.maximum_pairs_to_publish < 1)
   {
      reason_code = "invalid_maximum_pairs_to_publish";
      return false;
   }
   if(config.enforce_freshness && config.maximum_latest_bar_age_seconds < 1)
   {
      reason_code = "invalid_freshness_threshold";
      return false;
   }
   if(config.force_full_refresh_seconds < 1)
   {
      reason_code = "invalid_force_refresh_seconds";
      return false;
   }
   return true;
}

bool DAYE_EnsureSymbolSelected(const string symbol,string &reason_code)
{
   reason_code = "";
   bool is_custom_symbol = false;
   if(!SymbolExist(symbol,is_custom_symbol))
   {
      reason_code = "symbol_does_not_exist";
      return false;
   }
   if(!SymbolSelect(symbol,true))
   {
      reason_code = "symbol_select_failed_" + IntegerToString(GetLastError());
      return false;
   }
   long selected = 0;
   if(!SymbolInfoInteger(symbol,SYMBOL_SELECT,selected) || selected == 0)
   {
      reason_code = "symbol_not_selected_after_request";
      return false;
   }
   return true;
}

bool DAYE_LoadSymbolDescriptor(const string broker_symbol,const string canonical_symbol,DAYE_SymbolDescriptor &descriptor)
{
   ZeroMemory(descriptor);
   descriptor.schema_version = DAYE_DATA_SCHEMA_VERSION;
   descriptor.broker_symbol = DAYE_DataCleanString(broker_symbol);
   descriptor.canonical_symbol = DAYE_DataCleanString(canonical_symbol);
   if(descriptor.canonical_symbol == "")
      descriptor.canonical_symbol = descriptor.broker_symbol;

   string reason = "";
   if(!DAYE_EnsureSymbolSelected(descriptor.broker_symbol,reason))
   {
      descriptor.status = DAYE_DATA_STATUS_SYMBOL_NOT_SELECTED;
      descriptor.reason_code = reason;
      return false;
   }

   long visible = 0;
   long selected = 0;
   long digits = 0;
   double point = 0.0;
   if(!SymbolInfoInteger(descriptor.broker_symbol,SYMBOL_VISIBLE,visible) ||
      !SymbolInfoInteger(descriptor.broker_symbol,SYMBOL_SELECT,selected) ||
      !SymbolInfoInteger(descriptor.broker_symbol,SYMBOL_DIGITS,digits) ||
      !SymbolInfoDouble(descriptor.broker_symbol,SYMBOL_POINT,point))
   {
      descriptor.status = DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE;
      descriptor.reason_code = "symbol_metadata_unavailable_" + IntegerToString(GetLastError());
      return false;
   }

   descriptor.visible = (visible != 0);
   descriptor.selected = (selected != 0);
   descriptor.digits = (int)digits;
   descriptor.point = point;
   descriptor.status = DAYE_DATA_STATUS_OK;
   descriptor.reason_code = "ok";
   return true;
}

#endif
