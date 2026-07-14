#ifndef __FP_I10_INPUT_VALIDATION_MQH__
#define __FP_I10_INPUT_VALIDATION_MQH__
#include "FP_I10_Contracts.mqh"
#include "FP_I10_Hash.mqh"
bool FP_I10_ValidSymbol(const string symbol){ return StringLen(symbol)>0 && StringLen(symbol)<=64; }
bool FP_I10_ValidHostMinutes(const int minutes){ int allowed[]={1,2,3,4,5,6,10,12,15,20,30,60,120,180,240,360,480,720,1440,10080,43200}; for(int i=0;i<ArraySize(allowed);i++) if(allowed[i]==minutes) return true; return false; }
bool FP_I10_ValidateConfig(SFP_I10_Config &config,string &reason){
 if(!FP_I10_ValidSymbol(config.primary_symbol)||!FP_I10_ValidSymbol(config.secondary_symbol)){reason="FP_IND_SYMBOL_INVALID";return false;}
 if(config.primary_symbol==config.secondary_symbol){reason="FP_IND_SYMBOLS_IDENTICAL";return false;}
 if(!FP_I10_ValidHostMinutes(config.host_timeframe_minutes)){reason="FP_IND_HOST_TIMEFRAME_INVALID";return false;}
 if(config.timer_seconds<1||config.timer_seconds>60){reason="FP_IND_TIMER_SECONDS_INVALID";return false;}
 if(config.history_days<5||config.history_days>3660){reason="FP_IND_HISTORY_DAYS_INVALID";return false;}
 if(config.max_incremental_minutes<1||config.max_incremental_minutes>10080){reason="FP_IND_INCREMENTAL_LIMIT_INVALID";return false;}
 config.pair_id=(config.primary_symbol<config.secondary_symbol?"PAIR-"+config.primary_symbol+"-"+config.secondary_symbol:"PAIR-"+config.secondary_symbol+"-"+config.primary_symbol);
 config.config_hash=FP_I10_Hex64(FP_I10_Fnv1a64(config.context_id+"|"+config.context_epoch+"|"+config.primary_symbol+"|"+config.secondary_symbol+"|"+config.pair_id+"|"+IntegerToString(config.host_timeframe_minutes)+"|"+IntegerToString(config.timer_seconds)+"|"+IntegerToString(config.history_days)+"|"+IntegerToString(config.max_incremental_minutes)));
 reason="FP_IND_INPUT_VALIDATED"; return true;
}
#endif
