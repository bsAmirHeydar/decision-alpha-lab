#ifndef ALPHALAB_UCEI07_CAPABILITY_MATCHER_MQH
#define ALPHALAB_UCEI07_CAPABILITY_MATCHER_MQH
#include "UCEI07_Contracts.mqh"
class CUCEI07CapabilityMatcher{
private:
 bool ContainsToken(const string list,const string token)const{if(list==token)return true;string padded="|"+list+"|";return StringFind(padded,"|"+token+"|")>=0;}
public:
 bool Match(const UCEI07_TrainerCapability &cap,const UCEI07_TaskContract &task,const UCEI07_DatasetSchema &schema,const UCEI07_ResourceBudget &budget,string &reason)const{
  reason="";
  if(!ContainsToken(cap.supported_tasks,IntegerToString((long)task.task_kind))){reason="unsupported_task";return false;}
  if(!ContainsToken(cap.supported_views,IntegerToString((long)task.view_kind))){reason="unsupported_view";return false;}
  if(!ContainsToken(cap.supported_target_shapes,task.target_shape)){reason="unsupported_target_shape";return false;}
  if(!ContainsToken(cap.supported_tensors,schema.tensor_kind)){reason="unsupported_tensor";return false;}
  if(schema.row_count<cap.min_rows){reason="insufficient_rows";return false;}
  if(schema.feature_count>cap.max_features){reason="feature_limit_exceeded";return false;}
  if(schema.output_count>cap.max_outputs){reason="output_limit_exceeded";return false;}
  if(task.sample_weight_required && !cap.sample_weight){reason="sample_weight_unsupported";return false;}
  if(task.calibration_required && cap.calibration_kinds=="none"){reason="calibration_unsupported";return false;}
  if(budget.deterministic_required && cap.determinism>UCEI07_DETERMINISM_TOLERANCE){reason="determinism_insufficient";return false;}
  if(!ContainsToken(cap.devices,budget.device)){reason="device_unsupported";return false;}
  if(!ContainsToken(cap.precisions,budget.precision)){reason="precision_unsupported";return false;}
  return true;
 }
};
#endif
