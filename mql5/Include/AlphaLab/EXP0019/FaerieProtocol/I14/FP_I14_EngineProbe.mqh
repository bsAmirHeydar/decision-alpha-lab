#ifndef __FP_I14_ENGINE_PROBE_MQH__
#define __FP_I14_ENGINE_PROBE_MQH__
#include "FP_I14_Contracts.mqh"
bool FP_I14_BuildHealthEvent(const long sequence,const string config_hash,FP_I14_TraceEvent &out){out.sequence=sequence;out.event_time=TimeCurrent();out.product=FP_I14_PRODUCT_DIAGNOSTIC_EA;out.event_type=FP_I14_EVENT_HEALTH;out.semantic_id="FP-I14-HEALTH";out.payload_hash="HEALTH";out.config_hash=config_hash;out.source_revision_id="REV-RUNTIME";out.state="READY";out.buffer_index=-1;out.numeric_value=0.0;return true;}
#endif
