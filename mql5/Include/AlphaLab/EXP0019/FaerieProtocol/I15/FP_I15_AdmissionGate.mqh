#ifndef FP_I15_ADMISSION_GATE_MQH
#define FP_I15_ADMISSION_GATE_MQH
#include "FP_I15_Contracts.mqh"
bool FP_I15_Admit(const bool diagnostic_pass,const bool active_i09_winner,const bool pair_data_complete,const datetime watermark,const FP_I15_WinnerInput &winner,string &reason){
 if(!diagnostic_pass){reason="FP_PAPER_DIAGNOSTIC_ACCEPTANCE_NOT_PASS";return false;}
 if(!active_i09_winner){reason="FP_PAPER_NOT_ACTIVE_I09_WINNER";return false;}
 if(!pair_data_complete){reason="FP_PAPER_CAUSAL_DATA_INCOMPLETE";return false;}
 if(watermark<winner.confirmation_close){reason="FP_PAPER_CAUSAL_WATERMARK_BEHIND";return false;}
 reason="FP_PAPER_READY";return true;
}
#endif
