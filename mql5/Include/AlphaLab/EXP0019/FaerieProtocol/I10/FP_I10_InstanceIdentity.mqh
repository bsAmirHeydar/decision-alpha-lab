#ifndef __FP_I10_INSTANCE_IDENTITY_MQH__
#define __FP_I10_INSTANCE_IDENTITY_MQH__
#include "FP_I10_Contracts.mqh"
#include "FP_I10_Hash.mqh"
SFP_I10_Instance FP_I10_BuildInstance(const SFP_I10_Config &config,const long chart_id){
 SFP_I10_Instance x; x.chart_id=chart_id; x.terminal_instance_id=TerminalInfoString(TERMINAL_DATA_PATH); string material=IntegerToString(chart_id)+"|"+x.terminal_instance_id+"|"+config.pair_id+"|"+config.context_epoch+"|"+config.config_hash; x.instance_id=FP_I10_StableId("FPINST",material); x.pair_id=config.pair_id; x.context_epoch=config.context_epoch; x.config_hash=config.config_hash; x.object_namespace="FP19::"+x.instance_id+"::"; x.checkpoint_key="FP19_CHECKPOINT::"+x.instance_id; return x;
}
#endif
